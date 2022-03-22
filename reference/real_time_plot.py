
import time
import pyqtgraph as pg
from pyqtgraph.Qt import QtGui, QtCore
import serial.tools.list_ports
import numpy as np
import sys
import math

def euler_from_quaternion(x, y, z, w):
    t0 = +2.0 * (w * x + y * z)
    t1 = +1.0 - 2.0 * (x * x + y * y)
    roll_x = math.atan2(t0, t1)
    
    t2 = +2.0 * (w * y - z * x)
    t2 = +1.0 if t2 > +1.0 else t2
    t2 = -1.0 if t2 < -1.0 else t2
    pitch_y = math.asin(t2)
    
    t3 = +2.0 * (w * z + x * y)
    t4 = +1.0 - 2.0 * (y * y + z * z)
    yaw_z = math.atan2(t3, t4)
    
    return roll_x, pitch_y, yaw_z # in radians


class Graph:
    def __init__(self, ):
        size_of_graph = 1000
        self.curve1_plot = [0]*size_of_graph
        self.curve2_plot = [0]*size_of_graph
        self.curve3_plot = [0]*size_of_graph
        self.curve4_plot = [0]*size_of_graph
        self.t = [0]*size_of_graph

        # Connect to the server
        calib = False

        self.addresses = [1,2,3,4,5,6,7,8]

        # Command the IMUs are to perform
        command = [255, 255, 255, 255, 255, 255, 255, 255]
        command[0] = 0
        command[1] = 41
        command[2] = 255
        command[3] = 255
        command[4] = 255
        command[5] = 255
        command[6] = 255
        command[7] = 255

        # Find and open serial port for the IMU dongle
        a = serial.tools.list_ports.comports()
        for w in a:
            print("\tPort:", w.device, "\tSerial#:", w.serial_number, "\tDesc:", w.description, 'PID', w.pid)
            if w.pid == 4128: # small IMU dongle
                portIMU = w.device
        # portIMU = '/dev/tty.usbmodem14101' # rPi
        self.serial_port = serial.Serial(port=portIMU, baudrate=115200, timeout=0.01)
        time.sleep(0.1)
        self.serial_port.flush()
        self.serial_port.flushInput()
        self.serial_port.flushOutput()
        time.sleep(0.1)


        # Stop streaming
        for i in range(len(self.addresses)):
            self.serial_port.write(('>'+str(self.addresses[i])+',86\n').encode())
            time.sleep(0.1)
            while self.serial_port.inWaiting():
                out = '>> ' + self.serial_port.read(self.serial_port.inWaiting()).decode()
            # print(out)

        # Manual flush. Might not be necessary
        while not self.serial_port.inWaiting() == 0:
            self.serial_port.read(self.serial_port.inWaiting())
            time.sleep(0.1)

        print('Starting configuration')
        # Set streaming slots
        for i in range(len(self.addresses)):
            msg = '>' + str(self.addresses[i]) + ',80,' + str(command[0]) + ',' + \
                                                    str(command[1]) + ',' + \
                                                    str(command[2]) + ',' + \
                                                    str(command[3]) + ',' + \
                                                    str(command[4]) + ',' + \
                                                    str(command[5]) + ',' + \
                                                    str(command[6]) + ',' + \
                                                    str(command[7]) + '\n'
            print(msg)
            self.serial_port.write(msg.encode())
            time.sleep(0.1)
            out = ''
            while self.serial_port.inWaiting():
                out += '>> ' + self.serial_port.read(self.serial_port.inWaiting()).decode()
            print(out)
        out = ''

        # Set mag on(1)/off(0)
        for i in range(len(self.addresses)):
            self.serial_port.write(('>'+str(self.addresses[i])+',109, 0\n').encode())
            time.sleep(0.1)
            while self.serial_port.inWaiting():
                out = '>> ' + self.serial_port.read(self.serial_port.inWaiting()).decode()

        # Gyro autocalibration
        if calib:
            for i in range(len(self.addresses)):
                self.serial_port.write(('>'+str(self.addresses[i])+',165\n').encode())
                time.sleep(0.1)
                while self.serial_port.inWaiting():
                    out = '>> ' + self.serial_port.read(self.serial_port.inWaiting()).decode()

        # Tare
        for i in range(len(self.addresses)):
            self.serial_port.write(('>'+str(self.addresses[i])+',96\n').encode())
            time.sleep(0.1)
            while self.serial_port.inWaiting():
                out = '>> ' + self.serial_port.read(self.serial_port.inWaiting()).decode()
            # print(out)

        # Start streaming
        for i in range(len(self.addresses)):
            self.serial_port.write(('>'+str(self.addresses[i])+',85\n').encode())
            time.sleep(0.1)
            while self.serial_port.inWaiting():
                out = '>> ' + self.serial_port.read(self.serial_port.inWaiting()).decode()
            # print(out)

        print('Start')

        self.start_time = time.time()

        self.app = QtGui.QApplication([])
        self.win = pg.GraphicsWindow()

        self.p1 = self.win.addPlot(colspan=2)
        self.win.nextRow()
        self.p2 = self.win.addPlot(colspan=2)
        self.win.nextRow()
        self.p3 = self.win.addPlot(colspan=2)
        self.win.nextRow()
        self.p4 = self.win.addPlot(colspan=2)

        self.curve1 = self.p1.plot()
        self.curve2 = self.p2.plot()
        self.curve3 = self.p3.plot()
        self.curve4 = self.p4.plot()

        graphUpdateSpeedMs = 10
        timer = QtCore.QTimer()#to create a thread that calls a function at intervals
        timer.timeout.connect(self.update)#the update function keeps getting called at intervals
        timer.start(graphUpdateSpeedMs)   
        QtGui.QApplication.instance().exec_()

    def update(self):
        try:
            id = 0
            bytes_to_read = self.serial_port.inWaiting()
            if bytes_to_read > 0:
                data = self.serial_port.read(bytes_to_read)
                if len(data) <= 3 or data[0] != 0:
                    return
                data2 = data.decode().replace('\r\n',' ')
                data3 = data2.split(' ')
                data3 = list(filter(None, data3))

                info = data3[0][0:3]

                id = int.from_bytes(info[1].encode(), sys.byteorder)

                quaternion = data3[0][3:]
                accel = data3[1]

                quaternion = quaternion.split(',')
                quaternion = np.array(quaternion).astype(np.float)

                accel = accel.split(',')
                accel = np.array(accel).astype(np.float)

                x = quaternion[0]
                y = quaternion[1]
                z = quaternion[2]
                w = quaternion[3]
                acc_x = accel[0]
                acc_y = accel[1]
                acc_z = accel[2]

                out = [time.time(), id, w, x, y, z, acc_x, acc_y, acc_z]
                print(out)

                euler = euler_from_quaternion(w, x, y, z)

                self.curve1_plot[0:-1] = self.curve1_plot[1:]
                self.curve1_plot[-1] = math.degrees(euler[0])
                self.curve2_plot[0:-1] = self.curve2_plot[1:]
                self.curve2_plot[-1] = math.degrees(euler[1])
                self.curve3_plot[0:-1] = self.curve3_plot[1:]
                self.curve3_plot[-1] = math.degrees(euler[2])
                self.curve4_plot[0:-1] = self.curve4_plot[1:]
                self.curve4_plot[-1] = acc_z
                self.t[0:-1] = self.t[1:]
                self.t[-1] = time.time() - self.start_time
            else:
                pass

        except Exception as e:

            print('Exception raised: ', str(e), ', on line ', str(sys.exc_info()[2].tb_lineno))
            # Stop streaming
            for i in range(len(self.addresses)):
                self.serial_port.write(('>' + str(self.addresses[i]) + ',86\n').encode())
                time.sleep(0.1)
                while self.serial_port.inWaiting():
                    out = '>> ' + self.serial_port.read(self.serial_port.inWaiting()).decode()
                # print(out)
            self.serial_port.close()

        self.curve1.setData(self.t, self.curve1_plot)
        self.curve2.setData(self.t, self.curve2_plot)
        self.curve3.setData(self.t, self.curve3_plot)
        self.curve4.setData(self.t, self.curve4_plot)
        self.app.processEvents()  

if __name__ == '__main__':
    g = Graph()