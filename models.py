from google.appengine.ext import db


class PhotoLink(db.Model):
    link = db.LinkProperty()

class AccessToken(db.Model):
    access_token = db.StringProperty()
    access_token_secret = db.StringProperty()
