from matplotlib import colors
import numpy as np
import cv2

import colors

LINEWIDTH_RATIO = 280
CIRCLE_RATIO = 170

#-------------------------------------------------------------------------------------
# Function to draw points in the specified joints in each frame
def drawKeypoints(frame, keypoints):
    y, x, c = frame.shape
    circle_radius = int(y/CIRCLE_RATIO)
    for kp in keypoints:
        kx, ky = kp
        if(not np.isnan(kx) and not np.isnan(ky)): # Alterei isso aqui para AND -> OR não fazia sentido!!!
            cv2.circle(frame, (int(kx), int(ky)), circle_radius, (255,255,0), -1)
        

#-------------------------------------------------------------------------------------
# Function to draw lines in the specified parings in each frame
def drawConnections(frame, selected_joints, edges):
    y, x, c = frame.shape
    linewidth = int(y/LINEWIDTH_RATIO)
    for edge, color in edges.items():
        p1, p2 = edge
        x1, y1 = selected_joints[p1]
        x2, y2 = selected_joints[p2]

        if(not np.isnan(x1) and not np.isnan(x2) and not np.isnan(y1) and not np.isnan(y2)): 
            cv2.line(frame, (int(x1), int(y1)), (int(x2), int(y2)), (128,0,255), linewidth)

#-------------------------------------------------------------------------------------
