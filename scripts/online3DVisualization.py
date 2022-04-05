import pygame
from math import *
import numpy as np
from scipy.spatial.transform import Rotation as R
import sys

sys.path.append("../utils/")
from colors import *
import serialOperations as serialOp
import pygameOperations as pygameOp

# Start - Set visual configurations ---------------------------------------------------------------------------
WINDOW_SIZE =  600
window = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
clock = pygame.time.Clock()

# cube points inicial location
SIZE_X = 1
SIZE_Y = 0.5
SIZE_Z = 1.5
cube_points = pygameOp.get_3d_object_points(SIZE_X, SIZE_Y, SIZE_Z)

orientation_points = pygameOp.get_orientation_points()


imuConfiguration = {
    "disableCompass": True,
    "disableGyro": False,
    "disableAccelerometer": False,
    "gyroAutoCalib": True,
    "filterMode": 1,
    "tareSensor": True,
    "logical_ids": [8],
    "streaming_commands": [2, 255, 255, 255, 255, 255, 255, 255]
}
serial_port = serialOp.initializeImu(imuConfiguration)

# Main Loop
SCALE = 100

# set the pygame window name
pygame.display.set_caption('IMU 3D Visualization')


# Initialize rotation matrix
rotation_matrix = np.array([[0,0,0], [0,0,0], [0,0,0]])

texts_dict = [
    {
        "text": "X axis",
        "color": pygameOp.RED_RGB,
        "position": (20, 20)
    },
    {
        "text": "Y axis",
        "color": pygameOp.GREEN_RGB,
        "position": (20, 50)
    },
    {
        "text": "Z axis",
        "color": pygameOp.CYAN_RGB,
        "position": (20, 80)
    },
    {
        "text": "Press t to tare.",
        "color": pygameOp.WHITE_RGB,
        "position": (20, WINDOW_SIZE-40)
    }
]

while True:

    try:
        clock.tick(60)
        window.fill((0,0,0))

        pygameOp.draw_texts(window, texts_dict)
        
        #draw cube points
        points = [0 for _ in range(len(cube_points))]
        pygameOp.draw_cube_points(
            window, 
            cube_points,
            rotation_matrix,
            points,
            SCALE,
            WINDOW_SIZE
        )
        # draw orientation points
        o_points, orientation_colors = pygameOp.draw_orientation_points(
            window,
            rotation_matrix,
            orientation_points,
            SCALE,
            WINDOW_SIZE
        )

        # Draw lines between points
        pygameOp.connect_cube_points(window, points, pygame, pygameOp.WHITE_RGB)
        pygameOp.connect_orientation_points(window, o_points, pygame, orientation_colors)

        # Update rotation matrix if there are data
        print("running...")
        bytes_to_read = serial_port.inWaiting()
        if(bytes_to_read > 0):
            data = serial_port.read(bytes_to_read)
            if data[0] != 0:
                continue
            extracted_data = serialOp.extractRotationMatrix(data)
            rotation_matrix = extracted_data['rotation_matrix']

        # Event user event handling handling
        for event in pygame.event.get():
            # Get qui event
            if event.type == pygame.QUIT:
                pygame.quit()
                raise KeyboardInterrupt

            # Tare sensor
            keys = pygame.key.get_pressed()
            if keys[pygame.K_t]:
                serialOp.tareSensor(serial_port, imuConfiguration['logical_ids'])
        
        # Update pygame display
        pygame.display.update()
    
    except KeyboardInterrupt:
        print(CYAN, "Keyboard finished execution.", RESET)
        print(GREEN, "Stop streaming.", RESET)
        serial_port = serialOp.stopStreaming(serial_port, imuConfiguration['logical_ids'])
        break
    except Exception:
        print(RED, "Unexpected exception occured.", RESET)
        print(GREEN, "Stop streaming.", RESET)
        serial_port = serialOp.stopStreaming(serial_port, imuConfiguration['logical_ids'])
        break