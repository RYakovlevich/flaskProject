from datetime import datetime
from settings import db


class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime, default=datetime.now().replace(microsecond=0))
    title = db.Column(db.Text)
    content = db.Column(db.Text)
