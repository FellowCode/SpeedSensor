from ctypes import windll
import os

from tkinter import *

from ser import SerialRead

user32 = windll.user32
user32.SetProcessDPIAware()

appdata_path = os.getenv('APPDATA') + '\\SpeedSensor\\'
if not os.path.exists(appdata_path):
    os.makedirs(appdata_path)

class SpeedSensorApp:
    com_num = 5

    def __init__(self, master):
        self.master = master
        self.frame = Frame(self.master)

        self.master.title("Speed Sensor")
        self.master.iconbitmap("icon.ico")

        self.frame.title = 'SpeedSensor'
        self.master.geometry('400x130+500+600')
        self.master.resizable(False, False)

        self.load_params()

        self.setupUI()

        self.connect()

    def save_params(self):
        try:
            f = open(appdata_path + 'settings.txt', 'w')
            f.write(str(self.com_num))
            f.close()
        except:
            print('save params error')

    def load_params(self):
        try:
            f = open(appdata_path + 'settings.txt')
            self.com_num = int(f.readline())
            f.close()
        except:
            print('load params error')

    def setupUI(self):
        self.com_label = Label(text='COM', font=("Courier", 11))
        self.com_label.place(x=10, y=6)

        self.com_text = StringVar()
        self.com_entry = Entry(textvariable=self.com_text, font=("Courier", 11))
        self.com_entry.place(x=50, y=7, width=30)
        self.com_text.set(str(self.com_num))

        self.conn_button = Button(text='Connect', font=("Calibri", 9), width=10)
        self.conn_button.bind('<ButtonRelease-1>', lambda event: self.connect())
        self.conn_button.place(x=90, y=2)

        self.conn_label = Label(text='Connection:', font=("Courier", 11), width=130)
        self.conn_label.place(x=200, y=5, width=180)

        self.canvas = Canvas(self.conn_label, width=50, height=20)
        self.canvas.place(x=148, y=0)

        self.speed_label = Label(text='Speed: None', font=("Courier", 26))
        self.speed_label.place(relx=0.05, y=60, relwidth=0.9)

    def connect(self):
        self.com_num = int(self.com_text.get())
        self.save_params()
        if hasattr(self, 'reader'):
            self.reader.close_serial()
        self.reader = SerialRead(self.com_num, self)
        self.reader.start()

    def setConnectionStatus(self, status):
        if status == 1:
            color = 'green'
        else:
            color = 'red'
        self.canvas.create_oval(2, 3, 18, 19, fill=color)

    def setSpeed(self, value):
        between_sensors = 63 / 1000
        time = value / 1000
        speed = between_sensors / time
        try:
            speed1 = str(speed)[:str(speed).find('.')+3]
        except:
            speed1 = str(speed)
        self.speed_label['text'] = 'Speed: ' + speed1 + 'm/s'

    def setCOMport(self, value):
        self.com_label['text'] = 'COM' + str(value)

if __name__ == '__main__':
    root = Tk()
    app = SpeedSensorApp(root)
    root.mainloop()