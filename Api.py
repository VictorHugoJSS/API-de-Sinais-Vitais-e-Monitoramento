from flask import Flask, request, jsonify
from Database import init_db, db_session
from Models import  Vitals, Alerts

app = Flask(__name__)

init_db()
db_session = db_session()

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

@app.route('/api/vitals', methods=['POST'])
def create_vitals():
    data = request.json
    if not data or ('patient_id' or 'temperature' or 'heart_rate' or 'blood_pressure' or 'respiratory rate' or 'timestamp' or 'device_id') not in data:
        return jsonify({'error': 'Invalid input'}), 400

    vitals = Vitals(
        patient_id=data['patient_id'], temperature=data['temperature'], heart_rate=data['heart_rate'],
        blood_pressure=data['blood_pressure'], respiratory_rate=data['respiratory_rate'], device_id=data['device_id']
    )
    
    try:
        db_session.add(vitals)
        db_session.commit()
    except Exception as e:
        db_session.rollback()
        return jsonify({'error': str(e)}), 500
    
    return jsonify({
        'patient_id': vitals.patient_id,
        'temperature': vitals.temperature,
        'heart_rate': vitals.heart_rate,
        'blood_pressure': vitals.blood_pressure,
        'respiratory_rate': vitals.respiratory_rate,
        'timestamp': vitals.timestamp,
        'device_id': vitals.device_id
    }), 201

@app.route('/api/vitals', methods=['GET'])
def get_vitals():
    vitals = db_session.query(Vitals).all()
    return jsonify([{
        'patient_id': vital.patient_id,
        'temperature': vital.temperature,
        'heart_rate': vital.heart_rate,
        'blood_pressure': vital.blood_pressure,
        'respiratory_rate': vital.respiratory_rate,
        'timestamp': vital.timestamp,
        'device_id': vital.device_id
    } for vital in vitals]), 200

@app.route('/api/vitals/<patient_id>', methods=['GET'])
def get_vitals_by_patient(patient_id):
    vitals = db_session.query(Vitals).filter(Vitals.patient_id == patient_id).all()
    if not vitals:
        return jsonify({'error': 'No vitals found for this patient'}), 404
    return jsonify([{
        'patient_id': vital.patient_id,
        'temperature': vital.temperature,
        'heart_rate': vital.heart_rate,
        'blood_pressure': vital.blood_pressure,
        'respiratory_rate': vital.respiratory_rate,
        'timestamp': vital.timestamp,
        'device_id': vital.device_id
    } for vital in vitals]), 200

@app.route('/api/alerts', methods=['POST'])
def create_alert():
    data = request.json
    if not data or 'alert_type' not in data or 'message' not in data:
        return jsonify({'error': 'Invalid input'}), 400 

    alert = Alerts(data['alert_type'], data['message'])
    
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
    alerts = db_session.query(Alerts).all()
    return jsonify([{
        'alert_id': alert.id,
        'alert_type': alert.alert_type,
        'message': alert.message,
        'timestamp': alert.timestamp
    } for alert in alerts]), 200
