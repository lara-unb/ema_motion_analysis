"""Poses functions and informations

Functions and dicts used to select the key points, angles and connections
of the pose to be predicted.

"""

#general imports
from turtle import right
import numpy as np
import mediapipe as mp
import sys

sys.path.append("../utils/")
import colors

mp_pose = mp.solutions.pose

#Possible keypoints - movenet
KEYPOINT_DICT_MOVENET = {
    'nose':0,
    'left_eye':1,
    'right_eye':2,
    'left_ear':3,
    'right_ear':4,
    'left_shoulder':5,
    'right_shoulder':6,
    'left_elbow':7,
    'right_elbow':8,
    'left_wrist':9,
    'right_wrist':10,
    'left_hip':11,
    'right_hip':12,
    'left_knee':13,
    'right_knee':14,
    'left_ankle':15,
    'right_ankle':16,
} 

#Possible keypoints - blazeposed
KEYPOINT_DICT_BLAZEPOSE = {
    'nose': (0, mp_pose.PoseLandmark.NOSE),
    'left_eye_inner': (1, mp_pose.PoseLandmark.LEFT_EYE_INNER),
    'left_eye': (2, mp_pose.PoseLandmark.LEFT_EYE),
    'left_eye_outer': (3, mp_pose.PoseLandmark.LEFT_EYE_OUTER),
    'right_eye_inner': (4, mp_pose.PoseLandmark.RIGHT_EYE_INNER),
    'right_eye': (5, mp_pose.PoseLandmark.RIGHT_EYE),
    'right_eye_outer': (6, mp_pose.PoseLandmark.RIGHT_EYE_OUTER),
    'left_ear': (7, mp_pose.PoseLandmark.LEFT_EAR),
    'right_ear': (8, mp_pose.PoseLandmark.RIGHT_EAR),
    'mouth_left': (9, mp_pose.PoseLandmark.MOUTH_LEFT),
    'mouth_right': (10, mp_pose.PoseLandmark.MOUTH_RIGHT),
    'left_shoulder': (11, mp_pose.PoseLandmark.LEFT_SHOULDER),
    'right_shoulder': (12, mp_pose.PoseLandmark.RIGHT_SHOULDER),
    'left_elbow': (13, mp_pose.PoseLandmark.LEFT_ELBOW),
    'right_elbow': (14, mp_pose.PoseLandmark.RIGHT_ELBOW),
    'left_wrist': (15, mp_pose.PoseLandmark.LEFT_WRIST),
    'right_wrist': (16, mp_pose.PoseLandmark.RIGHT_WRIST),
    'left_pinky': (17, mp_pose.PoseLandmark.LEFT_PINKY),
    'right_pinky': (18, mp_pose.PoseLandmark.RIGHT_PINKY),
    'left_index': (19, mp_pose.PoseLandmark.LEFT_INDEX),
    'right_index': (20, mp_pose.PoseLandmark.RIGHT_INDEX),
    'left_thumb': (21, mp_pose.PoseLandmark.LEFT_THUMB),
    'right_thumb': (22, mp_pose.PoseLandmark.RIGHT_THUMB),
    'left_hip': (23, mp_pose.PoseLandmark.LEFT_HIP),
    'right_hip': (24, mp_pose.PoseLandmark.RIGHT_HIP),
    'left_knee': (25, mp_pose.PoseLandmark.LEFT_KNEE),
    'right_knee': (26, mp_pose.PoseLandmark.RIGHT_KNEE),
    'left_ankle': (27, mp_pose.PoseLandmark.LEFT_ANKLE),
    'right_ankle': (28, mp_pose.PoseLandmark.RIGHT_ANKLE),
    'left_heel': (29, mp_pose.PoseLandmark.LEFT_HEEL),
    'right_heel': (30, mp_pose.PoseLandmark.RIGHT_HEEL),
    'left_foot_index': (31, mp_pose.PoseLandmark.LEFT_FOOT_INDEX),
    'right_foot_index': (32, mp_pose.PoseLandmark.RIGHT_FOOT_INDEX),
}


# Joint parings - movenet
KEYPOINT_CONNECTIONS_MOVENET = {
    (0, 1): 'm',
    (0, 2): 'c',
    (1, 3): 'm',
    (2, 4): 'c',
    (0, 5): 'm',
    (0, 6): 'c',
    (5, 7): 'm',
    (7, 9): 'm',
    (6, 8): 'c',
    (8, 10): 'c',
    (5, 6): 'y',
    (5, 11): 'm',
    (6, 12): 'c',
    (11, 12): 'y',
    (11, 13): 'm',
    (13, 15): 'm',
    (12, 14): 'c',
    (14, 16): 'c',
}


# Different poses to be processed
JUMP_PROFILE_MOVENET = {
    "frontal" : ['right_hip', 
                 'left_hip', 
                 'right_knee', 
                 'left_knee',
                 'right_ankle', 
                 'left_ankle'],
    "right": ['right_hip', 
              'right_knee', 
              'right_ankle'],
    "left": ['left_hip', 
             'left_knee', 
             'left_ankle'],
}

