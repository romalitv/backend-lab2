import uuid

from flask import jsonify, request
from lab import app
from datetime import datetime

records = {}

@app.post('/record')
def create_record():
    data = request.get_json()

    if not data or 'user_id' not in data or 'category_id' not in data or 'amount_of_money' not in data:
        return jsonify({'error': 'Invalid data format. Required fields: user_id, category_id, amount_of_money'}), 400

    try:
        amount_of_money = float(data['amount_of_money'])
    except ValueError:
        return jsonify({'error': 'Invalid amount_of_money. Must be a valid number.'}), 400

    record_id = uuid.uuid4().hex
    user_id = data['user_id']
    category_id = data['category_id']
    time = datetime.now()
    record = {"record_id": record_id, "user_id": user_id, "category_id": category_id, "time": time, "amount_of_money": amount_of_money}
    records[record_id] = record
    return jsonify(record)

@app.get('/record/<record_id>')
def get_record(record_id):
    if record_id in records:
        record = records[record_id]
        return jsonify(record)
    else:
        return jsonify({'message': 'Record not found'}), 404

@app.delete('/record/<record_id>')
def delete_record(record_id):
    if record_id in records:
        delete_record = records.pop(record_id)
        return jsonify({'message': 'Record deleted successfully', 'user': delete_record}), 200
    else:
        return jsonify({'message': 'Record not found'}), 404

@app.get('/record')
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

if __name__ == '__main__':
    app.run(debug=True)
