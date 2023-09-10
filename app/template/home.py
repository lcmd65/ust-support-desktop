#############################################################################################################################################################################
# using NLP for processing text from audio record
# using multithreading for except threaeding (process the demon of while loop Qapplication)
# speech_recognition api
import sys
import speech_recognition as sr
import threading
import app.view.var
import app.environment
import gc
import io
import base64
import app.func.func
import app.func.database
import PIL.Image as Image
from PIL.ImageQt import ImageQt
from functools import partial
from app.func.func import audioMicroToText, speakTextThread
from PyQt6.QtWidgets import (
    QMenu,
    QHBoxLayout,
    QTreeView,
    QStyle,
    QScrollArea,
    QVBoxLayout,
    QApplication,
    QMenuBar,
    QLabel,
    QMainWindow,
    QPushButton,
    QTabWidget,
    QWidget,
    QMessageBox,
    QFrame,
    QLineEdit,
    QDialogButtonBox,
    QCommandLinkButton,
    QHeaderView,
    QAbstractItemDelegate
)
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from app.model.conversation import Conver

################################################################################################################################################################################
# QObject for Recording with multithreading while running QApplication #########################################################################################################
################################################################################################################################################################################
class VoiceWorker(QObject):
    textRecord = pyqtSignal(str)
    textReply = pyqtSignal(str)
    
    @pyqtSlot()
    def task(self):
        recognizer_engine = sr.Recognizer()
        micro_engine = sr.Microphone()
        try:
            self.textReply.emit("Say something!")
        except:
            pass
        speakTextThread("Say something!")
        try:
            with micro_engine as source:
                try:
                    audio = recognizer_engine.listen(source, phrase_time_limit= 10)
                    value = recognizer_engine.recognize_google(audio)
                    self.textRecord.emit(f"{value}")
                    self.textReply.emit(f"{value}")
                    speakTextThread(str(value))
                    self.textReply.emit("Got it! Now to recognize it...")
                    speakTextThread("Got it! Now to recognize it...")
                except sr.UnknownValueError:
                    self.textReply.emit("Oops")
                    speakTextThread("Oops")
        except Exception as e:
            print(e)

