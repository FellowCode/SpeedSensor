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

    sens_dist = 500

    speed_list = []

    cur_speed_index = -1

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
            f.write(str(self.com_num) + '\n')
            f.write(self.sensor_dist.get())
            f.close()
        except:
            print('save params error')

    def load_params(self):
        try:
            f = open(appdata_path + 'settings.txt')
            self.com_num = int(f.readline())
            self.sens_dist = int(f.readline())
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

        self.com_label = Label(text='Dist', font=("Courier", 11))
        self.com_label.place(x=10, y=34)

        self.sensor_dist = StringVar()
        self.sens_dist_entry = Entry(textvariable=self.sensor_dist, font=("Courier", 11))
        self.sens_dist_entry.place(x=50, y=35, width=40)
        self.sensor_dist.set(self.sens_dist)

        self.conn_button = Button(text='Connect', font=("Calibri", 9), width=10)
        self.conn_button.bind('<ButtonRelease-1>', lambda event: self.connect())
        self.conn_button.place(x=90, y=2)

        self.conn_label = Label(text='Connection:', font=("Courier", 11), width=130)
        self.conn_label.place(x=200, y=5, width=180)

        self.canvas = Canvas(self.conn_label, width=50, height=20)
        self.canvas.place(x=148, y=0)

        self.conn_button = Button(text='<', font=("Calibri", 12), width=2)
        self.conn_button.bind('<ButtonRelease-1>', lambda event: self.prev_speed())
        self.conn_button.place(x=10, y=65)

        self.speed_label = Label(text='Speed: None', font=("Courier", 26))
        self.speed_label.place(relx=0.1, y=60, relwidth=0.8)

        self.conn_button = Button(text='>', font=("Calibri", 12), width=2)
        self.conn_button.bind('<ButtonRelease-1>', lambda event: self.next_speed())
        self.conn_button.place(x=365, y=65)

        self.page_label = Label(text='', font=("Courier", 11))
        self.page_label.place(x=170, y=100)

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

    def prev_speed(self):
        if len(self.speed_list) == 0:
            return
        if self.cur_speed_index > 0:
            self.cur_speed_index -= 1
        speed = str(self.speed_list[self.cur_speed_index])
        try:
            speed1 = str(speed)[:str(speed).find('.') + 3]
        except:
            speed1 = str(speed)
        self.speed_label['text'] = 'Speed: ' + speed1 + 'm/s'
        self.page_label['text'] = 'Page ' + str(self.cur_speed_index - len(self.speed_list) + 1)

    def next_speed(self):
        if len(self.speed_list) == 0:
            return
        if self.cur_speed_index < len(self.speed_list)-1:
            self.cur_speed_index += 1
        speed = str(self.speed_list[self.cur_speed_index])
        try:
            speed1 = str(speed)[:str(speed).find('.') + 3]
        except:
            speed1 = str(speed)
        self.speed_label['text'] = 'Speed: ' + speed1 + 'm/s'
        self.page_label['text'] = 'Page ' + str(self.cur_speed_index - len(self.speed_list) + 1)
        if self.cur_speed_index - len(self.speed_list) == -1:
            self.page_label['text'] = ''

    def setSpeed(self, value):
        between_sensors = int(self.sensor_dist.get()) / 1000
        time = value / 1000
        speed = between_sensors / time
        self.speed_list.append(speed)

        self.cur_speed_index = len(self.speed_list)-1
        try:
            speed1 = str(speed)[:str(speed).find('.')+3]
        except:
            speed1 = str(speed)
        self.speed_label['text'] = 'Speed: ' + speed1 + 'm/s'
        self.page_label['text'] = ''

    def setCOMport(self, value):
        self.com_label['text'] = 'COM' + str(value)

if __name__ == '__main__':
    root = Tk()
    app = SpeedSensorApp(root)
    root.mainloop()