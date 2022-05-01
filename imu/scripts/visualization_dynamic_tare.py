"""3D IMU visualization using rotation matrix

"""

import pygame
from math import *
import numpy as np
import sys
import time
import traceback

sys.path.append("../utils/")
import serial_operations as serial_op
import pygame_operations as pygame_op

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
    "tareSensor": False,
    "logical_ids": [7],
    "streaming_commands": [2, 255, 255, 255, 255, 255, 255, 255]
}

serial_port = serial_op.initialize_imu(imu_configuration)

answer = serial_op.write_command_read_answer(serial_port, imu_configuration["logical_ids"], 12)

print(answer)
input()
# Main Loop
SCALE = 100

# set the pygame window name
pygame.display.set_caption('IMU 3D Visualization')


# Initialize rotation matrix
rotation_matrix = np.array([[1,0,0], [0,1,0], [0,0,1]])

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


offset_x = WINDOW_SIZE/2
offset_y = WINDOW_SIZE/2

while True:

    try:
        clock.tick(60)
        window.fill((0,0,0))

        pygame_op.render_information(window,
                                    texts_dict,
                                    cube_points,
                                    rotation_matrix,
                                    SCALE,
                                    offset_x,
                                    offset_y,
                                    orientation_points,
                                    pygame_op.WHITE_RGB)


        # print("Euler angles: ")
        # serial_op.manual_flush(serial_port)
        # command  = serial_op.create_imu_command(7, 1)
        # serial_op.apply_command(serial_port, command, True)[-3:]
        # input()
        # Update rotation matrix if there are data
        print("running...")
        bytes_to_read = serial_port.inWaiting()
        
        # NUMERO DO ALEM VAMOS DESCOBRIR PQ
        if  0 < bytes_to_read > 80:
            data = serial_port.read(bytes_to_read)
            if data[0] != 0:
                continue
            extracted_data = serial_op.extract_rotation_matrix(data)
            rotation_matrix = extracted_data['rotation_matrix']

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