import os
import datetime
from dotenv import load_dotenv

# Flask import
from flask import Flask, request, jsonify, render_template, flash, make_response, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

# Flask JWT imports
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager

from stock import Stock

load_dotenv()
template_dir = os.path.abspath('./templates')
app = Flask(__name__, template_folder=template_dir)
app.config['SECRET_KEY'] = 'secret-key-goes-here'
app.config["JWT_SECRET_KEY"] = os.getenv('JWT_TOKEN')
app.config["JWT_TOKEN_LOCATION"] = os.getenv('JWT_TOKEN_LOCATION')
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = datetime.timedelta(minutes=int(os.getenv('JWT_ACCESS_TOKEN_EXPIRES')))
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///stock.db"

jwt = JWTManager(app)
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(50))

@app.route("/signup", methods=["POST"])
def create_user():
    name = request.form.get('username')
    password = request.form.get('password')
    hashed_password = generate_password_hash(password, method='sha256')
    try:
        new_user = User(name=name, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
    except Exception as e:
        flash('Username already exists')
        return redirect(url_for('signup'))
    flash("User created successfully")
    return redirect(url_for('login'))

@app.route("/login")
def login():
    return render_template('login.html')

@app.route("/signup")
def signup():
    return render_template('signup.html')

@app.route("/profile", methods=["POST"])
def login_post():
    username = request.form.get('username')
    password = request.form.get('password')
    user = User.query.filter_by(name=username).first()
    if not user:
        return jsonify({"msg": "No user found"}), 401
    check_pass = check_password_hash(user.password, password)
    print(user.name, user.password, check_pass)
    if username != user.name or not check_pass:
        return jsonify({"msg": "Bad username or password"}), 401
    access_token = create_access_token(identity=username)
    data = {"a":23}
    resp = make_response(render_template('profile.html', name=username, data=data))
    resp.set_cookie('access_token_cookie', access_token)
    return resp

@app.route("/logout")
@jwt_required()
def logout():
    resp = make_response()
    resp.set_cookie('access_token_cookie', '', expires=0)
    return resp


@app.route("/stocks", methods=["GET"])
@jwt_required()
def stocks():
    # Access the identity of the current user with get_jwt_identity
    current_user = get_jwt_identity()
    print(current_user)
    cmp_name = request.args.get('comp_name')
    print(cmp_name)
    stock_obj = Stock(cmp_name)
    data = stock_obj.get_info()
    print(data)
    resp = make_response(render_template('profile.html', name=current_user, data=data))
    return resp

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)