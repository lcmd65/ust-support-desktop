

class Request():
    def __init__(self):
        self.request = None
        self.respone = None
        self.status = None

class User():
    def __init__(self, username, password, email, ID, gender):
        self.username = username
        self.password = password
        self.email = email
        self.id = ID
        self.gender = gender
        self.image = None
        self.requests = []
        
        self.parsingIDRequest()
        self.parsingIDImage()
    
    def parsingIDRequest(self):
        import app.func.database
        data = app.func.database.connectUserRequest()
        for item in data:
            if item["id"] == str(self.id):
                self.requests.append(item)
    
    def parsingIDImage(self):
        import app.func.database
        self.image = app.func.database.connectUserImage(self.id)
    
    def updateRequest(self):
        self.requests.clear()
        self.parsingIDRequest()
    
        

        