import app.environment
import app.view.var
import app.func.database
from app.view.view import homeViewQT
from app.templates.home import HomeQT
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from functools import partial
from app.func.database import userAuthentication
from PyQt6.QtWidgets import QMessageBox

################################################################################################################################################################################
# QWWidget for login ###########################################################################################################################################################
################################################################################################################################################################################
class QLabel_alterada(QLabel):
    clicked=pyqtSignal()
    
    def mousePressEvent(self, ev):
        self.clicked.emit()
    
class LoginUIQT(QWidget):
    def __init__(self, parent = None):
        super().__init__()
        self.setWindowTitle("HCMUS Assistant")
        self.resize(1980, 1080) 
        self.setExternalVal()
        self.initUI()
        self.setObjectStyleCSS()
        
    def setExternalVal(self):
        #app.view.var.background_view = QPixmap('app/images/background_login.png').scaled(810, 801, Qt.AspectRatioMode.KeepAspectRatioByExpanding, Qt.TransformationMode.SmoothTransformation) ##4213 × 4167
        app.view.var.logo_view = QPixmap('app/images/color_logo.png').scaled(120, 75, Qt.AspectRatioMode.KeepAspectRatioByExpanding, Qt.TransformationMode.SmoothTransformation)
        
    def setStyle(self, object, css_path):
        with open(css_path,"r") as file:
            style= file.read()
            object.setStyleSheet(style)
    
    def eventButtonClickedLoginClick(self, account, password):
        try:
            if userAuthentication(account.text(), password.text()) == True:
                app.func.database.userParsing(account.text(), password.text())
                app.environment.thread = QThread()
                self.home = HomeQT()
                self.home.show()
                self.close()
            else:
                QMessageBox.critical(None, "Error", "Wrong username or password")
        except:
            if userAuthentication(account, password)== True:
                app.func.database.userParsing(account, password)
                app.environment.thread = QThread()
                self.home = HomeQT()
                self.home.show()
                self.close()
            else:
                QMessageBox.critical(None, "Error", "Wrong username or password")
    
    def eventChangePosition(self):
        self.width = self.frameGeometry().width()
        self.height = self.frameGeometry().height()

    def eventButtonClickedLoginEditClick(self):
        from app.templates.user_info import UserChange
        self.edit = UserChange()
        self.edit.show()
        
    def on_mouse_press_forgot(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.eventButtonClickedLoginEditClick()
    
    def on_mouse_press_register(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            from app.templates.user_register import UserRegister
            self.edit = UserRegister()
            self.edit.show()
    
    def keyPressEvent(self, qKeyEvent):
        if qKeyEvent.key() == 16777220 or (qKeyEvent.key() == 43):
            password = self.password.text()
            account = self.account.text()
            self.eventButtonClickedLoginClick(account, password)
    
    def initUI(self):
        self.main_layout = QVBoxLayout()

        self.label_background = QLabel()
        #self.label_background.setPixmap(app.view.var.background_view)
        self.label_background.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.label_privacy = QLabel("Privacy @2023")
        self.label_privacy.setStyleSheet("color: black")
        self.label_privacy.setAlignment(Qt.AlignmentFlag.AlignBottom)
        
        self.box = QGroupBox()
        self.box_layout = QHBoxLayout()
        self.box.setStyleSheet("background-color: transparent")
        self.box.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.box.setLayout(self.box_layout)
        
        self.layout_login = QFrame(self.box)
        self.box_layout.addWidget(self.layout_login)
        self.layout_login.setMaximumSize(350, 500)
        self.layout_login.setMinimumSize(325, 450)
        self.frame_login= QVBoxLayout()
        self.layout_login.setLayout(self.frame_login)
        
        self.bg_layout = QStackedLayout()
        self.bg_layout.setStackingMode(QStackedLayout.StackingMode.StackAll)
        self.bg_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.bg_layout.addWidget(self.label_background)
        self.bg_layout.addWidget(self.box)
        
        self.frame_entry = QVBoxLayout()
        self.frame_entry.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.frame_entry.setContentsMargins(15,10,15,50)
        
        self.label_login = QLabel()
        self.label_login.setPixmap(app.view.var.logo_view)
        self.label_login.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.label_login.setContentsMargins(0,25,0,0)
        self.frame_login.addWidget(self.label_login)
        
        self.label_account = QLabel("Username")
        self.label_account.setStyleSheet("color: black")
        self.label_account.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.frame_entry.addWidget(self.label_account)
        
        self.account = QLineEdit()
        self.account.setPlaceholderText('Enter your Username')
        self.frame_entry.addWidget(self.account)

        self.label_password = QLabel("Password")
        self.label_password.setStyleSheet("color: black;")
        self.label_password.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.frame_entry.addWidget(self.label_password)

        self.password = QLineEdit()
        self.password.setEchoMode(QLineEdit.EchoMode.Password)
        self.password.setPlaceholderText('Enter your password')
        self.frame_entry.addWidget(self.password)

        self.label_linked = QFrame()
        self.label_linked_layout = QHBoxLayout()
        self.label_linked.setLayout(self.label_linked_layout)
        self.frame_entry.addWidget(self.label_linked)
        
        self.label_forgot = QLabel("Forgot Password?")
        self.label_forgot.setStyleSheet("color: rgb(13, 13, 148);text-decoration: underline")
        self.label_forgot.setCursor(Qt.CursorShape.PointingHandCursor)
        self.label_forgot.mousePressEvent = (partial(self.on_mouse_press_forgot))
        self.label_linked_layout.addWidget(self.label_forgot)
        
        self.label_register = QLabel("Register")
        self.label_register.setStyleSheet("color: rgb(13, 13, 148);text-decoration: underline")
        self.label_register.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.label_register.setCursor(Qt.CursorShape.PointingHandCursor)
        self.label_register.mousePressEvent = (partial(self.on_mouse_press_register))
        self.label_linked_layout.addWidget(self.label_register)
        
        self.frame_login.addLayout(self.frame_entry)
        
        self.button_login = QPushButton("Sign In")
        self.button_login.setStyleSheet("color: black")
        self.button_login.clicked.connect(partial(self.eventButtonClickedLoginClick, self.account, self.password))
        self.button_login.setFixedWidth(200)
        self.frame_login.addWidget(self.button_login)
        
        self.main_layout.addLayout(self.bg_layout)
        self.main_layout.addWidget(self.label_privacy)
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setLayout(self.main_layout)
        
    def setObjectStyleCSS(self):
        self.setStyleSheet("background-color: #ececec")
        self.setStyle(self.account, "app/static/css/login/qline.css")
        self.setStyle(self.password, "app/static/css/login/qline.css")
        self.setStyle(self.box, "app/static/css/login/qgroupbox.css")
        self.setStyle(self.layout_login, "app/static/css/login/qframe.css")
        self.setStyle(self.button_login, "app/static/css/login/button.css")
        self.setStyle(self.label_background, "app/static/css/login/label.css")
        

        