################################################################################################################################################################################
# QMainWindow Home view of Project #############################################################################################################################################
################################################################################################################################################################################
class HomeQT(QMainWindow):
    def __init__(self, parent = None):
        super().__init__()
        
        # parent & event 
        self.setWindowTitle("HCMUS Assistant")
        self.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.resize(1400, 1080)
        self.eventCreateAction()
        self.createMenuBar()
        self.eventSetExternalVal()
        self.conversation = QStandardItemModel() #model treeview tab 2 (bot)
        self.requests_user = QStandardItemModel() # model treeview tab 1
        self.conversation_shot = []
        self.conversation_model = Conver()
        self.dashboard = None # Qitem request sau khi được click
        
        # audio thread in environment variable
        self.initThreadingWorker()

        # toplevel in menu button event clicked
        self.edit_toplevel = None
        self.help_toplevel = None
        self.file_toplevel = None
        self.login_toplevel = None
        
        # ui
        self.initUI()
        self.setObjectStyleCSS()
        app.func.database.getClient()
        app.func.database.connectServer()
    
    def closeEvent(self, event):
        if event.type() == QEvent.Type.Close:
            # check if event is not a button close click
            if not event.spontaneous():
                event.ignore() # prevent the program auto exit 
            else:
                reply = QMessageBox.question(self, "Quit?", "Are you sure you want to quit?", \
                    QMessageBox.StandardButton.Yes | \
                    QMessageBox.StandardButton.No)
                if reply == QMessageBox.StandardButton.Yes:
                    event.accept()
                else:
                    event.ignore()
        else:
            event.ignore()
    
    def keyPressEvent(self, qKeyEvent):
            if qKeyEvent.key() == 16777220 or (qKeyEvent.key() == 43):
                text = self.nohcel_conversation_entry.text()
                self.conversation_model.addConver(text)
                if self.conversation_model.score[self.conversation_model.length-1] >= 60:
                    text_output = self.conversation_model.getConver()
                else:
                    text_output = self.eventHomeProcessingLLM(text)
                self.eventInitLabelConversation(text, text_output)
                
    def eventInitLabelConversation(self, text, text_output):
        self.conversation_shot.append([None for _ in range (2)])
        index = len(self.conversation_shot)-1
        
        self.conversation_shot[index][0] = QLabel() 
        self.nohcel_conversation_view_layout.addWidget(self.conversation_shot[index][0])
        self.conversation_shot[index][0].setText(text)
        self.conversation_shot[index][0].setWordWrap(True)
        self.setStyle(self.conversation_shot[index][0], "app/template/css/home/tab2/conversation/label_user.css")
        
        self.conversation_shot[index][1] = QLabel()
        self.nohcel_conversation_view_layout.addWidget(self.conversation_shot[index][1])
        self.conversation_shot[index][1].setText(text_output)
        self.conversation_shot[index][1].setWordWrap(True)
        self.setStyle(self.conversation_shot[index][1], "app/template/css/home/tab2/conversation/label.css")
        
    # external variable background and icon init
    def eventSetExternalVal(self):
        app.view.var.background_view = QPixmap('app/images/background_login.png').scaled(810, 801,\
            Qt.AspectRatioMode.KeepAspectRatioByExpanding,\
            Qt.TransformationMode.SmoothTransformation) ##4213 × 4167
        app.view.var.logo_view = QPixmap('app/images/color_logo.png').scaled(80, 50, \
            Qt.AspectRatioMode.KeepAspectRatioByExpanding, \
            Qt.TransformationMode.SmoothTransformation)

    def setStyle(self, object, css_path):
        with open(css_path,"r") as file:
            style= file.read()
            object.setStyleSheet(style)
        file.close()
    
    def initThreadingWorker(self):
        app.environment.worker = VoiceWorker()
        app.environment.worker.moveToThread(app.environment.thread)
    
    def setIconButton(self, button, image_path, size):
        """Sets the icon of the button to the image at the specified path."""
        pixmap = QPixmap(image_path).scaled(size, size, \
            Qt.AspectRatioMode.KeepAspectRatioByExpanding, \
            Qt.TransformationMode.SmoothTransformation)
        icon = QIcon(pixmap)
        button.setIcon(icon)
        button.setIconSize(pixmap.rect().size())
    
    def eventButtonClickedEdit(self):
        try:     
            from app.template.edit import EditQT
            self.edit_toplevel = EditQT()
            self.edit_toplevel.show()
        except Exception as e:
            QMessageBox.critical(None, "Error", repr(e))
    
    def eventButtonClickedLogout(self):
        self.createLayoutLoginBox()
        gc.collect()

    def eventButtonClickedHelp(self):
        try:
            from app.template.help import HelpQT
            self.help_toplevel = HelpQT()
            self.help_toplevel.show()
        except Exception as e:
            QMessageBox.critical(None, "Error", repr(e))
        
    def eventButtonClickedFile(self):
        try:
            from app.template.file import FileQT
            self.file_toplevel = FileQT()
            self.file_toplevel.show()
        except Exception as e:
            QMessageBox.critical(None, "Error", repr(e))
            
    def eventHomeProcessingLLM(self, text):
        try:
            return app.func.func.processingLLM(text)
        except:
            return "Xin lỗi, bạn có thể nói rõ hơn không!" 
        
    # thử nghiệm API speech to text trên sys
    def eventButtonClickedAudioRecord(self):
        if not self.conversation:
            speakTextThread("Hi!, I am Nohcel, chat Assistant developed by VinBigdata")
        else:
            speakTextThread("How can i help you?")
        text = audioMicroToText()
        self.label_view.clear()
        self.label_view.setText(text)
        self.label_view.adjustSize() 
        item = QStandardItem(text)
        self.conversation.appendRow(item)
        self.temp_data_view.setModel(self.conversation)
        self.eventHomeProcessingLLM(text)

    def eventButtonClickedAudioRecordThread(self):
        threading_new_for_record_loop = threading.Thread(target= partial(self.eventButtonClickedAudioRecordQThread))
        threading_new_for_record_loop.daemon = True
        threading_new_for_record_loop.start()
    
    # test API speech to text trên QThread
    def eventButtonClickedAudioRecordQThread(self):
        app.environment.thread.start()
        app.environment.worker.task()
        app.environment.thread.exec()
        
    def eventCreateAction(self):
        self.file_action = QAction("&File Open", self, triggered = self.eventButtonClickedFile)
        self.edit_action = QAction("&Edit Param", self, triggered= self.eventButtonClickedEdit)
        self.help_action = QAction("$Help Infor", self, triggered= self.eventButtonClickedHelp)
        self.login_action = QAction("&Use other Account", self, triggered= self.eventButtonClickedLogout)

    def createLayoutLoginBox(self):
        # circle import for run login view again from home view
        try:
            from app.template.login import LoginUIQT
            self.login_toplevel = LoginUIQT()
            self.login_toplevel.show()
            self.close()    
        except Exception as e:
            QMessageBox.critical(None, "Error", repr(e))
    
    def createMenuBar(self):
        # Memu
        self.menu_bar = QMenuBar()
        self.file_menu = self.menu_bar.addMenu("&File")
        self.edit_menu = self.menu_bar.addMenu("&Edit")
        self.help_menu = self.menu_bar.addMenu("&Help")
        self.login_menu = self.menu_bar.addMenu("&Exit")
        self.file_menu.addAction(self.file_action)
        self.edit_menu.addAction(self.edit_action)
        self.help_menu.addAction(self.help_action)
        self.login_menu.addAction(self.login_action)
    
    def eventRequestTreeClicked(self, index):
        for i in reversed(range(self.hcmus_request_frame_layout.count())): 
            self.hcmus_request_frame_layout.itemAt(i).widget().deleteLater()
        item = self.requests_user.itemFromIndex(index)
        for request in  app.environment.User_info.requests:
            if str(request["subject"]) == item.text():
                self.dashboard = request
        subject = QLabel()
        subject.setStyleSheet("font-size: 30px;")
        subject.setText(self.dashboard["subject"])
        label_request = QLabel()
        label_request.setText("".join(["Request :", self.dashboard["request"]]))
        label_request.setWordWrap(True)
        label_respone = QLabel()
        label_respone.setText("".join(["Respone :", self.dashboard["respone"]]))
        label_respone.setWordWrap(True)
        
        self.setStyle(label_request, "app/template/css/home/tab1/label_request.css")
        self.setStyle(label_respone, "app/template/css/home/tab1/label_request.css")
        self.hcmus_request_frame_layout.addWidget(subject)
        self.hcmus_request_frame_layout.addWidget(label_request)
        self.hcmus_request_frame_layout.addWidget(label_respone)
        
    def eventButtonClickedUserSetting(self):
        pass
    
    def eventButtonClickedExitSetting(self):
        pass
    
    def eventButtonClickedSystemSetting(self):
        pass
    
    def initRequest(self, subject_text, request_text):
        text1 = subject_text.text()
        text2 = request_text.text()
        document = app.func.database.pushRequestToMongo(app.environment.User_info.id, text1, text2)
        QMessageBox.critical(None, "Message", repr("Success"))
        for i in reversed(range(self.hcmus_request_frame_layout.count())): 
            self.hcmus_request_frame_layout.itemAt(i).widget().deleteLater()
        self.button_request_init.deleteLater()
        self.hcmus_request_tree
        self.requests_user.invisibleRootItem().appendRow(QStandardItem(str(document["subject"])))
        app.environment.User_info.updateRequest()
            
    def eventButtonClickedInitRequest(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            try:
                self.button_request_init.deleteLater()
            except:
                pass
            for i in reversed(range(self.hcmus_request_frame_layout.count())): 
                self.hcmus_request_frame_layout.itemAt(i).widget().deleteLater()
            line_subject = QLineEdit()
            line_subject.setPlaceholderText("Chủ đề")
            line_request = QLineEdit()
            line_request.setPlaceholderText("Nhập Câu hỏi tại đây")
            self.button_request_init = QPushButton("Ok")
            self.button_request_init.clicked.connect(partial(self.initRequest,line_subject, line_request))
            self.setStyle(line_request, "app/template/css/home/tab1/line_init_request.css")
            self.setStyle(line_subject, "app/template/css/home/tab1/line_init_subject.css")
            self.hcmus_request_frame_layout.addWidget(line_subject)
            self.hcmus_request_frame_layout.addWidget(line_request)
            self.hcmus_frame_layout.addWidget(self.button_request_init)
                
            
    def initUI(self): # Interface component init 
        # Label & Logo
        self.label_background = QLabel()
        self.label_background.setPixmap(app.view.var.background_view)
        self.label_background.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.label_privacy = QLabel("Privacy @2023")
        self.label_privacy.setStyleSheet("color: black")
        self.label_privacy.setAlignment(Qt.AlignmentFlag.AlignBottom)
        
        # Tab 
        self.tabs = QTabWidget()
        self.tabs.setTabPosition(QTabWidget.TabPosition.North)
        self.tabs.setTabShape(QTabWidget.TabShape.Rounded)
        self.tabs.setMovable(True)
        
        # Tab 0
        self.hcmus_request = QWidget()
        self.hcmus_request_layout = QVBoxLayout()
        self.hcmus_request_main_layout = QHBoxLayout()
        self.hcmus_request.setLayout(self.hcmus_request_layout)
        
        self.hcmus_request_user = QLabel()
        self.hcmus_request_user.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.hcmus_request_user_avatar = QLabel()
        self.hcmus_request_user_avatar.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.hcmus_request_user_name = QLabel()
        self.hcmus_request_user_name.setAlignment(Qt.AlignmentFlag.AlignLeft)
        
        image =  ImageQt(Image.open(io.BytesIO(base64.b64decode(app.environment.User_info.image))))
        self.label_user_image = QPixmap.fromImage(image).scaled(80, 80, Qt.AspectRatioMode.KeepAspectRatioByExpanding,\
            Qt.TransformationMode.SmoothTransformation)
        self.hcmus_request_user_name.setText(app.environment.User_info.username)
        self.hcmus_request_user_avatar.setPixmap(self.label_user_image)
        
        self.button_setting = QPushButton()
        self.setIconButton(self.button_setting, "app/images/icons/settings.png", 30)
        self.button_setting_exit = QAction("Exit", triggered = self.eventButtonClickedExitSetting)
        self.button_setting_edit_information = QAction("User Information", triggered = self.eventButtonClickedUserSetting)
        self.button_setting_edit_system = QAction("Settings", triggered = self.eventButtonClickedSystemSetting)
        self.button_setting_menu = QMenu()
        self.button_setting_menu.addAction(self.button_setting_exit)
        self.button_setting_menu.addAction(self.button_setting_edit_information)
        self.button_setting_menu.addAction(self.button_setting_edit_system)
        self.button_setting.setMenu(self.button_setting_menu)
        
        self.hcmus_request_user_layout = QHBoxLayout()
        self.hcmus_request_user.setLayout(self.hcmus_request_user_layout)
        self.hcmus_request_user_layout.addWidget(self.hcmus_request_user_avatar)
        self.hcmus_request_user_layout.addWidget(self.hcmus_request_user_name)
        self.hcmus_request_user_layout.addWidget(self.button_setting)
        
        self.hcmus_request_layout.addWidget(self.hcmus_request_user)
        self.hcmus_request_layout.addLayout(self.hcmus_request_main_layout)
        
        self.hcmus_request_tree = QTreeView()
        self.hcmus_request_tree.setHeaderHidden(False)
        self.requests_user.setHorizontalHeaderLabels(["Câu hỏi"])
        font = QFont()
        font.setPointSize(20)
        self.hcmus_request_tree.header().setFont(font)
        self.hcmus_request_tree.setMinimumWidth(150)
        self.hcmus_request_tree.setMaximumWidth(250)
        self.hcmus_request_tree.setUpdatesEnabled(True)
        self.hcmus_request_tree.setModel(self.requests_user)
        self.hcmus_request_tree.clicked.connect(self.eventRequestTreeClicked)
        for item in app.environment.User_info.requests:
            self.requests_user.invisibleRootItem().appendRow(QStandardItem(str(item["subject"])))
        self.hcmus_request_main_layout.addWidget(self.hcmus_request_tree)
        
        self.hcmus_frame = QFrame()
        self.hcmus_frame_layout = QVBoxLayout()
        self.hcmus_frame.setLayout(self.hcmus_frame_layout)
        
        self.hcmus_function_button_bar = QFrame()
        self.hcmus_function_button_bar.setStyleSheet("padding-top:0;")
        self.hcmus_function_button_bar .setMaximumHeight(50)
        self.hcmus_function_button_bar_layout = QHBoxLayout()
        self.hcmus_function_button_bar_layout.setAlignment(Qt.AlignmentFlag.AlignTop|Qt.AlignmentFlag.AlignRight)
        self.hcmus_function_button_bar.setLayout(self.hcmus_function_button_bar_layout)
        self.hcmus_frame_layout.addWidget(self.hcmus_function_button_bar)
        
        self.init_request_button = QLabel("Tạo Câu hỏi")
        self.init_request_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.init_request_button.mousePressEvent = (self.eventButtonClickedInitRequest)
        self.init_request_button.setMaximumWidth(200)
        self.hcmus_function_button_bar_layout.addWidget(self.init_request_button)
        
        self.hcmus_request_frame = QFrame()
        self.hcmus_request_frame_layout = QVBoxLayout()
        self.hcmus_request_frame_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.hcmus_request_frame.setLayout(self.hcmus_request_frame_layout)
        self.hcmus_frame_layout.addWidget(self.hcmus_request_frame)
        self.hcmus_request_main_layout.addWidget(self.hcmus_frame)
        
        # Tab 1
        self.nohcel = QWidget()
        self.nohcel_layout = QVBoxLayout()
        self.nohcel_main_layout = QHBoxLayout()
        self.nohcel_layout.addLayout(self.nohcel_main_layout)

        self.audio_record = QWidget()
        self.audio_layout = QHBoxLayout()
        
        for tab,  name in zip([self.hcmus_request, self.nohcel, self.audio_record], ["HCMUS Chat" ,"NOHCEL BOT", "Speech to Text"]):
            self.tabs.addTab(tab, name)

        self.data_view = QTreeView()
        self.data_view.setMinimumWidth(150)
        self.data_view.setMaximumWidth(250)
        self.nohcel_main_layout.addWidget(self.data_view)
        
        self.nohcel_frame = QFrame()
        self.nohcel_frame_layout = QVBoxLayout()
        self.nohcel_frame.setLayout(self.nohcel_frame_layout)
        self.nohcel_main_layout.addWidget(self.nohcel_frame)
        
        self.nohcel_conversation_area = QScrollArea()
        self.nohcel_conversation_area.setWidgetResizable(True)
        
        self.nohcel_conversation_view = QLabel()
        self.nohcel_conversation_area.setWidget(self.nohcel_conversation_view )
        self.nohcel_conversation_view_layout = QVBoxLayout()
        self.nohcel_conversation_view.setLayout(self.nohcel_conversation_view_layout)
        self.nohcel_frame_layout.addWidget(self.nohcel_conversation_area)
        
        self.nohcel_conversation_entry = QLineEdit()
        self.nohcel_conversation_entry.setPlaceholderText("Nhập câu lệnh tại đây")
        self.nohcel_frame_layout.addWidget(self.nohcel_conversation_entry)
        
        self.audio_record.setLayout(self.audio_layout)
        self.temp_data_view = QTreeView()
        self.temp_data_view.setMinimumWidth(150)
        self.temp_data_view.setMaximumWidth(250)
        self.temp_data_view.setUpdatesEnabled(True)
        self.temp_data_view.setModel(self.conversation)
        self.audio_layout.addWidget(self.temp_data_view)
        
        self.temp_frame = QFrame()
        self.temp_frame_layout = QVBoxLayout()
        self.temp_frame.setLayout(self.temp_frame_layout)
        self.audio_layout.addWidget(self.temp_frame)
        
        self.label_temp_frame = QFrame()
        self.label_temp_frame.setObjectName("label")
        self.label_temp_frame_layout = QVBoxLayout()
        self.label_temp_frame_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.label_temp_frame.setLayout(self.label_temp_frame_layout)
        self.temp_frame_layout.addWidget(self.label_temp_frame)
        
        self.label_view = QLabel()
        self.label_view.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.label_temp_frame_layout.addWidget(self.label_view)
        app.environment.worker.textRecord.connect(lambda textRecord: self.label_view.setText(textRecord))
        
        self.audio_temp_frame = QFrame()
        self.audio_temp_frame_layout = QVBoxLayout()
        self.audio_temp_frame_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.audio_temp_frame.setLayout(self.audio_temp_frame_layout)
        self.temp_frame_layout.addWidget(self.audio_temp_frame)
        
        self.label_temp_input_frame = QFrame()
        self.label_temp_input_frame.setObjectName("label")
        self.label_temp_input_frame_layout = QVBoxLayout()
        self.label_temp_input_frame_layout.setAlignment(Qt.AlignmentFlag.AlignBottom)
        self.label_temp_input_frame.setLayout(self.label_temp_input_frame_layout)
        self.temp_frame_layout.addWidget(self.label_temp_input_frame)
        
        self.label_input = QLabel()
        self.label_input.setAlignment(Qt.AlignmentFlag.AlignBottom)
        self.label_temp_input_frame_layout.addWidget(self.label_input)
        app.environment.worker.textReply.connect(lambda textReply: self.label_view.setText(textReply))
        
        self.button_record = QPushButton()
        self.button_record.clicked.connect(self.eventButtonClickedAudioRecordQThread)
        self.setIconButton(self.button_record, 'app/images/icons/microphone.png', 50)
        self.audio_temp_frame_layout.addWidget(self.button_record)
        self.audio_temp_frame_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.nohcel_layout.addWidget(self.menu_bar)
        self.nohcel_layout.addWidget(self.label_privacy)
        self.audio_layout.addWidget(self.label_privacy)
        self.nohcel.setLayout(self.nohcel_layout)
        self.setCentralWidget(self.tabs)
    
    # style css setting for all object of home page
    def setObjectStyleCSS(self):
        self.setStyleSheet("background-color: #ececec")
        self.setStyle(self.tabs, "app/template/css/home/tab.css")
        
        self.setStyle(self.hcmus_request_user, "app/template/css/home/tab1/label_user.css")
        self.setStyle(self.hcmus_request_user_avatar, "app/template/css/home/tab1/label_avatar.css")
        self.setStyle(self.hcmus_request_user_name, "app/template/css/home/tab1/label_username.css")
        self.setStyle(self.button_setting, "app/template/css/home/tab1/setting_button.css")
        self.setStyle(self.hcmus_request_tree, "app/template/css/home/tab1/tree.css")
        self.setStyle(self.init_request_button, "app/template/css/home/tab1/label_init_request.css")
        
        self.setStyle(self.data_view, "app/template/css/home/tab2/tree.css")
        self.setStyle(self.nohcel_frame, "app/template/css/home/tab2/frame.css")
        self.setStyle(self.nohcel_conversation_view, "app/template/css/home/tab2/qlabel_conv.css")
        self.setStyle(self.nohcel_conversation_entry, "app/template/css/home/tab2/qline_conv.css")
        
        self.setStyle(self.temp_data_view, 'app/template/css/home/tab3/qframe.css')
        self.setStyle(self.button_record, "app/template/css/home/tab3/button.css")
        self.setStyle(self.label_view,  "app/template/css/home/tab3/label.css")
        self.setStyle(self.label_input,  "app/template/css/home/tab3/label.css")
        self.setStyle(self.label_temp_input_frame, 'app/template/css/home/tab3/qframe.css')
        self.setStyle(self.label_temp_frame, 'app/template/css/home/tab3/qframe.css')

# python3 app/template/home.py