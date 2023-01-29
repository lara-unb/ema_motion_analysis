""" Show real time angle between imu's

"""
import os

from numpy import byte
os.environ['FOR_DISABLE_CONSOLE_CTRL_HANDLER'] = '1'

from math import *
import sys
import time
import traceback
import matplotlib.pyplot as plt
import file_management

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
    "streaming_commands": [39, 0, 255, 255, 255, 255, 255, 255]
}


# Initialize angle between IMU's
angle_between_imus = 0

# Initialize imu's quaternions
quaternions1 = [0, 0, 0, 0]
quaternions2 = [0, 0, 0, 0]
acc1 = [0, 0, 0]
acc2 = [0, 0, 0]


angles_values = []
angles_timestamps = []

acc_values_thigh = []
acc_values_feet = []
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
                    
                if data[1] == 7:
                    extracted_data1 = serial_op.extract_acc_quat(data)
                    acc1 = extracted_data1['acc']
                    quaternions1 = extracted_data1['quaternions']

                elif data[1] == 8:
                    extracted_data2 = serial_op.extract_acc_quat(data)
                    acc2 = extracted_data2['acc']
                    quaternions2 = extracted_data2['quaternions']

                # calculate angle between IMUs
                angle_between_imus = quaternions_op.calculate_angle_between_quaternions(quaternions1, quaternions2)

                # save imu angle history
                #print(quaternions1[2])
                
                # Save angle and time stamp


                acc_values_thigh.append(acc1[2])
                acc_values_feet.append(acc2[1])
                acc_timestamps.append(time.time() - startTime)

                thigh_data = {
                    "time_stamp": time.time() - startTime,
                    "acc": str(acc1),
                    "quaternion": str(quaternions1),
                }
                file_management.write_to_json_file("data/coleta1_coxa3.json", 
                                               thigh_data, 
                                               write_mode='a')

                feet_data = {
                    "time_stamp": time.time() - startTime,
                    "acc": str(acc2),
                    "quaternion": str(quaternions2),
                }
                file_management.write_to_json_file("data/coleta1_pe3.json", 
                                               feet_data, 
                                               write_mode='a')

        except KeyboardInterrupt:
            print("Finished execution with control + c. ")
            serial_op.stop_streaming(serial_port, imu_configuration['logical_ids'])
            serial_op.manual_flush(serial_port)

            plt.plot(acc_timestamps, acc_values_thigh)
            plt.savefig("data/coleta1_coxa_acc3"+ ".pdf") # str(time.time()) +
            plt.show()
            
            plt.plot(acc_timestamps, acc_values_feet)
            plt.savefig("data/coleta1_pe_acc3"+ ".pdf") # str(time.time()) +
            plt.show()
            break
        except Exception as error:
            print("Unhandled exception.")
            print(error)
            print(traceback.format_exc())
            serial_op.stop_streaming(serial_port, imu_configuration['logical_ids'])
            break 