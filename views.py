from flask.views import View, request

class Vitals(View):
    
    def dispatch_request(self):
        if request.method == "POST":
            pass
        
        if request.method == "GET":
            pass
        

class Device(View):
    methods = ['GET', 'POST', 'PUT']
    
    def dispatch_request(self):
        if request.method == "GET":
            pass
        
        if request.method == "POST":
            pass
        
        if request.method == "PUT":
            pass
