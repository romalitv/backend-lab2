import uuid

from flask import jsonify, request
from lab import app
from datetime import datetime

users = {}

@app.get('/healthcheck')
def healthcheck():
    current_date = datetime.now()
    current_status = "ok"
    health_status = {'status': current_status, 'date': current_date}
    return jsonify(health_status)


@app.post('/user')
def create_user():
    data = request.get_json()
    user_name = data['user_name']
    user_id = uuid.uuid4().hex
    user = {"id": user_id, "user_name": user_name}
    users[user_id] = user
    return jsonify(user)


@app.get('/users')
def get_users():
    return list(users.values())

@app.get('/user/<user_id>')
def get_user(user_id):
    if user_id in users:
        user = users[user_id]
        return jsonify(user)
    else:
        return jsonify({'message': 'User not found'}), 404


@app.delete('/user/<user_id>')
def delete_user(user_id):
    if user_id in users:
        deleted_user = users.pop(user_id)
        return jsonify({'message': 'User deleted successfully', 'user': deleted_user}), 200
    else:
        return jsonify({'message': 'User not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)