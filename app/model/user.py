import app.func.database

class Request():
    def __init__(self):
        self.request = None
        self.respone = None

class User():
    def __init__(self, username, password, email, ID):
        self.username = username
        self.password = password
        self.email = email
        self.id = ID
        self.requests = []
    
    def parsingIDRequest(self):
        data = app.func.database.connectUserRequest()
        for item in data:
            if item["id"] == self.id:
                self.requests.append(item)
    
        

        