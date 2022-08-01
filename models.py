from datetime import datetime
from start import db


class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime, default=datetime.now())
    title = db.Column(db.text)
    content = db.Column(db.text)
