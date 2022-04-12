import math
import time
import sys
import traceback

sys.path.append("../utils/")
from colors import *
from data_monitor import DataMonitor
import serial_operations as serial_op
import math

# Define data monitor channels
channels = [
        {
            'title': "X Angle", 
            'color': 'pink', 
            'y_label': 'Angle(deg)', 
            'x_label': "Time(s)", 
            "width": 2,
            "y_limit" : (-200, 200),
        },
        {
            'title': "Y Angle", 
            'color': 'cyan', 
            'y_label': 'Angle(deg)', 
            'x_label': "Time(s)", 
            "width": 2,
            "y_limit" : (-200, 200),
        },
        {
            'title': "Z Angle", 
            'color': 'red', 
            'y_label': 'Angle(deg)', 
            'x_label': "Time(s)", 
            "width": 2,
            "y_limit" : (-200, 200),
        }, 
]

if __name__ == '__main__':
    with DataMonitor(channels=channels) as dm:
        # Define imu configuration
        imuConfiguration = {
            "disableCompass": True,
            "disableGyro": False,
            "disableAccelerometer": False,
            "gyroAutoCalib": True,
            "filterMode": 1,
            "tareSensor": True,
            "logical_ids": [7, 8],
            "streaming_commands": [1, 255, 255, 255, 255, 255, 255, 255]
        }

        # Initialize imu
        serial_port = serial_op.initialize_imu(imuConfiguration)
        
        try:
            startTime = time.time()
            while True:
                print("running...")

                # Get imu response
                bytes_to_read = serial_port.inWaiting()
                if bytes_to_read > 0:
                    data = serial_port.read(bytes_to_read)
                    if data[0] != 0:
                        continue
                    
                    # Extract euler angles
                    extracted_data = serial_op.extract_euler_angles(data)

                    # Update data monitor
                    dm.data = {
                        "data": (
                            math.degrees(extracted_data["euler_vector"][0]), 
                            math.degrees(extracted_data["euler_vector"][1]), 
                            math.degrees(extracted_data["euler_vector"][2]),
                        ),
                        "time": time.time() - startTime,
                    }

                else:
                    time.sleep(0.1)
                    print("No data")
                    pass
        except Exception as e:
            print(RED, "Unexpected exception ocurred: ", RESET)
            print(traceback.format_exc())
            print(GREEN, "Stoping streaming.", RESET)
            serial_port = serial_op.stop_streaming(serial_port,
                                                   imuConfiguration["logical_ids"])
        except KeyboardInterrupt:
            print(CYAN, "Keyboard finished execution.", RESET)
            print(RED, "Stop streaming.", RESET)
            serial_port = serial_op.stop_streaming(serial_port, 
                                                   imuConfiguration["logical_ids"])