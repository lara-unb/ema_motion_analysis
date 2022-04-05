'''
This script is used to comunicate with the IMUs.
If connection == True, it sends data to the server for logging.
Authors: Lucas Fonseca
Contact: lucasfonseca@lara.unb.br
Date: Feb 25th 2019
Last update: April 12th 2019
'''
# this is a client for the IMUs

import time
import serial
import numpy as np
from multiprocessing.connection import Client
import serial.tools.list_ports
import sys

sys.path.append("../utils/")
from dataMonitor import DataMonitor


# --------------------------------------------------------- DATA MONITOR CONFIG
# define meta-info for DataMonitor plotting (label of data-rows and coloring)
channels = [
    {'label': 'Imu data x', 'color': 'tab:pink', 'linewidth': 2},
    {'label': 'Imu data y', 'color': 'tab:cyan', 'linewidth': 2},
    {'label': 'Imu data z', 'color': 'tab:orange', 'linewidth': 2}

]

# define plot format (dict of matplotlib.pyplot attributes and related (*args, **kwargs))
n_frames = 1000 # Hard-coded -> see if it's possible to use it dynamically
plt_kwargs = dict(
    xlim=((0, n_frames), {}),
    ylim=((-10, 10), {}),
    xlabel=(('Frame number', ), {}),
    ylabel=(('Angles in degrees',), {}),
)
angle_data = [(0, 0, 0, 0)]
# --------------------------------------------------------- DATA MONITOR CONFIG





# --------------------------------------------------------- IMU CONFIGURATION
# Understand and comment each line 



# Find and open serial port for the IMU dongle
list_ports_info = serial.tools.list_ports.comports()
for port_info in list_ports_info:
    print("\tPort:", port_info.device, "\tSerial#:", port_info.serial_number, "\tDesc:", port_info.description, 'PID', port_info.pid)
    # Aparently it's functional to only one dongle, maybe this is why we cannot use the small imu dongle
    if port_info.pid == 4128: # small IMU dongle
        portIMU = port_info.device


# Initialize serial port object 
serial_port = serial.Serial(port=portIMU, baudrate=115200, timeout=0.01)
time.sleep(0.1) # Commented to see if this is really necessary
serial_port.flush()                # Flush of file like objects. In this case, wait until all data is written.
serial_port.reset_input_buffer()   # Changed bc flushInput is depracated
serial_port.reset_output_buffer()  # Changed bc flushOutpu is depracated
time.sleep(0.1) # Commented to see if this is really necessary 




# Stop streaming - I think that this stops reading imu in order to configure
addresses = [1,2,3,4,5,6,7,8]
for i in range(len(addresses)):
    serial_port.write(('>'+str(addresses[i])+',86\n').encode())
    time.sleep(0.1)
    while serial_port.inWaiting():
        out = '>> ' + serial_port.read(serial_port.inWaiting()).decode()


# Manual flush. Might not be necessary - Comment it later to see if it's or not
while not serial_port.inWaiting() == 0:
    serial_port.read(serial_port.inWaiting())
    time.sleep(0.1)




print('Starting configuration')
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
calib = False
if calib:
    for i in range(len(addresses)):
        serial_port.write(('>'+str(addresses[i])+',165\n').encode())
        time.sleep(0.1)
        while serial_port.inWaiting():
            out = '>> ' + serial_port.read(serial_port.inWaiting()).decode()

# # Tare
# for i in range(len(addresses)):
#     serial_port.write(('>'+str(addresses[i])+',96\n').encode())
#     time.sleep(0.1)
#     while serial_port.inWaiting():
#         out = '>> ' + serial_port.read(serial_port.inWaiting()).decode()
#     # print(out)


print('Ending configuration')

# Start streaming
for i in range(len(addresses)):
    serial_port.write(('>'+str(addresses[i])+',85\n').encode())
    time.sleep(0.1)
    while serial_port.inWaiting():
        out = '>> ' + serial_port.read(serial_port.inWaiting()).decode()
    # print(out)

# --------------------------------------------------------- IMU CONFIGURATION



def read_sensors(portIMU):
    timer = time.time()
    print("Oi")
    global x,y,z, running, counters
    t0 = time.time()
    running = True
    id = 0
    now = time.time()
    try:
        with DataMonitor(channels=channels, ax_kwargs=plt_kwargs) as dm:
            iterator = 0
            while running:
                # print('waiting...')
                bytes_to_read = serial_port.inWaiting()
                # print(bytes_to_read)
                if bytes_to_read > 0:
                    # print('reading...')
                    data = serial_port.read(bytes_to_read)
                    # print('Full raw data: ' + str(data))
                    # print(data[0])
                    if len(data) <= 3 or data[0] != 0:
                        continue
                    data2 = data.decode().replace('\r\n',' ')
                    # data2 = ''.join(chr(i) for i in data.encode() if ord(chr(i)) > 31 and ord(chr(i)) < 128 )
                    data3 = data2.split(' ')
                    data3 = list(filter(None, data3))
                    # print(data3)

                    info = data3[0][0:3]

                    id = int.from_bytes(info[1].encode(), sys.byteorder)

                    ################################################################
                    ################################################################
                    # get data
                    quaternion = data3[0][3:]
                    accel = data3[1]
                    # id = int.from_bytes(temp[1].encode(), sys.byteorder)
                    # print('Final data: ' + str(temp))
                    # print('Quaternion: ' + str(quaternion))
                    # print('Accel: ' + str(accel))
                    # print(temp[1].encode())
                    # print(id)
                    # print(quaternion)

                    quaternion = quaternion.split(',')
                    quaternion = np.array(quaternion).astype(np.float64)

                    accel = accel.split(',')
                    accel = np.array(accel).astype(np.float64)


                    x = quaternion[0]
                    y = quaternion[1]
                    z = quaternion[2]
                    w = quaternion[3]
                    acc_x = accel[0]
                    acc_y = accel[1]
                    acc_z = accel[2]

                    ################################################################
                    ################################################################


                    # Send data to server
                    out = [time.time(), id, w, x, y, z, acc_x, acc_y, acc_z]
                    # server.send(out)


                    interval = time.time() - timer
                    if interval > 0.1:
                        iterator += 1
                        #sample = out[-1]
                        angle_data.append((iterator, acc_x+5, acc_y, acc_z-5))
                        dm.data = np.asarray(angle_data).T
                        timer = time.time()
                    

                else:
                    # print("No data")
                    # time.sleep(0.1)
                    pass


    except Exception as e:

        print('Exception raised: ', str(e), ', on line ', str(sys.exc_info()[2].tb_lineno))
        # Stop streaming
        for i in range(len(addresses)):
            serial_port.write(('>' + str(addresses[i]) + ',86\n').encode())
            time.sleep(0.1)
            while serial_port.inWaiting():
                out = '>> ' + serial_port.read(serial_port.inWaiting()).decode()
            # print(out)
        serial_port.close()

read_sensors(portIMU)