JUMP_PROFILE_BLAZEPOSE = {
    "frontal" : ['right_hip', 
                 'left_hip', 
                 'right_knee', 
                 'left_knee',
                 'right_ankle', 
                 'left_ankle', 
                 'right_foot_index', 
                 'right_heel', 
                 'left_foot_index', 
                 'left_heel'],
    "right": ['right_hip', 
              'right_knee', 
              'right_ankle', 
              'right_foot_index', 
              'right_heel'],
    "left": ['left_hip', 
             'left_knee', 
             'left_ankle', 
             'left_foot_index', 
             'left_heel'],
}

ANGLES_MOVENET = {
    "right" : {
        "knee_angle": ['right_hip', 'right_knee', "right_ankle"],
    },
    "left": {
        "knee_angle": ['left_hip', 'left_knee', "left_ankle"]
    },
    "frontal": {}
}

ANGLES_BLAZEPOSE = {
        "right": {
            "knee_angle": ['right_hip', 'right_knee', "right_ankle"],
            "ankle_angle": ['right_knee', 'right_ankle', "right_foot_index"]
        },
        "left": {
            "knee_angle": ['left_hip', 'left_knee', "left_ankle"],
            "ankle_angle": ['left_knee', 'left_ankle', "left_foot_index"],
        },
        "frontal": {},
}



def select_connections(desired_keypoints, keypoints_dict, 
                      keypoints_connections, neural_network):
    """Select the connections for the desired joints
    
    Args:
        desired_keypoints: dictionaty with  pose desired keypoints
        keypoints_dict: dictionaty with all the possible keypoints for the
            selected neural network
        keypoints_connections: disctionary with the points connections
        neural_network: neural network that will be used to make the pose 
            prediction ('movenet' or 'blazepose')

    Return:
        new_keypoints_connections: dictionary with only de desired_keypoints 
            connections
    """
    new_keypoints_dict = {}
    new_keypoints_connections = {}


    for keypoint_name in desired_keypoints:
        if neural_network == "movenet":
            new_keypoints_dict[keypoint_name] = keypoints_dict[keypoint_name]
        elif neural_network == "blazepose":
            new_keypoints_dict[keypoint_name] = keypoints_dict[keypoint_name][0]

    if neural_network=="movenet":
        for pos, color in keypoints_connections.items():
            p1, p2 = pos
            if (p1 in list(new_keypoints_dict.values())
                and p2 in list(new_keypoints_dict.values())):
                p1_tf = list(new_keypoints_dict.values()).index(p1)
                p2_tf = list(new_keypoints_dict.values()).index(p2)
                new_keypoints_connections[(p1_tf, p2_tf)] = color
    if neural_network=="blazepose":
        for p1, p2 in keypoints_connections:
            if (p1 in list(new_keypoints_dict.values()) 
                and p2 in list(new_keypoints_dict.values())):
                p1_tf = list(new_keypoints_dict.values()).index(p1)
                p2_tf = list(new_keypoints_dict.values()).index(p2)
                new_keypoints_connections[(p1_tf, p2_tf)] = "c"

    return new_keypoints_connections

def select_keypoints(frame, keypoints, desired_keypoints,
                    keypoints_dict, neural_network):
    """Select only the desired joints
    
    Args:
        frame: frame of the video used in the predictions
        keypoints: disctionary with all the possible keypoints
        desired_keypoints: dictionaty with desired pose keypoints
        keypoints_dict: dictionaty with all the possible keypoints for the
            selected neural network
        neural_network: neural network that will be used to make the pose 
            prediction ('movenet' or 'blazepose')

    Return:
        selected_keypoints: vector with the (x, y) position of
            each desired keypoints
    """
    frame_height, frame_width, _ = frame.shape

    selected_keypoints = np.zeros([len(desired_keypoints), 2])
    selected_keypoints[:] = np.NaN

    for i in range(len(desired_keypoints)):
        keypoint = desired_keypoints[i]
        
        if neural_network == 'movenet':
            idx = list(keypoints_dict.keys()).index(keypoint)
            selected_keypoints[i, :] = keypoints[idx, :]
        elif neural_network == 'blazepose' and keypoints != None:
            keypoint_object = keypoints_dict[desired_keypoints[i]][1]
            selected_keypoints[i, :] = [
                    keypoints.landmark[keypoint_object].x*frame_width, 
                    keypoints.landmark[keypoint_object].y*frame_height,
            ]
    return selected_keypoints

def mark_keypoints_bellow_threshold(keypoints_with_scores, 
                                    confidence_threshold, 
                                    frame_width, 
                                    frame_height):
    """ Set np.nan for keypoints bellow threshold
    
    Args:
        keypoints_with_scores: array with pose keypoints and it's respectives 
        scores
        confidence_threshold: the threshold used to define np.nan to a keypoint
        frame_width: image width
        frame_height: image height

    Returns:
        marked_keypoints: numpy array with keypoints

    """
    marked_keypoints = np.zeros([len(list(KEYPOINT_DICT_MOVENET.values())), 2])
    
    y, x, c = frame_width, frame_height, 3
    shaped = np.squeeze(np.multiply(keypoints_with_scores, [y,x,1]))
    
    j = 0
    for i in range(len(shaped)):
        if i in list(KEYPOINT_DICT_MOVENET.values()):
            ky, kx, kp_conf = shaped[i]
            if kp_conf > confidence_threshold:
                marked_keypoints[j, 0] = kx
                marked_keypoints[j, 1] = ky
            else:
                marked_keypoints[j, 0] = np.nan
                marked_keypoints[j, 1] = np.nan
            j+=1
    return marked_keypoints