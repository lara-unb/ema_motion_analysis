import math
import spatialmath
from spatialmath import UnitQuaternion as UQ

import time
import sys
import traceback
import numpy as np
sys.path.append("../utils/")
from colors import *
from RealTimeDataMonitor import DataMonitor
import serialOperations

# Transform quaternions to euler angles
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
    
    return roll_x, pitch_y, yaw_z 


channels = [
        {'title': "X Angle", 'color': 'pink', 'y_label': 'Angle(deg)', 'x_label': "Time(s)", "width": 2},
        {'title': "Y Angle", 'color': 'cyan', 'y_label': 'Angle(deg)', 'x_label': "Time(s)", "width": 2},
        {'title': "Z Angle", 'color': 'red', 'y_label': 'Angle(deg)', 'x_label': "Time(s)", "width": 2},
        {'title': "X Angle Corke", 'color': 'pink', 'y_label': 'Angle(deg)', 'x_label': "Time(s)", "width": 2},
        {'title': "Y Angle Corke", 'color': 'cyan', 'y_label': 'Angle(deg)', 'x_label': "Time(s)", "width": 2},
        {'title': "Z Angle Corke", 'color': 'red', 'y_label': 'Angle(deg)', 'x_label': "Time(s)", "width": 2},
        
    ]

if __name__ == '__main__':
    with DataMonitor(channels=channels) as dm:
        calibGyro = True
        addresses = [0,1,2,3,4,5,6,7,8]

        # Find and open serial port for the IMU dongle
        serial_port = serialOperations.getDongleObject()


        # Stop streaming
        serial_port = serialOperations.stopStreaming(serial_port, addresses)

        # Manual flush. Might not be necessary
        serial_port = serialOperations.manualFlush(serial_port)
 
        print('Starting configuration')

        # Setting streaming slots, this means that while streaming sensors will send
        # this data to the dongle as in page 29 - User manual: 
        # 0 - Quaternions; 
        # 41 - Raw accelerations; 
        # 255 - No data
        commands = [0, 41, 255, 255, 255, 255, 255, 255]
        serial_port = serialOperations.setStreamingSlots(serial_port, addresses, commands)

        # Set magnetometer(explain it better), calibGyro if calibGyro=True and Tare sensor
        serial_port = serialOperations.calibrateSensor(serial_port, addresses, calibGyro)

        # Start streaming
        serial_port = serialOperations.startStreaming(serial_port, addresses)
        
        try:
            while True:
                print("running...")
                # time.sleep(.1)
                bytes_to_read = serial_port.inWaiting()
                if bytes_to_read > 0:

                    data = serial_port.read(bytes_to_read)
                    if len(data) <= 3 or data[0] != 0:
                        continue

                    extracted_data = serialOperations.extractResponse(data)

                    # Convert quaternions to visual euler angles
                    euler_angles_rad = euler_from_quaternion(
                        extracted_data['x'], extracted_data['y'],extracted_data['z'], extracted_data['w']
                    )
                    euler_angles_degree = list(map(lambda ang: math.degrees(ang), euler_angles_rad))
                    
                    # Convert quaternions to visual euler angles - using spatialmath library
                    quaternion_SM = UQ([extracted_data['x'], extracted_data['y'],extracted_data['z'], extracted_data['w']])
                    euler_angles_degree_SM = quaternion_SM.eul(unit='deg')

                    # TA DIFERENTE N SEI PQ :(
                    print('EULER VICTOR: ', euler_angles_degree)
                    print('EULER SM: ', euler_angles_degree_SM)

                    # time.sleep(.5)

                    # Update data monitor
                    dm.data = (euler_angles_degree[0], euler_angles_degree[1], euler_angles_degree[2],
                                euler_angles_degree_SM[0], euler_angles_degree_SM[1], euler_angles_degree_SM[2] )


                else:
                    # Did not receive data, wait 0.1 sec and continue
                    time.sleep(0.1)
                    pass
        except Exception as e:
            print(RED, "Unexpected exception ocurred: ", RESET)
            print(traceback.format_exc())
            print(GREEN, "Stoping streaming.", RESET)
            serial_port = serialOperations.stopStreaming(serial_port, addresses)
        except KeyboardInterrupt:
            print(CYAN, "Keyboard finished execution.", RESET)
            print(RED, "Stop streaming.", RESET)
            serial_port = serialOperations.stopStreaming(serial_port, addresses)