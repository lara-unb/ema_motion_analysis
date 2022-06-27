""" Show real time angle between imu's

"""

from math import *
import sys
import time


sys.path.append("../utils/")
import serial_operations as serial_op
import quaternion_operations as quaternions_op

sys.path.append("../../data_visualization")
from colors import *
from data_monitor import *

# Set parameters that will be configured
imu_configuration = {
    "disableCompass": True,
    "disableGyro": False,
    "disableAccelerometer": False,
    "gyroAutoCalib": True,
    "filterMode": 1,
    "tareSensor": True,
    "logical_ids": [7, 8],
    "streaming_commands": [0, 255, 255, 255, 255, 255, 255, 255]
}


# Initialize angle between IMU's
angle_between_imus = 0

# Initialize imu's quaternions
quaternions1 = [0, 0, 0, 0]
quaternions2 = [0, 0, 0, 0]



#  Main function
if __name__ == '__main__':

    channels = [
        {
            'title': "Angle 1", 
            'color': 'cyan', 
            'y_label': 'Angle(deg)', 
            'x_label': "Time(s)", 
            "width": 2,
        }, 
    ]
    with DataMonitor(channels=channels) as dm:
        # Starts dongle object
        serial_port = serial_op.initialize_imu(imu_configuration)

        # Wait configurations processing to avoid breaking
        time.sleep(2)

        startTime = time.time()
        while True:
            try:
                bytes_to_read = serial_port.inWaiting()

                # If there are data waiting in dongle, process it
                if  0 < bytes_to_read:

                    # Obtain data in dongle serial port
                    data = serial_port.read(bytes_to_read)

                    # Check if data package is OK - See sesnor user's manual.
                    if data[0] != 0:
                        print(RED, 'Corrupted data read.', RESET)
                        continue
                        
                    if data[1] == 8:
                        extracted_data1 = serial_op.extract_quaternions(data)
                        quaternions1 = extracted_data1['quaternions']

                    elif data[1] == 7:
                        extracted_data2 = serial_op.extract_quaternions(data)
                        quaternions2 = extracted_data2['quaternions']

                    # calculate angle between IMUs
                    angle_between_imus = quaternions_op.calculate_angle_between_quaternions(quaternions1, quaternions2)

                    # Update Data monitor
                    dm.data = {
                        "data": (angle_between_imus, ),
                        "time": time.time() - startTime
                    }

            except ExitDataMonitorException:
                print("Finished execution.")
                serial_op.stop_streaming(serial_port, imu_configuration['logical_ids'])
                break 
            except Exception:
                print("Unhandled exception.")
                serial_op.stop_streaming(serial_port, imu_configuration['logical_ids'])
                break 