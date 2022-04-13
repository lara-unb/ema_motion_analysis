"""Functions to get the angles between joits.

"""

import numpy as np
import math

def get_angle_limited(A, B, O, allow_negagtive=False):
    """ Get angles limited to 180º

    Args:
        A: First Point
        B: Second Point
        O: Origin/Intersection point
        allow_negative: Boolean that says if the returned point could be
        negative
    Return:
        angle: angle in degrees
    """
    if allow_negagtive:
        try:
            angle = math.degrees(math.atan2(
                B[1]-O[1], B[0]-O[0]) - math.atan2(A[1]-O[1], A[0]-O[0]))
            if angle > 180:
                angle = 360 - angle
        except:
            angle = np.nan
    else:
        try:
            angle = math.degrees(math.atan2(
                B[1]-O[1], B[0]-O[0]) - math.atan2(A[1]-O[1], A[0]-O[0]))
            if angle < 0:
                angle += 360
            if angle > 180:
                angle = 360 - angle
        except:
            angle = np.nan
    return angle

def get_angles(selected_keypoints, dict_angles, pose_selected):
    """ Return angles desired based in a dictionary

    Args:
        selected_keypoints: points that should be processed
        dict_angles: dictionary with each angle that should be processed and the
        three points(poses) that define this angles.
        pose_selected: list of points for determined profile.
    
    Returns:
        angles: Angles in degrees
    """
    selected_keypoints = np.array(selected_keypoints)
    angles = np.zeros(len(selected_keypoints))
    angles = []

    for angle in dict_angles.keys():
        angle_points = []   
        for point in dict_angles[angle]:
            index_keypoints = pose_selected.index(point)
            angle_points.append(selected_keypoints[index_keypoints])
        
        angles.append(get_angle_limited(angle_points[0], 
                                       angle_points[2], 
                                       angle_points[1]))

    return angles
