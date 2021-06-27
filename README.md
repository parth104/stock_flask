# stock_flask

This is my first Flask Api project using JWT. 

Steps to run
1. Clone the repo
2. Install the dependencies using `pip install -r requirements.txt`
3. run python api\routes.py


# Enhancement Required
1. Currently if JWT token expires for current user it shows access_token_expired message. Need to create mechanism like if user currently active create new token.
2. UI is very bad need to make it porper. 
3. Login button is showed even if user is logged in
4. Stock data is not porper format only shows current value. We can add more data insights
5. No validations are made on sign up data.
6. Code is not modular, We can create separate file for model storing
