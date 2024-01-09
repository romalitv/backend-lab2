import uuid

from flask import jsonify, request, abort
from flask_smorest import Blueprint
from marshmallow import ValidationError
from lab.models import db, CategoryModel
from lab.entities import CategorySchema

blp = Blueprint('category',__name__,description='Operations related to category')
category_schema = CategorySchema()
category = {}


@blp.post("/category")
def create_category():
    category = request.args
    try:
        data = CategorySchema().load(category)
    except ValidationError as e:
        return jsonify(e.messages), 400
    data["category_id"] = uuid.uuid4().hex
    category = CategoryModel(**data)
    try:
        db.session.add(category)
        db.session.commit()
    except Exception:
        abort(400, message="failed creating category")

@blp.get("/category")
def get_categories():
    data = category_schema.dump(CategoryModel.query.all(), many=True)
    return jsonify(data)

@blp.delete("/category/<category_id>")
def delete_category(category_id):
    category = CategoryModel.query.get(category_id)
    try:
        db.session.delete(category)
        db.session.commit()
        return jsonify(category_schema.dump(category)), 200
    except Exception:
        abort(400, message="failed deleting category")