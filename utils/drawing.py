from matplotlib import colors
import numpy as np
import cv2

import colors

LINEWIDTH_RATIO = 300
CIRCLE_RATIO = 200

#-------------------------------------------------------------------------------------
# Function to draw points in the specified joints in each frame
def draw_keypoints(frame, keypoints):
    y, x, c = frame.shape
    circle_radius = int(y/CIRCLE_RATIO)
    print(frame.shape)
    for kp in keypoints:
        kx, ky = kp
        if(not np.isnan(kx) and not np.isnan(ky)): # Alterei isso aqui para AND -> OR não fazia sentido!!!
            cv2.circle(frame, (int(kx), int(ky)), circle_radius, (0,255,0), -1)
        

#-------------------------------------------------------------------------------------
# Function to draw lines in the specified parings in each frame
def draw_connections(frame, keypoints, edges):
    y, x, c = frame.shape
    linewidth = int(y/LINEWIDTH_RATIO)
    
    for edge, color in edges.items():
        p1, p2 = edge
        x1, y1 = keypoints[p1]
        x2, y2 = keypoints[p2]

        if(not np.isnan(x1) and not np.isnan(x2) and not np.isnan(y1) and not np.isnan(y2)): 
            cv2.line(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0,0,0), linewidth)

#-------------------------------------------------------------------------------------
