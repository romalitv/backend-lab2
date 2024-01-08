import uuid

from flask import jsonify, request
from marshmallow import ValidationError

from lab import app
from lab.models import UserModel, db
from lab.entities import PlainUserSchema
from datetime import datetime

user_schema = PlainUserSchema()

@app.get('/healthcheck')
def healthcheck():
    current_date = datetime.now()
    current_status = "ok"
    health_status = {'status': current_status, 'date': current_date}
    return jsonify(health_status)


@app.post('/user')
def create_user():
    try:
      data = user_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400

    data['user_id'] = uuid.uuid4().hex
    user = UserModel(**data)
    try:
        db.session.add(user)
        db.session.commit()
    except Exception as e:
        db.session.rollback()

    return jsonify(user)


@app.get('/users')
def get_users():
    data = user_schema.dump(UserModel.query.all(), many=True)
    return jsonify(data)

@app.get('/user/<user_id>')
def get_user(user_id):
    user = UserModel.query.get(user_id)
    try:
        return jsonify(user_schema.dump(user)), 200
    except Exception as e:
        db.session.rollback()


@app.delete('/user/<user_id>')
def delete_user(user_id):
    user = UserModel.query.get(user_id)
    try:
        db.session.delete(user)
        db.session.commit()
        return jsonify(user_schema.dump(user)), 200
    except Exception as e:
        db.session.rollback()


if __name__ == '__main__':
    app.run(debug=True)