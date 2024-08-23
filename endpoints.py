from uuid import uuid4
from random import choice
from typing import Optional

from flask import request
from flask import session
from flask import abort
from flask import g
from bcrypt import checkpw
import cv2 as cv

from web import app
from model import User, DailyTip
from ml import detect_diabetes
from computer_vision import get_iris, Iris


VALID_LANGS = {"fa", "en"}
def get_daily_tip(lang: str) -> str:
    if lang not in VALID_LANGS:
        raise ValueError("Invalid lang. It should be either 'fa' or 'en'")
    if "daily_tip" not in g:
        g.daily_tip = dict()
        tips = list(DailyTip.select().dicts())
        g.daily_tip["en"] = map(lambda tip: tip["tip_en"], tips)
        g.daily_tip["fa"] = map(lambda tip: tip["tip_fa"], tips)
    return choice(g.daily_tip[lang])


def get_iris_by_id(iris_id: str) -> Optional[bytes]:
    if g.irides is None:
        return None
    else:
        return g.irides.get(iris_id)


def store_iris(iris_id: str, iris: Iris):
    if g.irides is None:
        g.irides = dict()
    g.irides[iris_id] = iris


@app.route("/login", method="POST")
def login():
    if request.json is None:
        abort(404)
    
    username = request.json.get("username")
    password = request.json.get("password")

    if username is None or password is None:
        abort(404)

    user = User.get_or_none(User.select().where(User.username == username))
    if user is None:
        return { "login_result": "credentials" }

    if checkpw(password.encode(), user.password.encode()):
        session["user"] = user
        return {
            "login_result": "success",
            "userPreference": {
                "colorScheme": user.color,
                "lang": user.lang,
            },
            "userInfo": {
                "age": user.age,
                "gender": "male" if user.is_male else "female",
                "name": user.name
            }
        }
    else:
        return {
            "login_result": "credentials"
        }

@app.route("/logout")
def logout():
    session.pop("username", None)
    return { "login_result": "success" }


@app.route("/dailyTip")
def daily_tip():
    user_obj = session.get("user")
    if user_obj is None:
        lang = "fa"
    else:
        lang = user_obj.lang
    return get_daily_tip(lang)

@app.route("/diabetes/<iris_id>")
def diabetes(iris_id: str):
    if session.get("user") is None:
        abort(403)
    
    iris = get_iris_by_id(iris_id)
    if iris is None:
        abort(404)

    feats = 
    if detect_diabetes(iris):
        return "yes"
    else:
        return "no"


@app.route("/iris", method="POST")
def iris():
    if session.get("user") is None:
        abort(403)
 
    image = request.get_data(as_text=False)
    image_obj = cv.imdecode(image, cv.IMREAD_GRAYSCALE)
    iris_id = str(uuid4())
    iris = get_iris(image_obj)
    if iris is None:
        abort(400)
    store_iris(
        iris_id,
        get_iris(image_obj)
    )

    return iris_id
