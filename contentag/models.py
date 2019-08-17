from contentag import db
from flask_login import UserMixin
from sqlalchemy import Column, Integer, String
from datetime import datetime


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    title = db.Column(db.String(250), nullable=False)
    url = db.Column(db.String(500), nullable=False)
    img_path = db.Column(db.String(250))
    date_created = db.Column(db.String(100))
    source_id = db.Column(db.Integer, db.ForeignKey(
        'source.id'), nullable=False)

    def __init__(self, title, url, img_path, date_created, source_id):
        self.title = title
        self.url = url
        self.img_path = img_path
        self.date_created = date_created
        self.source_id = source_id

    def serialize(self):
        return {
            'title': self.title,
            'url': self.url,
            'img_path': self.img_path,
            'date_created': self.date_created,
            'source_id': self.source_id
        }


class Source(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(200), nullable=False)
    source = db.relationship('Article', backref='source', lazy=True)

    def serialize(self):
        return {
            'name': self.name
        }
