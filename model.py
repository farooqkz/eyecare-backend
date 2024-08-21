import peewee as pw
from web import db

class BaseModel(pw.Model):
    class Meta
        database = db

class User(BaseModel):
    username = pw.CharField(unique=True, index=True)
    name = pw.TextField()
    lang = pw.CharField()
    color = pw.CharField()
    is_male = pw.BooleanField()
    quota = pw.IntegerField()
    password = pw.BlobField()
    age = pw.SmallIntegerField()

class DailyTip(BaseModel):
    id = pw.IntegerField(unique=True)
    tip_en = pw.TextField()
    tip_fa = pw.TextField()
