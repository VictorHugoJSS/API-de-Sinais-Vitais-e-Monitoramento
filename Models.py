import datetime
from sqlalchemy import Table, Column, Integer, String
from sqlalchemy.orm import mapper
from .Database import metadata, db_session


class Vitals(object):
    def __init__(self, temperature, heart_rate, blood_pressure, respiratory_rate):
        self.temperature = temperature
        self.heart_rate = heart_rate
        self.blood_pressure = blood_pressure
        self.respiratory_rate = respiratory_rate

class Device(object):
    query = db_session.query_property()
    
    def __init__(self, deviceName, model, type):
        self.deviceName = deviceName
        self.model = model
        self.type = type
    
    def __repr__(self):
        return f'<Device {self.deviceName!r}>'
    
devices = Table('devices', metadata,
    Column('id', autoincrement=Integer, primary_key=True),
    Column('Devicename', String(100), unique=True),
    Column('model', String(10), unique=True),
    Column('type', String(7))
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

mapper(Alert, alerts_table)