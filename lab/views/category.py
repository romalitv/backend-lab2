import uuid

from flask import jsonify, request
from lab import app

categories = {}

@app.post("/category")
def create_category():
    data = request.get_json()

    if not data or 'category_name' not in data:
        return jsonify({'error': 'Invalid data format. Required field: category_name'}), 400

    category_name = data["category_name"]
    category_id = uuid.uuid4().hex
    category = {"id": category_id, "category_name": category_name}
    categories[category_id] = category

    return jsonify(category)

@app.get("/category")
def get_categories():
    return list(categories.values())

@app.delete("/category/<category_id>")
def delete_category(category_id):
    if category_id in categories:
        deleted_category = categories.pop(category_id)
        return jsonify({'message': 'Category deleted successfully', 'category': deleted_category}), 200
    else:
        return jsonify({'message': 'Category not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)