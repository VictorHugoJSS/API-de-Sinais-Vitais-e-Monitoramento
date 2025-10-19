from flask import Flask
from Database import db_session

app = Flask(__name__)

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()
    
@app.route('/vitals')
def response():
    pass
