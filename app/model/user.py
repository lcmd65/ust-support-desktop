

class Request():
    def __init__(self):
        self.request = None
        self.respone = None
        self.status = None

class User():
    def __init__(self, username, password, email, ID):
        self.username = username
        self.password = password
        self.email = email
        self.id = ID
        self.image = None
        self.requests = []
        
        self.parsingIDRequest()
        self.parsingIDImage()
    
    def parsingIDRequest(self):
        import app.func.database
        data = app.func.database.connectUserRequest()
        for item in data:
            if item["_id"] == self.id:
                self.requests.append(item)
    
    def parsingIDImage(self):
        import app.func.database
        self.image = app.func.database.connectUserImage(self.id)
    
        

        