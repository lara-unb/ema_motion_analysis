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
window = pygame.display.set_mode( (WINDOW_SIZE, WINDOW_SIZE) )
clock = pygame.time.Clock()

# matrix to project 3D element in 2D
projection_matrix = [
    [1,0,0],
    [0,1,0],
    [0,0,0]
]

# cube points inicial location
SIZE_X = 1
SIZE_Y = 0.5
SIZE_Z = 1.5
cube_points = [n for n in range(8)]
cube_points[0] = [[-SIZE_X], [-SIZE_Y], [SIZE_Z]]
cube_points[1] = [[SIZE_X],[-SIZE_Y],[SIZE_Z]]
cube_points[2] = [[SIZE_X],[SIZE_Y],[SIZE_Z]]
cube_points[3] = [[-SIZE_X],[SIZE_Y],[SIZE_Z]]
cube_points[4] = [[-SIZE_X],[-SIZE_Y],[-SIZE_Z]]
cube_points[5] = [[SIZE_X],[-SIZE_Y],[-SIZE_Z]]
cube_points[6] = [[SIZE_X],[SIZE_Y],[-SIZE_Z]]
cube_points[7] = [[-SIZE_X],[SIZE_Y],[-SIZE_Z]]

# center -> orientation_points[0]
# x axis -> orientation_points[1]
# y axis -> orientation_points[2]
# z axis -> orientation_points[3]
# first vector: end of orientation arrow
# second, third and fourth vectors: points to draw the arrow
orientation_points = [n for n in range(4)]
orientation_points[0] = [[0], [0], [0]], [[0], [0], [0]], [[0], [0], [0]], [[0], [0], [0]] #center
orientation_points[1] = [[2], [0], [0]], [[2-0.07], [0.05], [0]], [[2-0.07], [-0.05], [0]], [[2-0.07], [0], [-0.05]]       # x axis
orientation_points[2] = [[0], [-2], [0]], [[0], [-2+0.07], [-0.05]], [[0], [-2+0.07], [0.05]], [[-0.05], [-2+0.07], [0]]   # y axis
orientation_points[3] = [[0], [0], [-2]], [[0.05], [0], [-2+0.07]], [[-0.05], [0], [-2+0.07]], [[0], [-0.05], [-2+0.07]]   # z axis

RED_RGB = (255, 0, 0)
GREEN_RGB = (0, 255, 0)
CYAN_RGB = (0, 255, 255) 
WHITE_RGB = (255, 255, 255) 

#draw cube connections
def connect_points(points, pygame, color):
        connect_point(0, 1, points, pygame, color)
        connect_point(0, 3, points, pygame, color)
        connect_point(0, 4, points, pygame, color)
        connect_point(1, 2, points, pygame, color)
        connect_point(1, 5, points, pygame, color)
        connect_point(2, 6, points, pygame, color)
        connect_point(2, 3, points, pygame, color)
        connect_point(3, 7, points, pygame, color)
        connect_point(4, 5, points, pygame, color)
        connect_point(4, 7, points, pygame, color)
        connect_point(6, 5, points, pygame, color)
        connect_point(6, 7, points, pygame, color)

#draw orientation arrows conections
def connect_orientation_points(points, pygame, colors):
        connect_point(0, 1, points, pygame, colors[0])
        connect_point(0, 2, points, pygame, colors[1])
        connect_point(0, 3, points, pygame, colors[2])

# connect 2 points
def connect_point(i, j, points, pygame, color):
    pygame.draw.line(window, color, (points[i][0], points[i][1]) , (points[j][0], points[j][1]))

configDict = {
    "disableCompass": True,
    "disableGyro": False,
    "disableAccelerometer": False,
    "gyroAutoCalib": True,
    "filterMode": 1,
    "tareSensor": True,
    "logical_ids": [8],
    "streaming_commands": [2, 255, 255, 255, 255, 255, 255, 255]
}
serial_port = serialOeratserialOperations as serialOpp.initializeImu(configDict)

# Main Loop
scale = 100
angle_x = angle_y = angle_z = 0

# set the pygame window name
pygame.display.set_caption('IMU 3D Visualization')

# create a font object.
pygame.font.init()
Font = pygame.font.SysFont('didot.ttc',  30)

