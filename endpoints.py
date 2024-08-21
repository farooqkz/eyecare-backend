from flask import request
from flask import session
from flask import abort


from web import app
from model import User
from ml import detect_diabetes

@app.route("/login", method="POST")
def login():
    if not request.is_json:
        abort(404)

    username = request.json.get("username")
    password = request.json.get("password")

    if username is None or password is None:
        abort(404)

    user = User.get_or_none(User.select().where(User.username == username))
    if user is None:
        return { login_result: "credentials" }

    if bcrypt.checkpw(password.encode(), user.password.encode()):
        flask_login.login_user(user)
        return {
            "login_result": "success",
            "userPreference": {
                "colorScheme": user.color,
                "lang": user.lang,
            },
            "userInfo": {
                "age": user.age,
                "gender": "male" if user.is_male == True else "female",
                "name": user.name
            }
        }
    else:
        return {
            "login_result": "credentials"
        }
