"""Functions used for 3D IMU visualization

"""

import numpy as np
import pygame

# create a font object.
pygame.font.init()
Font = pygame.font.SysFont('didot.ttc',  30)

# Define constants for the colors used in the pygame window
RED_RGB = (255, 0, 0)
GREEN_RGB = (0, 255, 0)
CYAN_RGB = (0, 255, 255) 
WHITE_RGB = (255, 255, 255) 

# Matrix to project a 3D object in 2D
PROJECTION_MATRIX = [
    [1,0,0],
    [0,1,0],
    [0,0,0]
]


def get_3d_object_points(size_x, size_y, size_z):
    """ Get 3D object point 

    Args:
        size_x: float 
        size_y: 
        size_z: 
    
    Return:
        objectPoints: 
        

    """
    objectPoints = [n for n in range(8)]
    objectPoints[0] = [[-size_x], [-size_y], [size_z]]
    objectPoints[1] = [[size_x],[-size_y],[size_z]]
    objectPoints[2] = [[size_x],[size_y],[size_z]]
    objectPoints[3] = [[-size_x],[size_y],[size_z]]
    objectPoints[4] = [[-size_x],[-size_y],[-size_z]]
    objectPoints[5] = [[size_x],[-size_y],[-size_z]]
    objectPoints[6] = [[size_x],[size_y],[-size_z]]
    objectPoints[7] = [[-size_x],[size_y],[-size_z]]
    return objectPoints

# center -> orientation_points[0]
# x axis -> orientation_points[1]
# y axis -> orientation_points[2]
# z axis -> orientation_points[3]
# first vector: end of orientation arrow
# second, third and fourth vectors: points to draw the arrow
def get_orientation_points():
    orientation_points = [n for n in range(4)]
    orientation_points[0] = [[0], [0], [0]], [[0], [0], [0]], [[0], [0], [0]], [[0], [0], [0]] #center
    orientation_points[1] = [[-2], [0], [0]], [[-2+0.07], [0.05], [0]], [[-2+0.07], [-0.05], [0]], [[-2+0.07], [0], [-0.05]]   # x axis
    orientation_points[2] = [[0], [-2], [0]], [[0], [-2+0.07], [-0.05]], [[0], [-2+0.07], [0.05]], [[-0.05], [-2+0.07], [0]]   # y axis
    orientation_points[3] = [[0], [0], [-2]], [[0.05], [0], [-2+0.07]], [[-0.05], [0], [-2+0.07]], [[0], [-0.05], [-2+0.07]]   # z axis
    return orientation_points

def get_points_to_draw_arrows(projection_matrix, rotation_matrix, point, scale, WINDOW_SIZE):
    #center and edge points
    rotated_point = np.matmul(rotation_matrix, point[0])
    point_2d = np.matmul(projection_matrix, rotated_point)
    x = (point_2d[0][0] * scale) + WINDOW_SIZE/2
    y = (point_2d[1][0] * scale) + WINDOW_SIZE/2
    
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
    
    return x, y, x1, y1, x2, y2, x3, y3

#draw cube connections
def connect_cube_points(window, points, pygame, color):
        connect_point(window, 0, 1, points, pygame, color)
        connect_point(window, 0, 3, points, pygame, color)
        connect_point(window, 0, 4, points, pygame, color)
        connect_point(window, 1, 2, points, pygame, color)
        connect_point(window, 1, 5, points, pygame, color)
        connect_point(window, 2, 6, points, pygame, color)
        connect_point(window, 2, 3, points, pygame, color)
        connect_point(window, 3, 7, points, pygame, color)
        connect_point(window, 4, 5, points, pygame, color)
        connect_point(window, 4, 7, points, pygame, color)
        connect_point(window, 6, 5, points, pygame, color)
        connect_point(window, 6, 7, points, pygame, color)

#draw orientation arrows conections
def connect_orientation_points(window, points, pygame, colors):
        connect_point(window, 0, 1, points, pygame, colors[0])
        connect_point(window, 0, 2, points, pygame, colors[1])
        connect_point(window, 0, 3, points, pygame, colors[2])

# connect 2 points
def connect_point(window, i, j, points, pygame, color):
    pygame.draw.line(window, color, (points[i][0], points[i][1]) , (points[j][0], points[j][1]))


# Draw texts
def draw_texts(window, texts:dict):
    for textValue in texts:
        text =  Font.render(textValue['text'], True, textValue['color'])
        window.blit(text, textValue['position'])

# Essa função retornar é feio :( 
def draw_orientation_points(window, rotation_matrix, orientation_points, SCALE, WINDOW_SIZE):
    orientation_colors = [RED_RGB, GREEN_RGB, CYAN_RGB]
    o_points = [0 for _ in range(len(orientation_points))]
    i = 0
    for point in orientation_points:
    
        # points to draw the arrow -------------------------------
        x, y, x1, y1, x2, y2, x3, y3 = get_points_to_draw_arrows(
            PROJECTION_MATRIX,
            rotation_matrix,
            point,
            SCALE,
            WINDOW_SIZE
        )

        o_points[i] = (x,y)
        #draw the arow polygon
        if i > 0:
            pygame.draw.polygon(window, 
            orientation_colors[i-1], 
            [(x, y), (x1, y1), (x2, y2), (x3, y3)], 
            width=0)
        
        i += 1
    return o_points, orientation_colors
def draw_cube_points(window, cube_points, rotation_matrix, points, SCALE, WINDOW_SIZE):
    i = 0
    for point in cube_points:
        rotated_point = np.matmul(rotation_matrix, point)
        point_2d = np.matmul(PROJECTION_MATRIX, rotated_point)
    
        x = (point_2d[0][0] * SCALE) + WINDOW_SIZE/2
        y = (point_2d[1][0] * SCALE) + WINDOW_SIZE/2

        points[i] = (x,y)
        i += 1
        pygame.draw.circle(window, CYAN_RGB, (x, y), 5)


def render_information(window, 
                       texts_dict, 
                       cube_points, 
                       rotation_matrix, 
                       SCALE, 
                       WINDOW_SIZE,
                       orientation_points):
    draw_texts(window, texts_dict)
        
    #draw cube points
    points = [0 for _ in range(len(cube_points))]
    draw_cube_points(
        window, 
        cube_points,
        rotation_matrix,
        points,
        SCALE,
        WINDOW_SIZE
    )
    # draw orientation points
    o_points, orientation_colors = draw_orientation_points(
        window,
        rotation_matrix,
        orientation_points,
        SCALE,
        WINDOW_SIZE
    )

    # Draw lines between points
    connect_cube_points(window, points, pygame, WHITE_RGB)
    connect_orientation_points(window, o_points, pygame, orientation_colors)