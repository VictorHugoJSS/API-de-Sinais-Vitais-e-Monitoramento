import datetime
import uuid
from sqlalchemy import Table, Column, Integer, String, ForeignKey, Float, Numeric
from sqlalchemy.orm import mapper
from .Database import metadata, db_session


class Vitals(object):
    def __init__(self, patient_id, temperature, heart_rate, blood_pressure, respiratory_rate, device_id):
        self.patient_id = patient_id
        self.temperature = temperature
        self.heart_rate = heart_rate
        self.blood_pressure = blood_pressure
        self.respiratory_rate = respiratory_rate
        self.timestamp = datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')
        self.device_id = device_id

    def __repr__(self):
        return f'<Vitals {self.patient_id!r}>'

vitals = Table('vitals', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('patient_id', Integer), #cpf
    Column('temperature', String(10)),
    Column('heart_rate', String(10)),
    Column('blood_pressure', String(10)),
    Column('respiratory_rate', String(10)),
    Column('timestamp', String(20)),
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