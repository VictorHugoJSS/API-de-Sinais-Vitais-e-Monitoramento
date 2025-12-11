from flask import Flask, request, jsonify
from Database import init_db, conn, cursor,check_vitals_and_generate_alerts
from psycopg2.errors import Error

app = Flask(__name__)

init_db()

@app.teardown_appcontext
def shutdown_session(exception=None):
    cursor.close()

@app.route('/api/vitals', methods=['POST'])
def create_vitals():
    cursor = conn.cursor()
    data = request.json
    field_list = ['cpf','temperature','heart_rate','blood_pressure','respiratory_rate']
    missing_fields = [field for field in field_list if field not in data]
    if not data:
        return jsonify({'error': 'Invalid input'}), 400
    
    if missing_fields:
        return jsonify({'error': 'Invalid input',
        'missing_fields': missing_fields}), 400

    cpf=data['cpf']
    temperature=float(data.get("temperature"))
    heart_rate=int(data.get('heart_rate'))
    blood_pressure=data.get('blood_pressure')
    respiratory_rate=int(data.get('respiratory_rate'))
    
    try:
        cursor.execute("INSERT INTO vitals (cpf, temperature, heart_rate, blood_pressure, respiratory_rate) VALUES (%s,%s,%s,%s,%s)", (cpf,temperature,heart_rate,blood_pressure,respiratory_rate))
        conn.commit()
        alerts = check_vitals_and_generate_alerts(temperature,heart_rate,blood_pressure,respiratory_rate)
        cursor.execute("SELECT CURRENT_DATE")
        for alert in alerts:
            cursor.execute("INSERT INTO alerts (alert_type,message,timestamp) VALUES (%s,%s,%s)", (alert[0],alert[1],cursor.fetchall()[0]))
        conn.commit()
    except Error as e:
        return jsonify({'error': str(e)}), 500
    
    cursor.execute("SELECT id FROM vitals WHERE cpf=%s", (cpf,))
    id = cursor.fetchall()
    cursor.execute("SELECT CURRENT_TIMESTAMP")
    return jsonify({
        'vitals': {
            'id': id[0][0],
            'cpf': cpf,
            'temperature': temperature,
            'heart_rate': heart_rate,
            'blood_pressure': blood_pressure,
            'respiratory_rate': respiratory_rate,
            'timestamp': cursor.fetchall()[0]
        },
        'alerts': [{
            'alert_type':alert[0],
            'message': alert[1]
            }for alert in alerts]
    }), 201

@app.route('/api/vitals', methods=['GET'])
def get_vitals():
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM vitals")
    vitals = cursor.fetchall()
    cursor.execute("SELECT CURRENT_TIMESTAMP")
    return jsonify([{
        'id': vital[0],
        'cpf': vital[1],
        'temperature': vital[2],
        'heart_rate': vital[3],
        'blood_pressure': vital[4],
        'respiratory_rate': vital[5],
        'timestamp': cursor.fetchall(),
    } for vital in vitals]), 200

"""@app.route('/api/vitals/<patient_id>', methods=['GET'])
def get_vitals_by_patient(patient_id):
    vitals = db_session.query(Vitals).filter(Vitals.patient_id == patient_id).all()
    if not vitals:
        return jsonify({'error': 'No vitals found for this patient'}), 404
    return jsonify([{
        'id': vital.id,
        'patient_id': vital.patient_id,
        'temperature': vital.temperature,
        'heart_rate': vital.heart_rate,
        'blood_pressure': vital.blood_pressure,
        'respiratory_rate': vital.respiratory_rate,
        'timestamp': vital.timestamp,
        'device_id': vital.device_id
    } for vital in vitals]), 200"""

@app.route('/api/vitals/<id>', methods=['GET'])
def get_vitals_by_id(id):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM vitals WHERE id=%s", (id,))
    vital = cursor.fetchall()
    if not vital:
        return jsonify({'error': 'No vitals found for this id'}), 404
    return jsonify([{
        'id': vital[0][0],
        'cpf': vital[0][1],
        'temperature': vital[0][2],
        'heart_rate': vital[0][3],
        'blood_pressure': vital[0][4],
        'respiratory_rate': vital[0][5],
    }]), 200

@app.route('/api/alerts', methods=['POST'])
def create_alert():
    cursor = conn.cursor()
    data = request.json
    if not data or 'alert_type' not in data or 'message' not in data:
        return jsonify({'error': 'Invalid input'}), 400 

    # alert = Alerts(data['alert_type'], data['message'])
    
    alert_type = data['alert_type']
    message = data['message']
    
    try:
        cursor.execute("SELECT CURRENT_TIMESTAMP")
        date = cursor.fetchall()[0]
        cursor.execute("INSERT INTO alerts (alert_type,message,timestamp) VALUES (%s,%s,%s)", (alert_type,message, date))
        conn.commit()
    except Error as e:
        return jsonify({'error': str(e)}), 500
    
    cursor.execute("SELECT id,timestamp from alerts where alert_type=%s", (alert_type,))
    alert = cursor.fetchall()
    return jsonify({
        'alert_id': alert[0][0],
        'alert_type': alert_type,
        'message': message,
        'timestamp': alert[0][1]
    }), 201

@app.route('/api/alerts', methods=['GET'])
def get_alerts():
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM alerts")
    alerts = cursor.fetchall()
    return jsonify([{
        'alert_id': alert[0],
        'alert_type': alert[1],
        'message': alert[2],
        'timestamp': alert[3]
    } for alert in alerts]), 200

@app.route('/api/devices', methods=['GET', 'POST'])

def response():
    cursor = conn.cursor()
    if request.method == 'POST':
        response = request.get_json(silent=True)
        if response == {}:
            return jsonify({"Erro": "json is empty"}), 404
        
        cpf = response.get("cpf_pessoa")
        cursor.execute("SELECT CURRENT_TIMESTAMP")
        data = cursor.fetchall()
        devicename = response.get("Devicename")
        deviceModel = response.get("Devicemodel")
        deviceType = response.get("type")
        heart_rate =int(response.get("heart_rate"))
        temperature = float(response.get("temperature"))
        blood_pressure = response.get("blood_pressure")
        respiratory_rate = int(response.get("respiratory_rate"))
        
        cursor.execute("""INSERT INTO devices (cpf_pessoa,data,Devicename,Devicemodel,type,heart_rate,temperature,blood_pressure,respiratory_rate) VALUES (%s, %s, %s,%s, %s, %s,%s, %s, %s)""",(cpf,data[0], devicename,deviceModel,deviceType,heart_rate,temperature,blood_pressure,respiratory_rate))
        conn.commit()
        return jsonify({"Result": "Info saved in database"}), 200
        
    if request.method == "GET":
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM devices")
        devices = cursor.fetchall()
        
        return jsonify([{
            'id':device[0],
            'data':device[1],
            'Devicename':device[2],
            'Devicemodel':device[3],
            'type':device[4],
            'heart_rate':device[5],
            'temperature':device[6],
            'blood_pressure':device[7],
            'respiratory_rate':device[8],
            'cpf_pessoa':device[9]
        }for device in devices])