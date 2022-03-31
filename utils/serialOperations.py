from re import I
import serial.tools.list_ports
import time
import sys
import numpy as np


# If permission denied error occurs in Linux try:
# sudo chmod 666 /dev/ttyACM0 -> with the correspondent COM port
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

def createIMUCommandString(logical_id, command_number, arguments = []):
    # Create command
    command = ">"+str(logical_id)+","+str(command_number)
    if(len(arguments) != 0):
        arguments_string = ","
        for  argument in arguments:
            arguments_string += str(argument)
            arguments_string += ","
        arguments_string = arguments_string[:-1]
        command += arguments_string
    command += '\n'
    return command.encode()

def applyCommand(serial_port, commandString, showResponse=False):
    serial_port.write(commandString)
    if(showResponse):
        time.sleep(0.1)
        while serial_port.inWaiting():
            out = '>> ' + serial_port.read(serial_port.inWaiting()).decode()
        print(out)

def stopStreaming(serial_port, logical_ids):
    for id in logical_ids:
        commandString = createIMUCommandString(id, 86)
        applyCommand(serial_port, commandString)
    return serial_port

def startStreaming(serial_port, logical_ids):
    for id in logical_ids:
        commandString = createIMUCommandString(id, 85)
        applyCommand(serial_port, commandString)
    return serial_port

def setStreamingSlots(serial_port, logical_ids, commands):
    for id in logical_ids:
        commandString = createIMUCommandString(id, 85, commands)
        applyCommand(serial_port, commandString)
    return serial_port

# Explain configDict
def configureSensor(serial_port, logical_ids, configDict):
    if(configDict["unableGyro"]):
        for id in logical_ids:
            commandString = createIMUCommandString(id, 107)
            applyCommand(serial_port, commandString)
    if(configDict["unableAccelerometer"]):
        for id in logical_ids:
            commandString = createIMUCommandString(id, 108)
            applyCommand(serial_port, commandString)
    if(configDict["unableCompass"]):
        for id in logical_ids:
            commandString = createIMUCommandString(id, 109)
            applyCommand(serial_port, commandString)
    # Set filter mode
    filterMode = configDict["filterMode"]
    for id in logical_ids:
        commandString = createIMUCommandString(id, 123, [filterMode])
        applyCommand(serial_port, commandString)

    if configDict["gyroAutoCalib"]:
        for id in logical_ids:
            commandString = createIMUCommandString(id, 165)
            applyCommand(serial_port, commandString)

    if configDict["tareSensor"]:
        for id in logical_ids:
            commandString = createIMUCommandString(id, 96)
            applyCommand(serial_port, commandString)
    
    return serial_port

def getSensorInformation(serial_port, addresses):
    # Current Filter Mode 
    for i in range(len(addresses)):
        serial_port.write(('>'+str(addresses[i])+',152\n').encode())
        time.sleep(0.1)
        while serial_port.inWaiting():
            out = serial_port.read(serial_port.inWaiting()).decode()
            if(out[0] == "0"):
                print("Current Filter Mode: >> ", out)
    # Current accelerometer trust values
    for i in range(len(addresses)):
        serial_port.write(('>'+str(addresses[i])+',130\n').encode())
        time.sleep(0.1)
        while serial_port.inWaiting():
            out = serial_port.read(serial_port.inWaiting()).decode()
            if(out[0] == "0"):
                print("Current Accelerometer Trust Values: >> ", out)

# Get the expected output/this works for the corresponding 
# streaming slots setted previously
def extractResponse(data):
    # Clean data
    list_data = data.decode().replace('\r\n',' ').split(' ')
    cleaned_list_data = list(filter(None, list_data))

    # Extracting quaternions and aceleration
    quaternion = cleaned_list_data[0][3:].split(',')
    euler = cleaned_list_data[1].split(",")
    quaternion = np.array(quaternion, dtype=np.float64)
    euler = np.array(euler, dtype=np.float64)

    extracted_data = {
        'x': quaternion[0],
        'y': quaternion[1],
        'z': quaternion[2],
        'w': quaternion[3],
        'roll': euler[0],
        'pitch': euler[1],
        'yaw': euler[2]
    }   
    return extracted_data


