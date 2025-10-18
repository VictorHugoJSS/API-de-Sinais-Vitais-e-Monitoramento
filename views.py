from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask("Sistemas Vitais & Monitoramento")
app.config['SQLALCHEMY_DATABASE_URI'] = ''
db = SQLAlchemy(app)

class Vitals(db.Model):
    id = db.Column()
        

class Device(db.Model):
    pass

class Alerts(db.Model):
    pass
