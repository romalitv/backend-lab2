from flask import jsonify
from lab import app
from datetime import datetime

@app.get('/healthcheck')
def healthcheck():
    current_date = datetime.now()
    current_status = "ok"
    health_status = {'status': current_status, 'date': current_date}
    return jsonify(health_status)

if __name__ == '__main__':
    app.run(debug=True)