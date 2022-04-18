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
PINK_RGB = (255, 203, 219)
YELLOW_RGB = (252, 247, 135) 


# Matrix to project a 3D object in 2D
PROJECTION_MATRIX = [
    [1,0,0],
    [0,1,0],
    [0,0,0],
]


def get_3d_object_points(size_x, size_y, size_z):
    """ Get 3D object point 

    Args:
        size_x: float with the x point location
        size_y: float with the y point location
        size_z: float with the z point location
    
    Return:
        objectPoints: vector with the (x, y, z) location of each point (8)
        
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

def get_orientation_points():
    """ Get 3D Orientation points 

    Return:
        orientation_points: vector with the (x, y, z) location of each 
            orientation (center, x, y, z) and their arrows
        
    """

    # center -> orientation_points[0]
    # x axis -> orientation_points[1]
    # y axis -> orientation_points[2]
    # z axis -> orientation_points[3]
    # first vector: end of orientation arrow
    # second, third and fourth vectors: points used to draw the arrow
    #                                       with the draw_polygon function
    orientation_points = [n for n in range(4)]
    orientation_points[0] = [
                                [[0], [0], [0]], # center point -> does not have arrow
                                [[0], [0], [0]], 
                                [[0], [0], [0]], 
                                [[0], [0], [0]],
                            ] #center

    orientation_points[1] = [
                                [[-2], [0], [0]],           # end of orientation arrow
                                [[-2+0.07], [0.05], [0]],   # arrow point 1
                                [[-2+0.07], [-0.05], [0]],  # arrow point 2
                                [[-2+0.07], [0], [-0.05]],  # arrow point 3
                            ]  # x axis

    orientation_points[2] = [
                                [[0], [-2], [0]],           # end of orientation arrow
                                [[0], [-2+0.07], [-0.05]],  # arrow point 1
                                [[0], [-2+0.07], [0.05]],   # arrow point 2
                                [[-0.05], [-2+0.07], [0]],  # arrow point 3
                            ]  # y axis

    orientation_points[3] = [
                                [[0], [0], [-2]],           # end of orientation arrow
                                [[0.05], [0], [-2+0.07]],   # arrow point 1
                                [[-0.05], [0], [-2+0.07]],  # arrow point 2
                                [[0], [-0.05], [-2+0.07]],  # arrow point 3
                            ]  # z axis

    return orientation_points

def get_rotated_orientation_points(projection_matrix, 
                                   rotation_matrix, 
                                   point, 
                                   scale, 
                                   offset_x,
                                   offset_y):
    """ Get rotaded orientation arrow points 

    Args: 
        projection_matrix: matrix used to project a 3D object in 2D
        rotation_matrix: matrix to rotate the 3D object
        point: victor of points to be rotated
        scale: constant used to scale the image 
        WINDOW_SIZE: pygame window size (constant)
    Return:
        x: x location of the edge of the orientation axis
        y: y location of the edge of the orientation axis
        x1: x location of the 1st arrow point of the orientation axis
        y1: y location of the 1st arrow point of the orientation axis
        x2: x location of the 2nd arrow point of the orientation axis
        y2: y location of the 2nd arrow point of the orientation axis
        x3: x location of the 3rd arrow point of the orientation axis
        y3: y location of the 3rd arrow point of the orientation axis
        
    """

    #center and edge points
    rotated_point = np.matmul(rotation_matrix, point[0])
    point_2d = np.matmul(projection_matrix, rotated_point)
    x = (point_2d[0][0] * scale) + offset_x
    y = (point_2d[1][0] * scale) + offset_y
    
    #1st arrow point of the orientation axis
    rotated_point = np.matmul(rotation_matrix, point[1])
    point_2d = np.matmul(projection_matrix, rotated_point)
    x1 = (point_2d[0][0] * scale) + offset_x
    y1 = (point_2d[1][0] * scale) + offset_y

    #2nd arrow point of the orientation axis
    rotated_point = np.matmul(rotation_matrix, point[2])
    point_2d = np.matmul(projection_matrix, rotated_point)
    x2 = (point_2d[0][0] * scale) + offset_x
    y2 = (point_2d[1][0] * scale) + offset_y

    #3rd arrow point of the orientation axis
    rotated_point = np.matmul(rotation_matrix, point[3])
    point_2d = np.matmul(projection_matrix, rotated_point)
    x3 = (point_2d[0][0] * scale) + offset_x
    y3 = (point_2d[1][0] * scale) + offset_y
    
    return x, y, x1, y1, x2, y2, x3, y3

def connect_cube_points(window, points, color):
    """ Draw cube connections 

    Args: 
        window: pygame window to draw the connections
        point: vector of points to be connected
        color: color of the connection line

    """
    connect_point(window, 0, 1, points, color)
    connect_point(window, 0, 3, points, color)
    connect_point(window, 0, 4, points, color)
    connect_point(window, 1, 2, points, color)
    connect_point(window, 1, 5, points, color)
    connect_point(window, 2, 6, points, color)
    connect_point(window, 2, 3, points, color)
    connect_point(window, 3, 7, points, color)
    connect_point(window, 4, 5, points, color)
    connect_point(window, 4, 7, points, color)
    connect_point(window, 6, 5, points, color)
    connect_point(window, 6, 7, points, color)

#draw orientation arrows conections
def connect_orientation_points(window, points, colors):
    """ Draw orientation axis connections 

    Args: 
        window: pygame window to draw the connections
        point: vector of points to be connected
        color: color of the connection line

    """
    connect_point(window, 0, 1, points, colors[0])
    connect_point(window, 0, 2, points, colors[1])
    connect_point(window, 0, 3, points, colors[2])

def connect_point(window, i, j, points, color):
    """ Draw connection between 2 points 

    Args: 
        window: pygame window to draw the connections
        i: point 1 index
        j: point 2 index
        points: vector of points to be connected
        color: color of the connection line

    """
    pygame.draw.line(window, 
                     color, 
                     (points[i][0], points[i][1]), 
                     (points[j][0], points[j][1]))


def draw_texts(window, texts:dict):
    """ Draw text in pygame window 

    Args: 
        window: pygame window to draw the connections
        texts: dict of the texts and their positions

    """
    for textValue in texts:
        text =  Font.render(textValue['text'], True, textValue['color'])
        window.blit(text, textValue['position'])

def draw_orientation_points(window, 
                            rotation_matrix, 
                            orientation_points, 
                            SCALE, 
                            offset_x,
                            offset_y):
    """ Draw orienentation axis edge ponits 

    Args: 
        window: pygame window to draw the connections
        rotation_matrix: rotation matrix used to multiply each point
        orientation_points: edge points of the orientation axis
        SCALE: constant int to scale the drawing
        offset_x: x position representing the center of the orientation axis
        offset_y: y position representing the center of the orientation axis

    Return:
        o_points: rotaded edge points of orientation axis (tuple vector)
        orientation_colors: vector with the color of each orientation axis

    """                 
    orientation_colors = [RED_RGB, GREEN_RGB, CYAN_RGB]
    o_points = [0 for _ in range(len(orientation_points))]
    i = 0
    for point in orientation_points:
    
        # points to draw the arrow -------------------------------
        x, y, x1, y1, x2, y2, x3, y3 = get_rotated_orientation_points(
            PROJECTION_MATRIX,
            rotation_matrix,
            point,
            SCALE,
            offset_x,
            offset_y,
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

def draw_cube_points(window, 
                     cube_points, 
                     rotation_matrix, 
                     points, 
                     SCALE, 
                     offset_x,
                     offset_y, 
                     color):
    """ Draw cube points 

    Args: 
        window: pygame window to draw the connections
        cube_points: vector with the location of each cube point
        rotation_matrix: rotation matrix used to multiply each point
        ponits: vector of zeros to be filled with the rotaded cube points
        SCALE: constant int to scale the drawing
        offset_x: x position representing the center of the orientation axis
        offset_y: y position representing the center of the orientation axis
        color: color of the cube ponits

    """     
    i = 0
    for point in cube_points:
        # rotate point
        rotated_point = np.matmul(rotation_matrix, point)
        # project 3d point in 2d
        point_2d = np.matmul(PROJECTION_MATRIX, rotated_point)
        x = (point_2d[0][0] * SCALE) + offset_x
        y = (point_2d[1][0] * SCALE) + offset_y

        points[i] = (x,y)
        i += 1
        # draw cube edge
        pygame.draw.circle(window, color, (x, y), 5)


def render_information(window, 
                       texts_dict, 
                       cube_points, 
                       rotation_matrix, 
                       SCALE, 
                       offset_x,
                       offset_y,
                       orientation_points,
                       color):
    """ Show cube drawing and text in the window 

    Args: 
        window: pygame window to draw the connections
        texts_dict: dict of the texts and their positions
        cube_points: vector with the location of each cube point
        rotation_matrix: rotation matrix used to multiply each point
        ponits: vector of zeros to be filled with the rotaded cube points
        SCALE: constant int to scale the drawing
        offset_x: x position representing the center of the orientation axis
        offset_y: y position representing the center of the orientation axis
        orientation_points: edge points of the orientation axis
        color: color of the cube ponits

    """    
    draw_texts(window, texts_dict)
        
    #draw cube points
    points = [0 for _ in range(len(cube_points))]
    draw_cube_points(
        window, 
        cube_points,
        rotation_matrix,
        points,
        SCALE,
        offset_x,
        offset_y,
        color,
    )
    # draw orientation points
    o_points, orientation_colors = draw_orientation_points(
        window,
        rotation_matrix,
        orientation_points,
        SCALE,
        offset_x,
        offset_y,
    )

    # Draw lines between points
    connect_cube_points(window, points, color)
    connect_orientation_points(window, o_points, orientation_colors)