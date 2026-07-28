from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class FeatureFlag(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    name = db.Column(
        db.String(100),
        unique=True,
        nullable=False
    )

    enabled = db.Column(
        db.Boolean,
        default=False
    )
