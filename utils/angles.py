import numpy as np
import math


def getAngleLimited(A, B, O, allow_neg=False):
    if allow_neg:
        try:
            ang = math.degrees(math.atan2(
                B[1]-O[1], B[0]-O[0]) - math.atan2(A[1]-O[1], A[0]-O[0]))
            if ang > 180:
                ang = 360 - ang
        except:
            ang = np.nan
    else:
        try:
            ang = math.degrees(math.atan2(
                B[1]-O[1], B[0]-O[0]) - math.atan2(A[1]-O[1], A[0]-O[0]))
            if ang < 0:
                ang += 360
            if ang > 180:
                ang = 360 - ang
        except:
            ang = np.nan
    return ang

def getAngles(selected_keypoints, dict_angles, profile, pose_selected):

    selected_keypoints = np.array(selected_keypoints)
    angles = np.zeros(len(selected_keypoints))

    print(selected_keypoints)
    print(dict_angles)
    print(profile)
    print(pose_selected)
    angle_points = []
    for angle in dict_angles[profile].keys():
        for point in dict_angles[profile][angle]:
            index_keypoints = pose_selected.index(point)
            angle_points.append(selected_keypoints[index_keypoints])
    
    angles = getAngleLimited(angle_points[0], angle_points[2], angle_points[1])

    return angles
