from flask import Flask
from Database import init_db, db_session

app = Flask(__name__)

init_db()
db_session = db_session()

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()
    
@app.route('/vitals')
def response():
    pass

@app.route('/api/alerts', methods=['POST'])
def create_alert():
    data = request.json
    if not data or 'alert_type' not in data or 'message' not in data:
        return jsonify({'error': 'Invalid input'}), 400 

    alert = Alert(data['alert_type'], data['message'])
    
    try:
        db_session.add(alert)
        db_session.commit()
    except Exception as e:
        db_session.rollback()
        return jsonify({'error': str(e)}), 500

    return jsonify({
        'alert_id': alert.id,
        'alert_type': alert.alert_type,
        'message': alert.message,
        'timestamp': alert.timestamp
    }), 201

@app.route('/api/alerts', methods=['GET'])
def get_alerts():
    alerts = db_session.query(Alert).all()
    return jsonify([{
        'alert_id': alert.id,
        'alert_type': alert.alert_type,
        'message': alert.message,
        'timestamp': alert.timestamp
    } for alert in alerts]), 200
