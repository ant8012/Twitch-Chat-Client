import socket
import re
import sys
import subprocess
from twitch import *
from settings import *
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtNetwork import *

BUFFER_LENGTH = 4096 # buffer for message size

# regex for parsing various messages
PRIVMSG = re.compile(":(?P<name>.*)!.* (?P<type>PRIVMSG) #(?P<target>.*?) :(?P<message>.*)")
NOTICE = re.compile(":tmi.twitch.tv NOTICE [*]")
PING = re.compile("PING")
CONNECT= re.compile(":tmi.twitch.tv 001")
COLOR = re.compile(":jtv PRIVMSG.*:(?P<type>USERCOLOR)(?P<user>.*) #(?P<color>.*)")
INVALID = re.compile("\W")

# main
class Form(QMainWindow):

    # initialize custom signals
    success = pyqtSignal()
    fail = pyqtSignal()
    messageWritten = pyqtSignal()

    def __init__(self, parent=None):
        super(Form, self).__init__(parent)
        self.ui = Ui_mainWindow()
        self.ui.setupUi(self)
        self.ui.actionLogout.setEnabled(False)
         
        self.authenticate = False #if the user has not logged in yet
        self.getStreamName = False #if currently in "change stream" mode
        self.messageCount = 0 #number of messages printed on screen      
        self.streamProcess = None #if a livestreamer instance is running
        self.streamOn = False #if a stream to be open on startup is desired

        self.user_data = QSettings("twitch_irc", "twitch_irc") # get user settings

        self.user = ""
        self.password = ""
        self.stream = ""

        # various signals
        self.success.connect(self.login_success) #on successful client login to twitch
        self.fail.connect(self.disconnect) #on unsuccessful client login to twitch
        self.messageWritten.connect(self.maxMessageCheck) #on any message written to the screen
        # various socket signals
        self.clientSocket = QTcpSocket()
        self.clientSocket.connected.connect(self.login) 
        self.clientSocket.readyRead.connect(self.recieve_message)
        self.clientSocket.disconnected.connect(self.disconnect)
        
        self.setWindowTitle("Twitch chat")

        # various ui signals
        self.ui.actionLogin.triggered.connect(self.connect) #on 'Login'
        self.ui.actionLogout.triggered.connect(self.disconnect) #on 'Discconect'
        self.ui.actionSettings.triggered.connect(self.settings_panel) #on 'Settings'
        self.ui.actionchangeStream.triggered.connect(self.get_stream) #on 'change Stream'
        self.ui.actionExit.triggered.connect(self.close) #on 'Exit'         
        self.ui.chat_box.returnPressed.connect(self.get_input) #on user entering text
        self.ui.actionClearScreen.triggered.connect(self.clearScreen) #on 'Clear Screen'
        self.ui.actionOpenCloseStream.triggered.connect(self.openCloseStream) # on 'Open/Close Stream'

        if str(self.user_data.value("loginOnStartup", "").toString()) == "True":
            pass
            #self.connect()

    # on applicaiton close disconnect
    def closeEvent(self, event):
        self.disconnect()        
        event.accept()
        
    # connect to twitch
    def connect(self):
        # get user info from settings
        self.user = str(self.user_data.value("username", "").toString())
        self.password = str(self.user_data.value("password","").toString())
     
        # on bad info print error else connect socket to Twitch
        if not self.user or not self.password:
            self.ui.displayBox("Missing information, please add information via settings \n")
            self.messageWritten.emit()
        else:        
            self.ui.actionLogin.setEnabled(False)
            self.ui.actionLogout.setEnabled(True)
            self.clientSocket.connectToHost(SERVER, PORT)

    # disconnect from twitch
    def disconnect(self):
        # disconnect socket if active
        if self.clientSocket.state() != 0:
            self.clientSocket.disconnectFromHost()
            self.ui.displayBox.append("Disconnected from host \n")  
            self.messageWritten.emit()
        # close livestreamer if open
        if self.streamProcess is not None:
            self.ui.actionOpenCloseStream.setEnabled(False)
            self.streamProcess.terminate()
            self.streamProcess.wait()
            self.streamProcess = None
        # reset various variables
        self.authenticate = False
        self.ui.actionLogin.setEnabled(True)
        self.ui.actionLogout.setEnabled(False)
        self.ui.actionchangeStream.setEnabled(False)
        self.ui.chat_box.setEnabled(False)

    # on connection login with client info
    def login(self):
        self.ui.displayBox.append("Connected to host \n")   
        self.messageWritten.emit()
        self.clientSocket.write("PASS " + self.password + "\r\n")
        self.clientSocket.write("NICK " + self.user + "\r\n")           
        self.clientSocket.write("TWITCHCLIENT 2 \r\n")
         
    # on successful login get stream name
    def login_success(self):
        # read stream name if stream startup is true
        if str(self.user_data.value("streamOnStartup", "").toString()) == "True": 
            self.stream = str(self.user_data.value("stream","").toString())
        # set menu items to active
        self.ui.actionchangeStream.setEnabled(True)
        self.ui.chat_box.setEnabled(True)
        self.ui.actionOpenCloseStream.setEnabled(True)
        # connect to stream
        if self.stream:
            self.goto_stream("")            
    
    # read input from twitch
    def recieve_message(self):   
        while self.clientSocket.bytesAvailable():
            message = self.clientSocket.readLine()  
            self.print_message(self.parse_message(message))
    
    # parse twitch message
    def parse_message(self, message):
        parsed_message = PRIVMSG.match(message)
        # message of type user
        if parsed_message:
            return { "type": "privsmg", 
                "name": parsed_message.group("name"), 
                "target": parsed_message.group("target"), 
                "message": parsed_message.group("message")
            }
        # message of type ping
        parsed_message = PING.match(message)
        if parsed_message:
            return {"type": "ping"}
        # message of type twitch server, check for login authorized message
        if not self.authenticate: 
            parsed_message = NOTICE.match(message)
            if parsed_message:
                return {"type": "notice",
                        "message": "login failed, inccorect username/password"
                }
            parsed_message = CONNECT.match(message)
            if parsed_message:
                return {"type": "logged in",
                        "message": "login successful"
                }       
        
        return { "type": "unkown",
                "message": message }

    # print message to ui
    def print_message(self, message):
        test = QString()
        # print based on type from parse message
        if message["type"] == "privsmg":

            test = QString(message["name"] + ": " + message["message"] + "\n")
                    
        elif message["type"] == "ping":
            test = self.clientSocket.write("PONG \r\n")
            test = QString("PONG SENT")
        elif message["type"] == "notice":
            test = QString("Login Failed \n")
            self.fail.emit()
        elif message["type"] == "logged in":
            test = QString("Login Successful \n")
            self.authenticate = True
            self.success.emit()           
        else:
            pass
            #print(message["message"])
        if test:
            self.ui.displayBox.append(test)
            #print(test)
            self.messageWritten.emit() 
    
    # checks if number of messages on screen exceeds limit
    def maxMessageCheck(self):
        self.messageCount += 1
        # if so remove top line
        if self.messageCount >= 200:        
            cursor = self.ui.displayBox.textCursor()
            cursor.movePosition(1,0)
            cursor.movePosition(12,1,2)

            cursor.removeSelectedText()
            self.messageCount -= 1

    # clear the screen
    def clearScreen(self):
        self.ui.displayBox.clear()
        self.messageCount = 0  

    # set get Stream mode
    def get_stream(self):
        if(self.getStreamName):
            self.ui.actionchangeStream.setText("Change stream")
            self.getStreamName = False
            self.ui.chat_box.setPlaceholderText("")
        else:
            self.ui.actionchangeStream.setText("Cancel change stream")
            self.ui.chat_box.setPlaceholderText("Type the name of the stream")
            self.getStreamName = True

    # goto new stream room
    def goto_stream(self, newStream):
        # send message to twitch to disconnect/connect to stream
        if newStream:
            self.ui.displayBox.append("Leaving Stream \n")
            self.messageWritten.emit()
            self.clientSocket.write("PART #" + self.stream + "\r\n")
            self.stream = newStream
        self.ui.displayBox.append("Entering Stream \n")
        self.messageWritten.emit()
        self.clientSocket.write("JOIN #" + self.stream + "\r\n")
        
        # close livestreamer if active
        if self.streamProcess is not None:
            self.ui.actionOpenCloseStream.setEnabled(False)
            self.streamProcess.terminate()   
            self.streamProcess.wait()              
        
        # open livestreamer
        self.streamProcess = subprocess.Popen(['/usr/local/bin/livestreamer','twitch.tv/' + self.stream,'best'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False)
        # set menu item if livestreamer is open
        if self.streamProcess:
            self.ui.actionOpenCloseStream.setEnabled(True)
            self.streamOn = True   
             
    # open or close live streamer
    def openCloseStream(self):
        if self.streamOn:
            self.ui.actionOpenCloseStream.setEnabled(False)
            self.streamProcess.terminate()   
            self.streamProcess.wait()
            self.streamOn = False
            self.ui.actionOpenCloseStream.setEnabled(True)
            self.streamProcess = None 
        else:
            self.streamProcess = subprocess.Popen(['/usr/local/bin/livestreamer','twitch.tv/' + self.stream,'best'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False)
            self.streamOn = True         
            
    # reads input from user, catagoarizes type
    def get_input(self):
        # if in change stream mode, get stream
        if self.getStreamName:
            newStream = str(self.ui.chat_box.text())                        
            if newStream:
                self.goto_stream(newStream)
                self.ui.actionchangeStream.setText("Change stream")
                self.ui.chat_box.setPlaceholderText("") 
                self.getStreamName = False
            else:
                self.ui.displayBox.append("No stream name entered")
                self.messageWritten.emit()
        # else its a message
        else:
            message = str(self.ui.chat_box.text())
            if message:
                self.ui.displayBox.append(self.user + ": " + message + "\n")
                self.messageWritten.emit()
            #send message            
        self.ui.chat_box.clear()

    # initiazlies settings window
    def settings_panel(self):
        panel = Settings(self.user_data)
        panel.setModal(True)
        panel.exec_()

# class from settings window
class Settings(QDialog):
    def __init__(self, user_data, parent=None):
        super(Settings, self).__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.user_data = user_data
        # set user data previously entered
        self.ui.username.setText(self.user_data.value("username", "").toString())
        self.ui.password.setText(self.user_data.value("password","").toString())
        self.ui.stream.setText(self.user_data.value("stream","").toString())
        
        # set signals for check mark items
        self.ui.streamcheckBox.toggled.connect(self.streamStartup)
        self.ui.autoLogin.toggled.connect(self.startLogin)
        self.ui.cancel.clicked.connect(self.close)
        self.ui.apply_settings.clicked.connect(self.getData)

        if self.user_data.value("streamOnStartup", "").toString():
            self.ui.streamcheckBox.setChecked(True)
        else:
            self.ui.streamcheckBox.setChecked(False)

        if self.user_data.value("loginOnStartup", "").toString():
            self.ui.autoLogin.setChecked(True)
        else:
            self.ui.autoLogin.setChecked(False)

        self.streamStartup()

    # initialize values based on previous user input
    def getData(self):
        invalid = False
        # check fro invalid usernames/streams
        if not self.ui.username.text() or re.findall('\W', str(self.ui.username.text())):
            self.ui.username.clear()
            self.ui.username.setPlaceholderText("invalid username")           
            invalid = True
        if re.findall('\W', str(self.ui.stream.text())):
            self.ui.stream.clear()
            self.ui.stream.setPlaceholderText("invalid stream")
            invalid = True

        if invalid:
            return
        
        # save user data
        self.user_data.setValue("username", self.ui.username.text())
        self.user_data.setValue("password", self.ui.password.text())
        self.user_data.setValue("stream", self.ui.stream.text())

        if self.ui.streamcheckBox.isChecked():
            self.user_data.setValue("streamOnStartup", "True")
        else:            
            self.user_data.setValue("streamOnStartup", "")
        if self.ui.autoLogin.isChecked():
            self.user_data.setValue("loginOnStartup", "True")
        else:
            self.user_data.setValue("loginOnStartup", "")

        self.close()

        
    # set the checkbox on stream start up based on previous user settings
    def streamStartup(self):
        if self.ui.streamcheckBox.isChecked():
            self.ui.stream.setEnabled(True)
        else:
            self.ui.stream.setEnabled(False)

    # set the checkbox on login on startup based on previous user settings
    def startLogin(self):
        if self.ui.autoLogin.isChecked():
            self.ui.stream.setEnabled(True)
        else:
            self.ui.stream.setEnabled(False)
  
# initialize and run the application          
if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    form = Form()
    form.show()
    app.exec_()

    
