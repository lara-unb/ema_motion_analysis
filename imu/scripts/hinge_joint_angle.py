"""3D IMU visualization using rotation matrix

"""
import pygame
from math import *
import sys
import math
import traceback

sys.path.append("../utils/")
import serial_operations as serial_op
import orientation_operations as orientation_op

sys.path.append("../../data_visualization")
from colors import *

# Set parameters that will be configured
imu_configuration = {
    "disableCompass": True,
    "disableGyro": False,
    "disableAccelerometer": False,
    "gyroAutoCalib": True,
    "filterMode": 1,
    "tareSensor": False,
    "logical_ids": [7, 8],
    "streaming_commands": [0, 255, 255, 255, 255, 255, 255, 255]
}

# Initialize imu sensors
serial_port = serial_op.initialize_imu(imu_configuration)

# Not using streaming by now
serial_op.stop_streaming(serial_port, [7,8])

# Hinge joint -> Getting rotational offset of the compensation for the first device.
offset_quat0 = orientation_op.get_offset_quaternion(serial_port, 7)
print(offset_quat0)

# Hinge joint -> Getting rotational offset of the compensation for the second device.
offset_quat1 = orientation_op.get_offset_quaternion(serial_port, 8)
print(offset_quat1)

while True:
    try:
        print("running...")
        bytes_to_read = serial_port.inWaiting()
        
        # HINGE JOINT
        forward0 = orientation_op.calculate_device_vector(serial_port, 7, [0.0, 0.0, 1.0], offset_quat0)

        forward1 = orientation_op.calculate_device_vector(serial_port, 8, [0.0, 0.0, 1.0], offset_quat1)

        up0 = orientation_op.calculate_device_vector(serial_port, 7, [0.0, 1.0, 0.0], offset_quat0)

        print("Foward0: ", forward0)
        print("Foward1: ", forward1)


        angle = orientation_op.calculate_angle(forward1, forward0, up0)
        
        print("Angle between sensors: ", math.degrees(angle))
               
    except KeyboardInterrupt:
        print(CYAN, "Keyboard finished execution.", RESET)
        print(GREEN, "Stop streaming.", RESET)
        serial_port = serial_op.stop_streaming(serial_port, 
                                               imu_configuration['logical_ids'])
        break
    except Exception:
        print(RED, "Unexpected exception occured.", RESET)
        print(traceback.format_exc())
        print(GREEN, "Stop streaming.", RESET)
        serial_port = serial_op.stop_streaming(serial_port, 
                                               imu_configuration['logical_ids'])
        break