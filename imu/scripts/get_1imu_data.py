""" Get imu accelerations and quaternions and plot it.

"""
import os
os.environ['FOR_DISABLE_CONSOLE_CTRL_HANDLER'] = '1'

from math import *
import sys
import time
import traceback
import matplotlib.pyplot as plt

sys.path.append("../utils/")
import serial_operations as serial_op
import file_management


sys.path.append("../../data_visualization")
from colors import *

# Set parameters that will be configured
imu_configuration = {
    "disableCompass": True,
    "disableGyro": False,
    "disableAccelerometer": False,
    "gyroAutoCalib": True,
    "filterMode": 1,
    "tareSensor": True,
    "logical_ids": [7],
    "streaming_commands": [39, 0, 255, 255, 255, 255, 255, 255]
}


# Initialize angle between IMU's
angle_between_imus = 0

# Initialize imu's quaternions
quaternions1 = [0, 0, 0, 0]
acc1 = [0, 0, 0]


angles_values = []
angles_timestamps = []

acc_values = []
acc_timestamps = []

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
                if data[0] != 0 and len(data)<=3:
                    print(RED, 'Corrupted data read.', RESET)
                    continue
                
                # Check sensor id number to get data
                if data[1] == 7:
                    extracted_data1 = serial_op.extract_acc_quat(data)
                    acc1 = extracted_data1['acc']
                    quaternions1 = extracted_data1['quaternions']


                acc_values.append(acc1[2])
                acc_timestamps.append(time.time() - startTime)

                sensor_data = {
                    "time_stamp": time.time() - startTime,
                    "acc": str(acc1),
                    "quaternion": str(quaternions1),
                }
                file_management.write_to_json_file("data/coleta1_imu_0.json", 
                                               sensor_data, 
                                               write_mode='a')

        except KeyboardInterrupt:
            print("Finished execution with control + c. ")
            serial_op.stop_streaming(serial_port, imu_configuration['logical_ids'])
            serial_op.manual_flush(serial_port)

            plt.plot(acc_timestamps, acc_values)
            plt.savefig("data/coleta1_coxa_acc3"+ ".pdf") 
            plt.show()
            
            break
        except Exception as error:
            print("Unhandled exception.")
            print(error)
            print(traceback.format_exc())
            serial_op.stop_streaming(serial_port, imu_configuration['logical_ids'])
            break 