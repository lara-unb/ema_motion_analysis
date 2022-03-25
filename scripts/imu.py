import time
import pyqtgraph as pg
from pyqtgraph.Qt import QtGui, QtCore
import serial.tools.list_ports
import numpy as np
import sys
sys.path.append("../utils/")
from RealTimeDataMonitor import DataMonitor
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


# Connect to the server
calib = False

addresses = [1,2,3,4,5,6,7,8]

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
serial_port = serial.Serial(port=portIMU, baudrate=115200, timeout=0.01)
time.sleep(0.1)
serial_port.flush()
serial_port.flushInput()
serial_port.flushOutput()
time.sleep(0.1)

# Stop streaming
for i in range(len(addresses)):
    serial_port.write(('>'+str(addresses[i])+',86\n').encode())
    time.sleep(0.1)
    while serial_port.inWaiting():
        out = '>> ' + serial_port.read(serial_port.inWaiting()).decode()
    # print(out)

# Manual flush. Might not be necessary
while not serial_port.inWaiting() == 0:
    serial_port.read(serial_port.inWaiting())
    time.sleep(0.1)

print('Starting configuration')
# Set streaming slots
for i in range(len(addresses)):
    msg = '>' + str(addresses[i]) + ',80,' + str(command[0]) + ',' + \
                                            str(command[1]) + ',' + \
                                            str(command[2]) + ',' + \
                                            str(command[3]) + ',' + \
                                            str(command[4]) + ',' + \
                                            str(command[5]) + ',' + \
                                            str(command[6]) + ',' + \
                                            str(command[7]) + '\n'
    print(msg)
    serial_port.write(msg.encode())
    time.sleep(0.1)
    out = ''
    while serial_port.inWaiting():
        out += '>> ' + serial_port.read(serial_port.inWaiting()).decode()
    print(out)
out = ''

# Set mag on(1)/off(0)
for i in range(len(addresses)):
    serial_port.write(('>'+str(addresses[i])+',109, 0\n').encode())
    time.sleep(0.1)
    while serial_port.inWaiting():
        out = '>> ' + serial_port.read(serial_port.inWaiting()).decode()

# Gyro autocalibration
if calib:
    for i in range(len(addresses)):
        serial_port.write(('>'+str(addresses[i])+',165\n').encode())
        time.sleep(0.1)
        while serial_port.inWaiting():
            out = '>> ' + serial_port.read(serial_port.inWaiting()).decode()

# Tare
for i in range(len(addresses)):
    serial_port.write(('>'+str(addresses[i])+',96\n').encode())
    time.sleep(0.1)
    while serial_port.inWaiting():
        out = '>> ' + serial_port.read(serial_port.inWaiting()).decode()
    # print(out)

# Start streaming
for i in range(len(addresses)):
    serial_port.write(('>'+str(addresses[i])+',85\n').encode())
    time.sleep(0.1)
    while serial_port.inWaiting():
        out = '>> ' + serial_port.read(serial_port.inWaiting()).decode()
    # print(out)

channels = [
        {'title': "X Angle", 'color': 'pink', 'y_label': 'Angle(deg)', 'x_label': "Time(s)", "width": 2},
        {'title': "Y Angle", 'color': 'cyan', 'y_label': 'Angle(deg)', 'x_label': "Time(s)", "width": 2},
        {'title': "Z Angle", 'color': 'cyan', 'y_label': 'Angle(deg)', 'x_label': "Time(s)", "width": 2}
    ]

with DataMonitor(channels=channels) as dm:
    i = 30
    while(i > 0):
        dm.data = (i, -i, 2)
        i-=1
        time.sleep(1)
        # try:
        #     id = 0
        #     bytes_to_read = serial_port.inWaiting()
        #     if bytes_to_read > 0:
        #         data = serial_port.read(bytes_to_read)
        #         if len(data) <= 3 or data[0] != 0:
        #             break
        #         data2 = data.decode().replace('\r\n',' ')
        #         data3 = data2.split(' ')
        #         data3 = list(filter(None, data3))

        #         info = data3[0][0:3]

        #         id = int.from_bytes(info[1].encode(), sys.byteorder)

        #         quaternion = data3[0][3:]
        #         accel = data3[1]

        #         quaternion = quaternion.split(',')
        #         quaternion = np.array(quaternion).astype(np.float)

        #         accel = accel.split(',')
        #         accel = np.array(accel).astype(np.float)

        #         x = quaternion[0]
        #         y = quaternion[1]
        #         z = quaternion[2]
        #         w = quaternion[3]
        #         acc_x = accel[0]
        #         acc_y = accel[1]
        #         acc_z = accel[2]

        #         out = [time.time(), id, w, x, y, z, acc_x, acc_y, acc_z]
        #         print(out)

        #         euler = euler_from_quaternion(w, x, y, z)

        #         dm.data = (math.degrees(euler[0]), math.degrees(euler[1]), math.degrees(euler[2]))

        #     else:
        #         pass

        # except Exception as e:

        #     print('Exception raised: ', str(e), ', on line ', str(sys.exc_info()[2].tb_lineno))
        #     # Stop streaming
        #     for i in range(len(addresses)):
        #         serial_port.write(('>' + str(addresses[i]) + ',86\n').encode())
        #         time.sleep(0.1)
        #         while serial_port.inWaiting():
        #             out = '>> ' + serial_port.read(serial_port.inWaiting()).decode()
        #         # print(out)
        #     serial_port.close()
