import pygame
from math import *
import numpy as np
import serialOperations
from scipy.spatial.transform import Rotation as R
from colors import *

# Start - Set visual configurations ---------------------------------------------------------------------------
WINDOW_SIZE =  800
ROTATE_SPEED = 0.02
window = pygame.display.set_mode( (WINDOW_SIZE, WINDOW_SIZE) )
clock = pygame.time.Clock()

projection_matrix = [[1,0,0],
                     [0,1,0],
                     [0,0,0]]

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

def connect_points(i, j, points):
    pygame.draw.line(window, (255, 255, 255), (points[i][0], points[i][1]) , (points[j][0], points[j][1]))

def get_rotation_matrices(angle_x, angle_y, angle_z):
    rotation_x = [
        [1, 0, 0],
        [0, cos(angle_x), -sin(angle_x)],
        [0, sin(angle_x), cos(angle_x)]
    ]

    rotation_y = [
        [cos(angle_y), 0, sin(angle_y)],
        [0, 1, 0],
        [-sin(angle_y), 0, cos(angle_y)]
    ]

    rotation_z = [
        [cos(angle_z), -sin(angle_z), 0],
        [sin(angle_z), cos(angle_z), 0],
        [0, 0, 1]
    ]
    return rotation_x, rotation_y, rotation_z

# End - Set visual configurations ---------------------------------------------------------------------------


addresses = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14]

# Find and open serial port for the IMU dongle
serial_port = serialOperations.getDongleObject()


# Stop streaming
serial_port = serialOperations.stopStreaming(serial_port, addresses)

# Manual flush. Might not be necessary
serial_port = serialOperations.manualFlush(serial_port)

print('Starting configuration')

# Setting streaming slots, this means that while streaming sensors will send
# this data to the dongle as in page 29 - User manual: 
# 0 - Differential quaternions; 
# 41 - Raw accelerations; 
# 255 - No data
commands = [0, 1, 255, 255, 255, 255, 255, 255]
serial_port = serialOperations.setStreamingSlots(serial_port, addresses, commands)

# Set magnetometer(explain it better), calibGyro if calibGyro=True and Tare sensor
calibGyro = False
serial_port = serialOperations.configureSensor(serial_port, addresses, calibGyro)

# Show some sensor configuration
# serialOperations.getSensorInformation(serial_port, addresses)

# Start streaming
serial_port = serialOperations.startStreaming(serial_port, addresses)

# Main Loop
scale = 100
angle_x = angle_y = angle_z = 0

while True:

    try:
        clock.tick(60)
        window.fill((0,0,0))

        # rotate_x, rotate_y, rotate_z = get_rotation_matrices(angle_x, angle_y, angle_z)
        rotation_x = [
        [1, 0, 0],
        [0, cos(angle_x), -sin(angle_x)],
        [0, sin(angle_x), cos(angle_x)]
        ]

        rotation_y = [
            [cos(angle_y), 0, sin(angle_y)],
            [0, 1, 0],
            [-sin(angle_y), 0, cos(angle_y)]
        ]

        rotation_z = [
            [cos(angle_z), -sin(angle_z), 0],
            [sin(angle_z), cos(angle_z), 0],
            [0, 0, 1]
        ]
        points = [0 for _ in range(len(cube_points))]
        i = 0

        for point in cube_points:

            rotate_x = np.matmul(rotation_x, point)
            rotate_y = np.matmul(rotation_y, rotate_x)
            rotate_z = np.matmul(rotation_z, rotate_y)
            point_2d = np.matmul(projection_matrix, rotate_z)
        
            x = (point_2d[0][0] * scale) + WINDOW_SIZE/2
            y = (point_2d[1][0] * scale) + WINDOW_SIZE/2

            points[i] = (x,y)
            i += 1
            pygame.draw.circle(window, (255, 0, 0), (x, y), 5)

        connect_points(0, 1, points)
        connect_points(0, 3, points)
        connect_points(0, 4, points)
        connect_points(1, 2, points)
        connect_points(1, 5, points)
        connect_points(2, 6, points)
        connect_points(2, 3, points)
        connect_points(3, 7, points)
        connect_points(4, 5, points)
        connect_points(4, 7, points)
        connect_points(6, 5, points)
        connect_points(6, 7, points)


        print("running...")
        bytes_to_read = serial_port.inWaiting()

        if(bytes_to_read > 0):

            data = serial_port.read(bytes_to_read)
            if len(data) <= 3 or data[0] != 0:
                continue

            extracted_data = serialOperations.extractResponse(data)

            rot = R.from_quat([extracted_data['x'], extracted_data['y'],extracted_data['z'], extracted_data['w']])
            euler_angles_scipy = rot.as_euler('xyz', degrees=False)
            
            # Coment this to debug
            angle_x = euler_angles_scipy[0]
            angle_y = euler_angles_scipy[1]
            angle_z = euler_angles_scipy[2]

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise KeyboardInterrupt
            
            keys = pygame.key.get_pressed()

            # Retorna o gráfico para posição inicial
            if keys[pygame.K_r]:
                angle_y = angle_x = angle_z = 0  
            

            # Uncoment this to debug

            # if keys[pygame.K_a]:
            #     angle_y += ROTATE_SPEED
            # if keys[pygame.K_d]:
            #     angle_y -= ROTATE_SPEED      
            # if keys[pygame.K_w]:
            #     angle_x += ROTATE_SPEED
            # if keys[pygame.K_s]:
            #     angle_x -= ROTATE_SPEED
            # if keys[pygame.K_q]:
            #     angle_z -= ROTATE_SPEED
            # if keys[pygame.K_e]:
            #     angle_z += ROTATE_SPEED 
            
        pygame.display.update()
    except KeyboardInterrupt:
        print(CYAN, "Keyboard finished execution.", RESET)
        print(RED, "Stop streaming.", RESET)
        serial_port = serialOperations.stopStreaming(serial_port, addresses)