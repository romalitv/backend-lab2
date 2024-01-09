import uuid

from flask import jsonify, request, abort
from flask_smorest import Blueprint
from marshmallow import ValidationError
from lab import CategoryModel, UserModel, db, RecordModel
from datetime import datetime
from lab.entities import RecordSchema

blp = Blueprint('record',__name__, description="Record operations")
record_schema = RecordSchema()
records = {}

@blp.post('/record')
def create_record():
    record = request.args
    try:
        data = record_schema.load(record)
    except ValidationError as e:
        return jsonify(e.messages), 400

    data['record_id'] = uuid.uuid4().hex
    data['time'] = datetime.now()
    user = UserModel.query.get(record['user_id'])
    category = CategoryModel.query.get(record['category_id'])
    if(category is not None and user is not None):
        data["user_id"] = user.user_id
        data["category_id"] = category.category_id
        record = RecordModel(**data)
    try:
        db.session.add(record)
        db.session.commit()
    except Exception as e:
        abort(400, message="failed creating record")



@blp.get('/record/<record_id>')
def get_record(record_id):
    record = RecordModel.query.get(record_id)
    try:
        return jsonify(record_schema.dump(record)), 200
    except Exception as e:
        abort(400, e.message)

@blp.delete('/record/<record_id>')
def delete_record(record_id):
    record = RecordModel.query.get(record_id)
    try:
        db.session.delete(record)
        db.session.commit()
    except Exception as e:
        abort(500, e.message)

@blp.get('/record')
def get_records():
    data = request.get_json()
    user_id = data['user_id']
    category_id = data['category_id']

    if user_id == "" and category_id == "":
        return jsonify({'error': 'At least one parameter (user_id or category_id) is required'}), 400

    filtered_records = [
        record for record in records.values()
        if (user_id == "" or str(record.get('user_id')) == user_id) and (
                    category_id == "" or str(record.get('category_id')) == category_id)
    ]

    return jsonify({'records': filtered_records})
