import peewee as pw
from flask import Flask
from toml import load

app = Flask(__name__)
app.secret_key = b"HelloWorld"
app.config.from_file("config.toml", load=load)

all_config = load("config.toml")

db = pw.SqliteDatabase("/var/tmp/eyecare.sqlite", autocommit=True)

@app.before_request  
def db_connect():
        db.connect()

@app.teardown_request
def db_disconnect(_):
    if not db.is_closed():
        db.close()
