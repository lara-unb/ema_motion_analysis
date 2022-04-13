import numpy as np
import poses

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
    marked_keypoints = np.zeros([len(list(poses.KEYPOINT_DICT_MOVENET.values())), 2])
    
    y, x, c = frame_width, frame_height, 3
    shaped = np.squeeze(np.multiply(keypoints_with_scores, [y,x,1]))
    
    j = 0
    for i in range(len(shaped)):
        if i in list(poses.KEYPOINT_DICT_MOVENET.values()):
            ky, kx, kp_conf = shaped[i]
            if kp_conf > confidence_threshold:
                marked_keypoints[j, 0] = kx
                marked_keypoints[j, 1] = ky
            else:
                marked_keypoints[j, 0] = np.nan
                marked_keypoints[j, 1] = np.nan
            j+=1
    return marked_keypoints