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

def connect_points(points, pygame):
        connect_point(0, 1, points, pygame)
        connect_point(0, 3, points, pygame)
        connect_point(0, 4, points, pygame)
        connect_point(1, 2, points, pygame)
        connect_point(1, 5, points, pygame)
        connect_point(2, 6, points, pygame)
        connect_point(2, 3, points, pygame)
        connect_point(3, 7, points, pygame)
        connect_point(4, 5, points, pygame)
        connect_point(4, 7, points, pygame)
        connect_point(6, 5, points, pygame)
        connect_point(6, 7, points, pygame)
def connect_point(i, j, points, pygame):
    pygame.draw.line(window, (255, 255, 255), (points[i][0], points[i][1]) , (points[j][0], points[j][1]))


# End - Set visual configurations ---------------------------------------------------------------------------


logical_ids = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14]

# Find and open serial port for the IMU dongle
serial_port = serialOperations.getDongleObject()


# Stop streaming
serial_port = serialOperations.stopStreaming(serial_port, logical_ids)

# Manual flush. Might not be necessary
# serial_port = serialOperations.manualFlush(serial_port)

print('Starting configuration')

# Setting streaming slots, this means that while streaming sensors will send
# this data to the dongle as in page 29 - User manual: 
# 0 - Differential quaternions; 
# 41 - Raw accelerations; 
# 255 - No data
commands = [0, 1, 255, 255, 255, 255, 255, 255]
serial_port = serialOperations.setStreamingSlots(serial_port, logical_ids, commands)

# Set magnetometer(explain it better), calibGyro if calibGyro=True and Tare sensor
configDict = {
            "unableCompass": True,
            "unableGyro": False,
            "unableAccelerometer": False,
            "gyroAutoCalib": True,
            "filterMode": 1,
            "tareSensor": True
}
serial_port = serialOperations.configureSensor(serial_port, logical_ids, configDict)

# Start streaming
serial_port = serialOperations.startStreaming(serial_port, logical_ids)

# Main Loop
scale = 100
angle_x = angle_y = angle_z = 0

while True:

    try:
        clock.tick(60)
        window.fill((0,0,0))

    
        rotation_x = R.from_euler('x', angle_x)
        rotation_y = R.from_euler('y', angle_y)
        rotation_z = R.from_euler('z', angle_z)

        print('ROTATION MATRIX X: ', rotation_x.as_matrix())

        points = [0 for _ in range(len(cube_points))]
        i = 0

        for point in cube_points:

            rotate_x = np.matmul(rotation_x.as_matrix(), point)
            rotate_y = np.matmul(rotation_y.as_matrix(), rotate_x)
            rotate_z = np.matmul(rotation_z.as_matrix(), rotate_y)
            point_2d = np.matmul(projection_matrix, rotate_z)
        
            x = (point_2d[0][0] * scale) + WINDOW_SIZE/2
            y = (point_2d[1][0] * scale) + WINDOW_SIZE/2

            points[i] = (x,y)
            i += 1
            pygame.draw.circle(window, (255, 0, 0), (x, y), 5)

        # Draw lines between points
        connect_points(points, pygame)

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
        serial_port = serialOperations.stopStreaming(serial_port, logical_ids)