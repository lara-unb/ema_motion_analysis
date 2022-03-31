import math
import time
import sys
import traceback
from scipy.spatial.transform import Rotation as R

sys.path.append("../utils/")
from colors import *
from realTimeDataMonitor import DataMonitor
import serialOperations
import math

channels = [
        {
            'title': "X Angle", 
            'color': 'pink', 
            'y_label': 'Angle(deg)', 
            'x_label': "Time(s)", 
            "width": 2,
            "y_limit" : (-200, 200)
        },
        {
            'title': "Y Angle", 
            'color': 'cyan', 
            'y_label': 'Angle(deg)', 
            'x_label': "Time(s)", 
            "width": 2,
            "y_limit" : (-200, 200)
        },
        {
            'title': "Z Angle", 
            'color': 'red', 
            'y_label': 'Angle(deg)', 
            'x_label': "Time(s)", 
            "width": 2,
            "y_limit" : (-200, 200)
        },
        {
            'title': "X Angle Corke", 
            'color': 'pink', 
            'y_label': 'Angle(deg)', 
            'x_label': "Time(s)", 
            "width": 2,
            "y_limit" : (-200, 200)
        },
        {
            'title': "Y Angle Corke",
            'color': 'cyan', 
            'y_label': 'Angle(deg)', 
            'x_label': "Time(s)", 
            "width": 2,
            "y_limit" : (-200, 200)
        },
        {
            'title': "Z Angle Corke", 
            'color': 'red', 
            'y_label': 'Angle(deg)', 
            'x_label': "Time(s)", 
            "width": 2,
            "y_limit" : (-200, 200)
        }, 
]

if __name__ == '__main__':
    with DataMonitor(channels=channels) as dm:
        logical_ids = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14]

        # Find and open serial port for the IMU dongle
        serial_port = serialOperations.getDongleObject()


        # Stop streaming
        serial_port = serialOperations.stopStreaming(serial_port, logical_ids)

        # Manual flush. Might not be necessary
        serial_port = serialOperations.manualFlush(serial_port)
 
        print('Starting configuration')

        # Setting streaming slots, this means that while streaming sensors will send
        # this data to the dongle as in page 29 - User manual: 
        # 0 - Quaternions; 
        # 41 - Raw accelerations; 
        # 255 - No data
        commands = [0, 1, 255, 255, 255, 255, 255, 255]
        serial_port = serialOperations.setStreamingSlots(serial_port, logical_ids, commands)

        # Configure dictionary
        configDict = {
            "unableCompass": True,
            "unableGyro": False,
            "unableAccelerometer": False,
            "gyroAutoCalib": True,
            "filterMode": 1,
            "tareSensor": True
        }
        serial_port = serialOperations.configureSensor(serial_port, logical_ids, configDict)
        
        # Show some sensor configuration
        serialOperations.getSensorInformation(serial_port, logical_ids)

        # Start streaming
        serial_port = serialOperations.startStreaming(serial_port, logical_ids)
        
        try:
            startTime = time.time()
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
                    rot = R.from_quat([extracted_data['x'], extracted_data['y'],extracted_data['z'], extracted_data['w']])
                    euler_angles_scipy = rot.as_euler('xyz', degrees=True)

                    # Update data monitor
                    dm.data = {
                        "data": (
                            euler_angles_scipy[0], 
                            euler_angles_scipy[1], 
                            euler_angles_scipy[2],
                            math.degrees(extracted_data['roll']), 
                            math.degrees(extracted_data['pitch']), 
                            math.degrees(extracted_data['yaw'])
                        ),
                        "time": time.time() - startTime
                    }

                else:
                    # Did not receive data, wait 0.1 sec and continue
                    time.sleep(0.1)
                    print("No data")
                    pass
        except Exception as e:
            print(RED, "Unexpected exception ocurred: ", RESET)
            print(traceback.format_exc())
            print(GREEN, "Stoping streaming.", RESET)
            serial_port = serialOperations.stopStreaming(serial_port, logical_ids)
        except KeyboardInterrupt:
            print(CYAN, "Keyboard finished execution.", RESET)
            print(RED, "Stop streaming.", RESET)
            serial_port = serialOperations.stopStreaming(serial_port, logical_ids)