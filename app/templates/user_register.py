import app.view.var
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from functools import partial
from app.func.database import addUserMongoDB

class UserRegister(QMainWindow):
    def __init__(self, parent = None):
        super().__init__()
        self.setWindowTitle("Forgot Password")
        self.resize(990, 540)
        
        self.changepass_toplevel = None
        
        self.setExternalVal()
        self.initUI()
        self.setStyleObject()
    
    def eventSetExternalVal(self):
        app.view.var.background_view = QPixmap('app/images/background_login.png').scaled(810, 801,\
            Qt.AspectRatioMode.KeepAspectRatioByExpanding,\
            Qt.TransformationMode.SmoothTransformation) ##4213 × 4167

    def setStyle(self, object, css_path):
        with open(css_path,"r") as file:
            style= file.read()
            object.setStyleSheet(style)
        file.close()
    
    def setExternalVal(self):
        pass
    
    def eventButtonClickedRegister(self, username, email, id, gender, password, confirm_password):
        if password.text() == confirm_password.text():
            bool = addUserMongoDB(username.text() , email.text() , password.text() , int(id.text()) , gender.text())
            if bool == True:
                msgBox= QMessageBox()
                msgBox.setText("Register Successful")
                msgBox.addButton(QMessageBox.StandardButton.Yes)
                response = msgBox.exec()
                if response == QMessageBox.StandardButton.Yes:
                    self.close()
            else:
                msgBox= QMessageBox()
                msgBox.setText("Information is existing on current system")
                msgBox.addButton(QMessageBox.StandardButton.Yes)
                response = msgBox.exec()
        else:
            msg_box = QMessageBox()
            msg_box.setText("Password don't match")
            msg_box.addButton(QMessageBox.StandardButton.Ok)
            msg_box.exec()

                                                
    def initUI(self): 
        self.frame = QFrame()
        self.main_form = QFormLayout()   
        self.frame.setLayout(self.main_form)
        self.main_form.setAlignment(Qt.AlignmentFlag.AlignTop)     
        self.username = QLineEdit()
        self.email = QLineEdit()
        self.id = QLineEdit()
        self.gender =  QLineEdit()
        self.password = QLineEdit(echoMode=QLineEdit.EchoMode.Password)
        self.confirm_password = QLineEdit(echoMode=QLineEdit.EchoMode.Password)
        self.button = QPushButton("OK")
        self.button.setMaximumWidth(100)
        self.button.clicked.connect(partial(self.eventButtonClickedRegister, self.username, self.email, self.id, self.gender, self.password, self.confirm_password))
        
        self.main_form.addRow('Username:', self.username)
        self.main_form.addRow('Email:', self.email)
        self.main_form.addRow('Mã số sinh viên:', self.id)
        self.main_form.addRow('Giới tính (M/F):', self.gender)
        self.main_form.addRow('Mật khẩu:', self.password)
        self.main_form.addRow('Xác nhận lại mật khẩu:', self.confirm_password)
        self.main_form.addRow(self.button) 
        self.setCentralWidget(self.frame) 
           
    def setStyleObject(self):
        self.setStyle(self.username, "app/static/css/user_info/line.css")
        self.setStyle(self.email, "app/static/css/user_info/line.css")
        self.setStyle(self.id, "app/static/css/user_info/line.css")
        self.setStyle(self.gender, "app/static/css/user_info/line.css")
        self.setStyle(self.password, "app/static/css/user_info/line.css")
        self.setStyle(self.confirm_password, "app/static/css/user_info/line.css")
        self.setStyle(self.frame,"app/static/css/user_info/frame.css" )