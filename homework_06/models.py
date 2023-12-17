from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Record(db.Model):
    __tablename__ = "record"
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(255), nullable=False)
