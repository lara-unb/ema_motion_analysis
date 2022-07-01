""" Show real time angle between imu's

"""
import os
os.environ['FOR_DISABLE_CONSOLE_CTRL_HANDLER'] = '1'

from math import *
import sys
import time

import matplotlib.pyplot as plt


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

angles_values = []
angles_timestamps = []

#  Main function
if __name__ == '__main__':
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

                # save imu angle history
                print(angle_between_imus)

                # Save angle and time stamp
                angles_values.append(angle_between_imus)
                angles_timestamps.append(time.time() - startTime)

        except KeyboardInterrupt:
            print("Finished execution with control + c. ")
            serial_op.stop_streaming(serial_port, imu_configuration['logical_ids'])
            serial_op.manual_flush(serial_port)
            plt.plot(angles_timestamps, angles_values)
            plt.savefig("imu_angle"+ ".pdf") # str(time.time()) +
            plt.show()
            break
        except Exception:
            print("Unhandled exception.")
            serial_op.stop_streaming(serial_port, imu_configuration['logical_ids'])
            break 