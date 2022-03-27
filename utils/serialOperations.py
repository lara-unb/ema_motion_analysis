import serial.tools.list_ports
import time
import sys
import numpy as np


def getDongleObject():
    ports_list = serial.tools.list_ports.comports()
    for wire in ports_list:
        print("\tPort:", wire.device, "\tSerial#:", wire.serial_number, "\tDesc:", wire.description, 'PID', wire.pid)
        if wire.pid == 4128: # small IMU dongle
            portIMU = wire.device
    # portIMU = '/dev/tty.usbmodem14101' # rPi
    serial_port = serial.Serial(port=portIMU, baudrate=115200, timeout=0.01)
    time.sleep(0.1)
    serial_port.flush()
    serial_port.flushInput()
    serial_port.flushOutput()
    time.sleep(0.1)
    return serial_port

def manualFlush(serial_port):
    while not serial_port.inWaiting() == 0:
        serial_port.read(serial_port.inWaiting())
        time.sleep(0.1)
    return serial_port

def stopStreaming(serial_port, addresses):
    for i in range(len(addresses)):
        serial_port.write(('>'+str(addresses[i])+',86\n').encode())
        time.sleep(0.1)
        while serial_port.inWaiting():
            out = '>> ' + serial_port.read(serial_port.inWaiting()).decode()
    return serial_port

def startStreaming(serial_port, addresses):
    # Start streaming
    for i in range(len(addresses)):
        serial_port.write(('>'+str(addresses[i])+',85\n').encode())
        time.sleep(0.1)
        while serial_port.inWaiting():
            out = '>> ' + serial_port.read(serial_port.inWaiting()).decode()
    return serial_port

def setStreamingSlots(serial_port, addresses, commands):
    for i in range(len(addresses)):
        msg = '>' + str(addresses[i]) + ',80,' + str(commands[0]) + ',' + \
                                                str(commands[1]) + ',' + \
                                                str(commands[2]) + ',' + \
                                                str(commands[3]) + ',' + \
                                                str(commands[4]) + ',' + \
                                                str(commands[5]) + ',' + \
                                                str(commands[6]) + ',' + \
                                                str(commands[7]) + '\n'
        print(msg)
        serial_port.write(msg.encode())
        time.sleep(0.1)
        out = ''
        while serial_port.inWaiting():
            out += '>> ' + serial_port.read(serial_port.inWaiting()).decode()
    return serial_port

def calibrateSensor(serial_port, addresses, calibGyro):
    # Set mag on(1)/off(0)
    for i in range(len(addresses)):
        serial_port.write(('>'+str(addresses[i])+',109, 0\n').encode())
        time.sleep(0.1)
        while serial_port.inWaiting():
            out = '>> ' + serial_port.read(serial_port.inWaiting()).decode()

    # Gyro autocalibration
    if calibGyro:
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
    
    return serial_port

# Get the expected output/this works for the corresponding 
# streaming slots setted previously
def extractResponse(data):
    extracted_data = {}

    data2 = data.decode().replace('\r\n',' ')
    data3 = data2.split(' ')
    data3 = list(filter(None, data3))

    info = data3[0][0:3]
    id = int.from_bytes(info[1].encode(), sys.byteorder)

    # Extracting quaternions and aceleration
    quaternion = data3[0][3:]
    accel = data3[1]
    quaternion = quaternion.split(',')
    quaternion = np.array(quaternion, dtype=np.float64)
    accel = accel.split(',')
    accel = np.array(accel).astype(np.float)
    extracted_data['x'] = quaternion[0]
    extracted_data['y'] = quaternion[1]
    extracted_data['z'] = quaternion[2]
    extracted_data['w'] = quaternion[3]
    extracted_data['acc_x'] = accel[0]
    extracted_data['acc_y'] = accel[1]
    extracted_data['acc_z'] = accel[2]
    
    return extracted_data