""" 2 IMU's 3d visualization and angle difference using quaternions

"""

import pygame
from math import *
import numpy as np
import sys
import time
import traceback
from scipy.spatial.transform import Rotation as R

sys.path.append("../utils/")
import serial_operations as serial_op
import pygame_operations as pygame_op
import quaternion_operations as quaternions_op

sys.path.append("../../data_visualization")
from colors import *

# Start - Set visual configurations 
WINDOW_SIZE =  600

# Cube points initialized
SIZE_X = 1
SIZE_Y = 0.5
SIZE_Z = 1.5
SCALE = 45

# Define imu's offsets (center of imu in the screen)
offset_x1 = WINDOW_SIZE/2
offset_y1 = WINDOW_SIZE/4
offset_x2 = WINDOW_SIZE/2
offset_y2 = 3 * WINDOW_SIZE/4

# Initialize pygame graphics interface
window = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
clock = pygame.time.Clock()

# set location of each cube point
cube_points = pygame_op.get_3d_object_points(SIZE_X, SIZE_Y, SIZE_Z)

# set de location of the orientation axis points
orientation_points = pygame_op.get_orientation_points()

# set the pygame window name
pygame.display.set_caption('IMU 3D Visualization')

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
serial_port = serial_op.initialize_imu(imu_configuration)

# Initialize rotation matrix
rotation_matrix1 = np.array([[1,0,0], [0,1,0], [0,0,1]])
rotation_matrix2 = np.array([[1,0,0], [0,1,0], [0,0,1]])

# Initialize angle between IMU's
angle_between_imus = 0

# Define shown texts
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
    {
        "text": "Angle between IMUs: ",
        "color": pygame_op.PINK_RGB,
        "position": (200, WINDOW_SIZE-40),
    },
    {
        "text": str(angle_between_imus),
        "color": pygame_op.CYAN_RGB,
        "position": (300, WINDOW_SIZE-40),
    },
]

# Initialize imu's quaternions
quaternions1 = [0, 0, 0, 0]
quaternions2 = [0, 0, 0, 0]

# Wait configurations processing to avoid breaking
time.sleep(2)

#  Main loop
while True:
    try:
        # Pygame update rate
        clock.tick(60)
        
        # Clean screen
        window.fill((0,0,0))

        # Draw IMU's in the screen
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

        print("running...")
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
                rotation_matrix1 = R.from_quat(quaternions1).as_matrix()
                # change tare position 90 degress
                rotation_matrix1[[1, 2]] = rotation_matrix1[[2, 1]]

            elif data[1] == 7:
                extracted_data2 = serial_op.extract_quaternions(data)
                quaternions2 = extracted_data2['quaternions']
                rotation_matrix2 = R.from_quat(quaternions2).as_matrix()
                # change tare position 90 degrees
                rotation_matrix2[[1, 2]] = rotation_matrix2[[2, 1]]

            # calculate angle between IMUs
            angle_between_imus = quaternions_op.calculate_angle_between_quaternions(quaternions1, quaternions2)

            # Update angle shown in the screen
            texts_dict[5] = {
                                "text": str(int(angle_between_imus)),
                                "color": pygame_op.PINK_RGB,
                                "position": (420, WINDOW_SIZE-40),
                            }

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