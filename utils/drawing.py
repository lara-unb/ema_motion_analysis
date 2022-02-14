import numpy as np
import cv2

linewidth = 2
circle_radius = 3

def draw_keypoints(frame, keypoints):
    y, x, c = frame.shape
    for kp in keypoints:
        kx, ky = kp
        if(not np.isnan(kx) or not np.isnan(ky)):
            cv2.circle(frame, (int(kx), int(ky)), circle_radius, (0,255,0), -1)

def draw_connections(frame, keypoints, edges):
    for edge, color in edges.items():
        p1, p2 = edge
        x1, y1 = keypoints[p1]
        x2, y2 = keypoints[p2]
        
        cv2.line(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0,0,0), linewidth)