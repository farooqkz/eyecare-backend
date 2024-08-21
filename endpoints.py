from flask import request
from flask import session
from flask import abort
from flask import g
import random
from uuid import uuid4
from cv import get_iris

from web import app, loginmgr
from model import User, DailyTip
from ml import detect_diabetes

def get_daily_tip(lang: "en" | "fa") -> str:
    if "daily_tip" not in g:
        g.daily_tip = dict()
        tips = list(DailyTip.select().dicts())
        g.daily_tip["en"] = map(lambda tip: tip["tip_en"], tips)
        g.daily_tip["fa"] = map(lambda tip: tip["tip_fa"], tips)
    random.choice(g.daily_tip[lang])


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
        session["user"] = user
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

@app.route("/logout")
def logout():
    session.pop("username", None)
    return { "login_result": "success" }


@app.route("/dailyTip")
def daily_tip():
    if session.get("user") is None:
        lang = "fa"
    else:
        lang = session.get("user").lang
    return get_daily_tip(lang)

@app.route("/diabetes/<iris_id>")
def diabetes(iris_id: str):
    if session.get("user") is None:
        abort(403)

    if detect_diabetes(g.irides[iris_id]):
        return "yes"
    else:
        return "no"


@app.route("/iris", method="POST")
def iris():
    if session.get("user") is None:
        abort(403)
 
    image = request.get_data(as_text=False)
    image_obj = cv2.imdecode(image, cv.IMREAD_GRAYSCALE)
    iris_id = str(uuid4())
    iris = get_iris(image_obj)
    if iris is None:
        abort(400)
    store_iris(
        iris_id,
        get_iris(image_obj)
    )

    return iris_id
