import peewee as pw
from web import db

class BaseModel(pw.Model):
    class Meta
        database = db

class User(BaseModel):
    username = pw.CharField(unique=True)
    name = pw.TextField()
    lang = pw.CharField()
    color = pw.CharField()
    is_male = pw.BooleanField()
    quota = pw.IntegerField()
    password = pw.BlobField()
    age = pw.SmallIntegerField()
