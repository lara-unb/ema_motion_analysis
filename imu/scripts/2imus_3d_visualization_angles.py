"""3D IMU visualization using rotation matrix

"""

import pygame
from math import *
import numpy as np
import sys
import time
import traceback
from pyquaternion import Quaternion

sys.path.append("../utils/")
import serial_operations as serial_op
import pygame_operations as pygame_op
import quaternion_operations as quaternions_op

sys.path.append("../../data_visualization")
from colors import *


# Start - Set visual configurations 
WINDOW_SIZE =  600
window = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
clock = pygame.time.Clock()

# Cube points initialized
SIZE_X = 1
SIZE_Y = 0.5
SIZE_Z = 1.5

cube_points = pygame_op.get_3d_object_points(SIZE_X, SIZE_Y, SIZE_Z)

orientation_points = pygame_op.get_orientation_points()

# Set parameters that will be configured
imu_configuration = {
    "disableCompass": True,
    "disableGyro": False,
    "disableAccelerometer": False,
    "gyroAutoCalib": True,
    "filterMode": 1,
    "tareSensor": True,
    "logical_ids": [7, 8],
    "streaming_commands": [0, 255, 255, 255, 255, 255, 255, 255] # 2 -> rotation matrix
}
serial_port = serial_op.initialize_imu(imu_configuration)

# Main Loop
SCALE = 45

# set the pygame window name
pygame.display.set_caption('IMU 3D Visualization')


# Initialize rotation matrix
rotation_matrix1 = np.array([[1,0,0], [0,1,0], [0,0,1]])
rotation_matrix2 = np.array([[1,0,0], [0,1,0], [0,0,1]])

texts_dict = [
    {
        "text": "X axis",
        "color": pygame_op.RED_RGB,
        "position": (20, 20),
    },
    {
        "text": "Y axis",
        "color": pygame_op.GREEN_RGB,
        "position": (20, 50),
    },
    {
        "text": "Z axis",
        "color": pygame_op.CYAN_RGB,
        "position": (20, 80),
    },
    {
        "text": "Press t to tare.",
        "color": pygame_op.WHITE_RGB,
        "position": (20, WINDOW_SIZE-40),
    },
]


offset_x1 = WINDOW_SIZE/2
offset_y1 = WINDOW_SIZE/4

offset_x2 = WINDOW_SIZE/2
offset_y2 = 3 * WINDOW_SIZE/4

time.sleep(2)

quaternions1 = [0, 0, 0, 0]
quaternions2 = [0, 0, 0, 0]

while True:

    try:
        clock.tick(60)
        window.fill((0,0,0))

        pygame_op.render_information(window,
                                    texts_dict,
                                    cube_points,
                                    rotation_matrix1,
                                    SCALE,
                                    offset_x1,
                                    offset_y1,
                                    orientation_points, 
                                    pygame_op.PINK_RGB)


        pygame_op.render_information(window,
                            texts_dict,
                            cube_points,
                            rotation_matrix2,
                            SCALE,
                            offset_x2,
                            offset_y2,
                            orientation_points,
                            pygame_op.YELLOW_RGB)


        # print("Euler angles: ")
        # serial_op.manual_flush(serial_port)
        # command  = serial_op.create_imu_command(7, 1)
        # serial_op.apply_command(serial_port, command, True)[-3:]
        # input()
        # Update rotation matrix if there are data
        print("running...")
        bytes_to_read = serial_port.inWaiting()
        print(CYAN, 'BYTES TO READ: ', bytes_to_read, RESET)

        # NUMERO DO ALEM VAMOS DESCOBRIR PQ
        if  0 < bytes_to_read > 86:
            data = serial_port.read(bytes_to_read)
            if data[0] != 0:
                print(RED, 'CONTINUE', RESET)
                continue
                

            print('DATA 1: ', data[1])
            if data[1] == 8:
                extracted_data1 = serial_op.extract_quaternions(data)
                quaternions1 = extracted_data1['quaternions']
                quaternionObject1 = Quaternion(quaternions1)
                rotation_matrix1 = quaternionObject1.rotation_matrix
            elif data[1] == 7:
                extracted_data2 = serial_op.extract_quaternions(data)
                quaternions2 = extracted_data2['quaternions']
                quaternionObject2 = Quaternion(quaternions2)
                rotation_matrix2 = quaternionObject2.rotation_matrix
            
            
            print()
            print(quaternions_op.calculate_angle_between_quaternions(quaternions1, quaternions2))
            print()


        # Event user event handling handling
        for event in pygame.event.get():
            # Get quit event
            if event.type == pygame.QUIT:
                pygame.quit()
                raise KeyboardInterrupt

            # Tare sensor
            keys = pygame.key.get_pressed()
            if keys[pygame.K_t]:
                serial_op.tare_sensor(serial_port, 
                                      imu_configuration['logical_ids'])
        
        # Update pygame display
        pygame.display.update()
    
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