# Initialize rotation matrix
rotation_matrix = np.array([[0,0,0], [0,0,0], [0,0,0]])

while True:

    try:
        clock.tick(60)
        window.fill((0,0,0))

        # create a text surface object,
        # on which text is drawn on it.
        text1 = Font.render('X axis', True, RED_RGB)
        text2 = Font.render('Y axis', True, GREEN_RGB)
        text3 = Font.render('Z axis', True, CYAN_RGB)
        text4 = Font.render('Press t to tare.', True, WHITE_RGB)

        # copying the text surface object to the display surface object
        # at the specified coodinate
        window.blit(text1, (20, 20))
        window.blit(text2, (20, 50))
        window.blit(text3, (20, 80))
        window.blit(text4, (20, WINDOW_SIZE-40))
    
        
        #draw cube points
        points = [0 for _ in range(len(cube_points))]
        i = 0

        for point in cube_points:
            rotated_point = np.matmul(rotation_matrix, point)
            point_2d = np.matmul(projection_matrix, rotated_point)
        
            x = (point_2d[0][0] * scale) + WINDOW_SIZE/2
            y = (point_2d[1][0] * scale) + WINDOW_SIZE/2

            points[i] = (x,y)
            i += 1
            pygame.draw.circle(window, CYAN_RGB, (x, y), 5)

        # draw orientation points
        orientation_colors = [RED_RGB, GREEN_RGB, CYAN_RGB]
        o_points = [0 for _ in range(len(orientation_points))]
        i = 0
        for point in orientation_points:
            
            #center and edge points
            rotated_point = np.matmul(rotation_matrix, point[0])
            point_2d = np.matmul(projection_matrix, rotated_point)
            x = (point_2d[0][0] * scale) + WINDOW_SIZE/2
            y = (point_2d[1][0] * scale) + WINDOW_SIZE/2


            # points to draw the arrow -------------------------------
            rotated_point = np.matmul(rotation_matrix, point[1])
            point_2d = np.matmul(projection_matrix, rotated_point)
            x1 = (point_2d[0][0] * scale) + WINDOW_SIZE/2
            y1 = (point_2d[1][0] * scale) + WINDOW_SIZE/2


            rotated_point = np.matmul(rotation_matrix, point[2])
            point_2d = np.matmul(projection_matrix, rotated_point)
            x2 = (point_2d[0][0] * scale) + WINDOW_SIZE/2
            y2 = (point_2d[1][0] * scale) + WINDOW_SIZE/2

            rotated_point = np.matmul(rotation_matrix, point[3])
            point_2d = np.matmul(projection_matrix, rotated_point)
            x3 = (point_2d[0][0] * scale) + WINDOW_SIZE/2
            y3 = (point_2d[1][0] * scale) + WINDOW_SIZE/2
            # END - points to draw the arrow --------------------------

            o_points[i] = (x,y)
            #draw the arow polygon
            if i > 0:
                pygame.draw.polygon(window, orientation_colors[i-1], [(x, y), (x1, y1), (x2, y2), (x3, y3)], width=0)
            
            i += 1

        # Draw lines between points
        connect_points(points, pygame, WHITE_RGB)
        connect_orientation_points(o_points, pygame, orientation_colors)

        print("running...")
        bytes_to_read = serial_port.inWaiting()
        print(bytes_to_read)
        if(bytes_to_read > 0):
            data = serial_port.read(bytes_to_read)
            if data[0] != 0:
                continue

            extracted_data = serialOeratserialOperations as serialOpp.extractRotationMatrix(data)
            rotation_matrix = extracted_data['rotation_matrix']

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise KeyboardInterrupt
            
            keys = pygame.key.get_pressed()

            # Tare sensor
            if keys[pygame.K_t]:
                serialOeratserialOperations as serialOpp.tareSensor(serial_port, configDict['logical_ids'])
            
        pygame.display.update()
    except KeyboardInterrupt:
        print(CYAN, "Keyboard finished execution.", RESET)
        print(RED, "Stop streaming.", RESET)
        serial_port = serialOeratserialOperations as serialOpp.stopStreaming(serial_port, configDict['logical_ids'])
        break