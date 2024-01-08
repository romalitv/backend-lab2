import uuid

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'

    user_id = db.Column(db.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_name = db.Column(db.String(), unique=True, nullable=False)

    record = db.relationship("RecordModel", back_populates="user", lazy="dynamic")


class Category(db.Model):
    __tablename__ = 'category'

    category_id = db.Column(db.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    category_name = db.Column(db.String(), unique=True, nullable=False)
    is_common = db.Column(db.Boolean(), default=False, nullable=False)

    record = db.relationship("RecordModel", back_populates="category", lazy="dynamic")


class RecordModel(db.Model):
    __tablename__ = 'record'

    record_id = db.Column(db.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4())
    user_id = db.Column(db.UUID(as_uuid=True),
                        db.ForeignKey('user.user_id'),
                        unique=True,
                        nullable=False
                        )
    category_id = db.Column(db.UUID(as_uuid=True),
                            db.ForeignKey('category.category_id'),
                            unique=True,
                            nullable=False
                            )
    time = db.Column(db.DateTime, server_default=func.now(), nullable=False)
    amount_of_money = db.Column(db.Float(), unique=False, nullable=False)

    user = db.relationship("UserModel", back_populates="record")
    category = db.relationship("CategoryModel", back_populates="record")