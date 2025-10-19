from sqlalchemy import Table, Column, Integer, String
from sqlalchemy.orm import mapper
from .Database import metadata, db_session


class Vitals(object):
    pass

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
    pass
