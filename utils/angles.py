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

def getAngles(kp_vec):
    kp_vec = np.array(kp_vec)
    angles = np.zeros(len(kp_vec))
    angles = getAngleLimited(kp_vec[0], kp_vec[2], kp_vec[1])
    return angles
