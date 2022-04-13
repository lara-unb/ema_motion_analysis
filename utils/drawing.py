""" This module defines functions to draw in the output video

"""

from matplotlib import colors
import numpy as np
import cv2

import colors

LINEWIDTH_RATIO = 280
CIRCLE_RATIO = 170

def draw_keypoints(frame, keypoints):
    """ Draw the keypoints in the specified frame

    Args:
        frame: frame of the video
        keypoints: vector with the x and y orientation of each point to 
            be drawn
        
    """
    y, x, c = frame.shape
    circle_radius = int(y/CIRCLE_RATIO)
    for kp in keypoints:
        kx, ky = kp
        if not np.isnan(kx) and not np.isnan(ky): 
            cv2.circle(frame, 
                       (int(kx), int(ky)), 
                       circle_radius, 
                       (255,255,0), 
                       -1)
        

def draw_connections(frame, selected_joints, keypoints_connections):
    """ Draw the keypoint connections in the specified frame

    Args:
        frame: frame of the video
        selected_joints: vactor with the x and y orientation of each keypoint
        keypoints_connections: dict with the keypoint pairs to be connected
        
    """
    y, x, c = frame.shape
    linewidth = int(y/LINEWIDTH_RATIO)
    for edge, color in keypoints_connections.items():
        p1, p2 = edge
        x1, y1 = selected_joints[p1]
        x2, y2 = selected_joints[p2]

        if (not np.isnan(x1) 
            and not np.isnan(x2) 
            and not np.isnan(y1) 
            and not np.isnan(y2)): 
            
            cv2.line(frame, 
                     (int(x1), int(y1)), 
                     (int(x2), int(y2)), 
                     (128,0,255), 
                     linewidth)


def write_angles_legends(frame, _angles, dict_profile_angles):
    """ Write the angle values in the video frame

    Args:
        frame: frame of the video
        _angles: vector with the angle values
        dict_profile_angles: dict with the selected angle profile
        
    """
    height_offset = 0
    for index in range(len(dict_profile_angles.keys())):
        text = list(dict_profile_angles.keys())[index] + " : " + str(round(_angles[index], 1))
        cv2.putText(frame, 
                    text, 
                    (40,50 + height_offset), 
                    cv2.FONT_HERSHEY_COMPLEX_SMALL, 
                    1.5, 
                    (128,0,255), 
                    2)
        height_offset += 40
        