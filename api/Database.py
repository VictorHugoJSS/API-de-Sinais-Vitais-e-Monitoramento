import psycopg2

CONNECTION=f"postgres://vitalsapp:test@timescaledb/vitals"

conn = psycopg2.connect(CONNECTION)
cursor = conn.cursor()

def init_db():
    cursor.execute("""DROP TABLE IF EXISTS alerts,vitals,devices""")
    # cursor.execute("""DROP TABLE IF EXISTS devices""")
    # cursor.execute("""DROP TABLE IF EXISTS  vitals""")
    
    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS alerts(
                       id serial,
                       alert_type TEXT NOT NULL,
                       message TEXT NOT NULL,
                       timestamp date
                   )
                   WITH(
                       tsdb.hypertable,
                       tsdb.partition_column='timestamp',
                       tsdb.segmentby = 'alert_type',
                       tsdb.orderby = 'timestamp DESC'
                   )
                   """)
    
    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS vitals(
                       id serial,
                       cpf TEXT PRIMARY KEY,
                       temperature DOUBLE PRECISION,
                       heart_rate INTEGER,
                       blood_pressure TEXT,
                       respiratory_rate INTEGER
                   )
                   """)
    
    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS devices(
                       id serial,
                       data TIMESTAMP WITHOUT TIME ZONE NOT NULL,
                       Devicename TEXT NOT NULL,
                       Devicemodel TEXT,
                       type TEXT,
                       heart_rate INTEGER,
                       temperature DOUBLE PRECISION,
                       blood_pressure DOUBLE PRECISION,
                       respiratory_rate INTEGER,
                       cpf_pessoa TEXT references vitals
                   )
                   WITH(
                       tsdb.hypertable,
                       tsdb.partition_column ='data',
                       tsdb.segmentby = 'Devicename',
                       tsdb.orderby = 'data DESC'
                   )
                   """)
    
    cursor.execute("""CALL add_columnstore_policy('devices', INTERVAL '1 days', if_not_exists => TRUE);""")
    cursor.execute("""CALL add_columnstore_policy('alerts', INTERVAL '1 days', if_not_exists => TRUE);""")
    conn.commit()

def check_vitals_and_generate_alerts(temperature, heart_rate, blood_pressure,respiratory_rate):
        alerts = []
        if temperature < 35.0:
            alert_type='TEMPERATURE_LOW', 
            message=f'Hipotermia detectada: {temperature}°C'
            alerts.append((alert_type,message))
        elif temperature > 38.0:
            alert_type='TEMPERATURE_HIGH',
            message=f'Febre detectada: {temperature}°C'
            alerts.append((alert_type,message))

        if heart_rate < 50:
            alert_type='HEART_RATE_LOW', 
            message=f'Frequência cardíaca baixa: {heart_rate} bpm'
            alerts.append((alert_type,message))
        elif heart_rate > 120:
            alert_type='HEART_RATE_HIGH', 
            message=f'Frequência cardíaca elevada: {heart_rate} bpm'
            alerts.append((alert_type,message))

        try:
            systolic, diastolic = blood_pressure.split('/')
            systolic = int(systolic)
            diastolic = int(diastolic)
            if systolic < 90 or diastolic < 60:
                alert_type='BLOOD_PRESSURE_LOW', 
                message=f'Pressão arterial baixa: {blood_pressure} mmHg'
                alerts.append(alert_type,message)
            elif systolic > 140 or diastolic > 90:
                alert_type='BLOOD_PRESSURE_HIGH', 
                message=f'Pressão arterial elevada: {blood_pressure} mmHg'
                alerts.append((alert_type,message))
        except (ValueError, AttributeError):
            alert_type='BLOOD_PRESSURE_ERROR', 
            message='Formato de pressão arterial inválido'
            alerts.append((alert_type,message))

        if respiratory_rate < 10:
            alert_type='RESPIRATORY_RATE_LOW', 
            message=f'Frequência respiratória baixa: {respiratory_rate} irpm'
            alerts.append((alert_type,message))
        elif respiratory_rate > 24:
            alert_type='RESPIRATORY_RATE_HIGH', 
            message=f'Frequência respiratória elevada: {respiratory_rate} irpm'
            alerts.append((alert_type, message))

        return alerts