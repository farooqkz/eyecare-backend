"""
    Copyright (C) 2024 Eyecare Team

    All rights is reserved
"""


from uuid import uuid4
from random import choice
from typing import Optional

from flask import request
from flask import session
from flask import abort
from flask import g
from flask import make_response
from bcrypt import checkpw
import cv2 as cv

from web import app
from model import User, DailyTip
from ml import detect_diabetes


VALID_LANGS = {"fa", "en"}
def get_daily_tip(lang: str) -> str:
    if lang not in VALID_LANGS:
        raise ValueError("Invalid lang. It should be either 'fa' or 'en'")
    if "daily_tip" not in g:
        g.daily_tip = dict()
        tips = list(DailyTip.select().dicts())
        g.daily_tip["en"] = list(map(lambda tip: tip["tip_en"], tips))
        g.daily_tip["fa"] = list(map(lambda tip: tip["tip_fa"], tips))
    return choice(g.daily_tip[lang])


@app.route("/login", methods=("POST", ))
def login():
    print("Incoming login request")
    if request.json is None:
        print("Incoming request is not json")
        abort(404)
    
    username = request.json.get("username")
    password = request.json.get("password")

    if username is None or password is None:
        print("No userpass")
        abort(404)

    user = User.get_or_none(User.select().where(User.username == username))
    if user is None:
        return { "login_result": "credentials" }

    if checkpw(password.encode(), user.password):
        session["user"] = user.username
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


@app.route("/dailyTip/<lang>")
def daily_tip(lang: str):
    username = session.get("user")
    if username is None:
        lang = "fa"
    else:
        lang = User.get(User.select().where(User.username == username)).lang
    return get_daily_tip(lang)


@app.route("/diabetes", methods=("POST", ))
def diabetes():
    if session.get("user") is None:
        abort(403)
    pic = request.get_data() 
    if pic is None:
        abort(404)
    User.update(quota = User.quota - 1).where(User.username == session.get("user")).execute()    
    if detect_diabetes(pic):
        return "yes"
    else:
        return "no"

@app.route("/ping")
def ping():
    return "pong"

@app.route("/quota")
def quota():
    username = session.get("user")
    if username is None:
        abort(403)
    
    user = User.get(User.select().where(User.username == username))
    return str(user.quota)


