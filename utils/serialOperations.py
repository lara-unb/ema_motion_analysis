from re import I
import serial.tools.list_ports
import time
import numpy as np

import sys
sys.path.append("../utils/")
from colors import *


# If permission denied error occurs in Linux try:
# sudo chmod 666 /dev/ttyACM0 -> with the correspondent COM port
def getDongleObject():
    ports_list = serial.tools.list_ports.comports()
    print("Ports available: ")
    for wire in ports_list:
        print("Port:", wire.device, "\tSerial#:", wire.serial_number, "\tDesc:", wire.description, 'PID', wire.pid)
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
    time.sleep(0.1)
    if(showResponse):
        while serial_port.inWaiting():
            out = '>> ' + serial_port.read(serial_port.inWaiting()).decode()
        print(out)
    time.sleep(0.1)

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
        commandString = createIMUCommandString(id, 80, commands)
        print(RED, commandString)
        applyCommand(serial_port, commandString, True)
    return serial_port

# Explain configDict
def configureSensor(serial_port, logical_ids, configDict):
    if(configDict["disableGyro"]):
        for id in logical_ids:
            commandString = createIMUCommandString(id, 107)
            applyCommand(serial_port, commandString)
    if(configDict["disableAccelerometer"]):
        for id in logical_ids:
            commandString = createIMUCommandString(id, 108)
            applyCommand(serial_port, commandString)
    if(configDict["disableCompass"]):
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

def tareSensor(serial_port, logical_ids):
    for id in logical_ids:
        commandString = createIMUCommandString(id, 96)
        applyCommand(serial_port, commandString)

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

# Get rotation matrix streamed in first slot. 
def extractRotationMatrix(data):
    decoded_data = data.decode()
    list_data = decoded_data.replace('\r\n',' ').split(' ')
    cleaned_list_data = list(filter(None, list_data))
    rotatation_vector = cleaned_list_data[0][3:].split(',')
    rotatation_vector = np.array(rotatation_vector, dtype=np.float64)
    rotation_matrix = rotatation_vector.reshape((3,3))
    return {'rotation_matrix': rotation_matrix}   

def initializeImu(configurationDict):
    # Find and open serial port for the IMU dongle
    print("Getting imu object:")
    serial_port = getDongleObject()
    print(GREEN, "Done.", RESET)

    # Clean outputs 
    serial_port = manualFlush(serial_port)
    
    # Stop streaming
    print("Stoping streaming.")
    serial_port = stopStreaming(serial_port, configurationDict['logical_ids'])


    # Setting streaming slots, this means that while streaming sensors will send
    # this data to the dongle as in page 29 - User manual: 
    # 0 - Differential quaternions; 
    # 1 - tared orientation as euler angles; 
    # 2 - rotation matrix
    # 255 - No data
    serial_port = setStreamingSlots(serial_port, configurationDict['logical_ids'], configurationDict['streaming_commands'])

    # Set magnetometer(explain it better), calibGyro if calibGyro=True and Tare sensor
    print('Starting configuration: ')
    serial_port = configureSensor(serial_port, configurationDict['logical_ids'], configurationDict)
    print(GREEN, "Done.", RESET)


    print(CYAN, "Starting streamnig.", RESET)
    # Start streaming
    serial_port = startStreaming(serial_port, configurationDict['logical_ids'])
    
    print(GREEN, "IMU's ready to use.", RESET)

    return serial_port