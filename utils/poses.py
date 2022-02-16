import numpy as np

#-------------------------------------------------------------------------------------
# Dictionary to map joints of body part
KEYPOINT_DICT = {
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
    'right_ankle':16
} 

#-------------------------------------------------------------------------------------
# Joint parings 
EDGES = {
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
    (14, 16): 'c'
}

#-------------------------------------------------------------------------------------
# Different poses to be processed

JUMP_SAGITTAL_LEFT = ['left_hip', 'left_knee', 'left_ankle']
JUMP_SAGITTAL_RIGHT = ['right_hip', 'right_knee', 'right_ankle']
JUMP_FRONTAL = ['right_hip', 'left_hip', 'right_knee', 'left_knee','right_ankle', 'left_ankle']


#-------------------------------------------------------------------------------------
# Function to get the parings of the desired joints
def getPairings(desired_kp, kp_dict, kp_pairings):
    new_kp_dict = {}
    new_kp_pairings = {}
    for kp_name in desired_kp:
        new_kp_dict[kp_name] = kp_dict[kp_name]
    for pos, color in kp_pairings.items():
        p1, p2 = pos
        if (p1 in list(new_kp_dict.values())) and (p2 in list(new_kp_dict.values())):
            p1_tf = list(new_kp_dict.values()).index(p1)
            p2_tf = list(new_kp_dict.values()).index(p2)
            new_kp_pairings[(p1_tf, p2_tf)] = color
   
    return new_kp_pairings

#-------------------------------------------------------------------------------------
# Function to select only the desired joints
def selectJoints(keypoints, desired_keypoints, kp_dict):
    selected_joints = np.zeros([len(desired_keypoints), 2])

    for i in range(len(desired_keypoints)):
        joint = desired_keypoints[i]
        idx = list(kp_dict.keys()).index(joint)
        selected_joints[i, :] = keypoints[idx, :]


    return selected_joints

#-------------------------------------------------------------------------------------



