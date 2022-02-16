
import numpy as np
import json
import poses

#-------------------------------------------------------------------------------------
# get the keypoints above the trashhold and change vector to numpy array
def transformDATA(kp_w_scores_vec, confidence_threshold, frame_width, frame_height):
    keypoints_vec = np.zeros([len(list(poses.KEYPOINT_DICT.values())), 2])
    
    y, x, c = frame_width, frame_height, 3
    shaped = np.squeeze(np.multiply(kp_w_scores_vec, [y,x,1]))
    
    j = 0
    for i in range(len(shaped)):
        if i in list(poses.KEYPOINT_DICT.values()):
            ky, kx, kp_conf = shaped[i]
            if kp_conf > confidence_threshold:
                keypoints_vec[j, 0] = kx
                keypoints_vec[j, 1] = ky
            else:
                keypoints_vec[j, 0] = np.nan
                keypoints_vec[j, 1] = np.nan
            j+=1
    return keypoints_vec


#-------------------------------------------------------------------------------------
# A GENTE TMB N TA USANDO ESSA

# def writeToDATA(file_path, data, write_mode='w'):
#     with open(file_path, write_mode) as f:
#         json.dump(data, f)