from datetime import datetime
import uuid
from sqlalchemy import Table, Column, Integer, String, ForeignKey, Float, Numeric, DateTime
from sqlalchemy.orm import mapper
from Database import metadata, db_session


class Vitals(object):
    def __init__(self, patient_id, temperature, heart_rate, blood_pressure, respiratory_rate, device_id):
        self.id = str(uuid.uuid4())
        self.patient_id = patient_id
        self.temperature = temperature
        self.heart_rate = heart_rate
        self.blood_pressure = blood_pressure
        self.respiratory_rate = respiratory_rate
        self.timestamp = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
        self.device_id = device_id

    def __repr__(self):
        return f'<Vitals {self.patient_id!r}>'
    
    def check_vitals_and_generate_alerts(self):
        alerts = []
        if self.temperature < 35.0:
            alerts.append(Alerts(
                alert_type='TEMPERATURE_LOW', 
                message=f'Hipotermia detectada: {self.temperature}°C'
            ))
        elif self.temperature > 38.0:
            alerts.append(Alerts(
                alert_type='TEMPERATURE_HIGH', 
                message=f'Febre detectada: {self.temperature}°C'
            ))

        if self.heart_rate < 50:
            alerts.append(Alerts(
                alert_type='HEART_RATE_LOW', 
                message=f'Frequência cardíaca baixa: {self.heart_rate} bpm'
            ))
        elif self.heart_rate > 120:
            alerts.append(Alerts(
                alert_type='HEART_RATE_HIGH', 
                message=f'Frequência cardíaca elevada: {self.heart_rate} bpm'
            ))

        try:
            systolic, diastolic = map(int, self.blood_pressure.split('/'))
            if systolic < 90 or diastolic < 60:
                alerts.append(Alerts(
                    alert_type='BLOOD_PRESSURE_LOW', 
                    message=f'Pressão arterial baixa: {self.blood_pressure} mmHg'
                ))
            elif systolic > 140 or diastolic > 90:
                alerts.append(Alerts(
                    alert_type='BLOOD_PRESSURE_HIGH', 
                    message=f'Pressão arterial elevada: {self.blood_pressure} mmHg'
                ))
        except (ValueError, AttributeError):
            alerts.append(Alerts(
                alert_type='BLOOD_PRESSURE_ERROR', 
                message='Formato de pressão arterial inválido'
            ))

        if self.respiratory_rate < 10:
            alerts.append(Alerts(
                alert_type='RESPIRATORY_RATE_LOW', 
                message=f'Frequência respiratória baixa: {self.respiratory_rate} irpm'
            ))
        elif self.respiratory_rate > 24:
            alerts.append(Alerts(
                alert_type='RESPIRATORY_RATE_HIGH', 
                message=f'Frequência respiratória elevada: {self.respiratory_rate} irpm'
            ))

        return alerts

vitals = Table('vitals', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('patient_id', String(14)), #cpf
    Column('temperature', Float),
    Column('heart_rate', Integer),
    Column('blood_pressure', String(6)),
    Column('respiratory_rate', Float),
    Column('timestamp', DateTime, default=datetime.now),
    Column('device_id', ForeignKey('devices.id'))
)
mapper(Vitals, vitals)

class Device(object):
    query = db_session.query_property()
    
    def __init__(self, deviceName, model, type):
        self.deviceName = deviceName
        self.model = model
        self.type = type
    
    def __repr__(self):
        return f'<Device {self.deviceName!r}>'
    
devices = Table('devices', metadata,
    Column('id', primary_key=True),
    Column('Devicename', String(100)),
    Column('model', String(20)),
    Column('type', String(10)),
    Column('heart_rate', Integer),
    Column('temperature', Float),
    Column('blood_pressure', Numeric),
    Column('respiratory_rate', Numeric)
)
mapper(Device, devices)

class Alerts(object):
    def __init__(self, alert_type, message):
        self.alert_id = str(uuid.uuid4())
        self.alert_type = alert_type
        self.message = message
        self.timestamp = datetime.now().strftime("%d %m %Y %H:%M:%S")

    def to_dict(self):
        return {
            'alert_type': self.alert_type,
            'message': self.message,
            'timestamp': self.timestamp
        }
    def __repr__(self):
        return f'<Alert {self.alert_type!r}>'


alerts_table = Table('alerts', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('alert_type', String(50)),
    Column('message', String(255)),
    Column('timestamp', String(20))
)

mapper(Alerts, alerts_table)