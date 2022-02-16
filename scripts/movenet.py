from ctypes import util
import tensorflow as tf
import numpy as np
from matplotlib import pyplot as plt
import cv2

import sys

sys.path.append("../utils/")
import fileManagement
import drawing
import utils
import poses
import userInterface


#-------------------------------------------------------------------------------------

# Trashhold que vai ser utilizado para as predições
TRASHHOLD = 0.3

#-------------------------------------------------------------------------------------
# ACHO Q A GNT PODE QUEBRAR MAIS ESSA FUNÇÃOZONA
def predictionToVideo(interpreter, video_path, video_out_path, profile):
    # get video
    cap = cv2.VideoCapture(video_path)
    fileManagement.videoCheck(cap)

    has_frame, image = cap.read()
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    n_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    frame_width = image.shape[0]
    frame_height = image.shape[1]
    cap.release() 

    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    fourcc = cv2.VideoWriter_fourcc('M','J','P','G')

    cap = cv2.VideoCapture(video_path)

    out = cv2.VideoWriter(video_out_path, fourcc, fps, (frame_width,frame_height))
    while True:
        ret, frame = cap.read()
        # frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
        if not ret:
            break
        
        # Reshape image
        img = frame.copy()
        img = tf.image.resize_with_pad(np.expand_dims(img, axis=0), 192,192)
        input_image = tf.cast(img, dtype=tf.float32)
        
        # Setup input and output 
        input_details = interpreter.get_input_details()
        output_details = interpreter.get_output_details()
        
        # Make predictions 
        interpreter.set_tensor(input_details[0]['index'], np.array(input_image))
        interpreter.invoke() 
        keypoints_with_scores = interpreter.get_tensor(output_details[0]['index'])
        
        # Key points
        keypoints = utils.transformDATA(keypoints_with_scores, TRASHHOLD, frame_width, frame_height)

        # Select correct pose 
        pose_selected = poses.JUMP_FRONTAL
        if(profile == "left"):
            pose_selected = poses.JUMP_SAGITTAL_LEFT
        elif(profile == "right"):
            pose_selected = poses.JUMP_SAGITTAL_RIGHT
        
        keypoint_pairings = poses.getPairings(pose_selected, poses.KEYPOINT_DICT, poses.EDGES)
        selected_joints = poses.selectJoints(keypoints, pose_selected, poses.KEYPOINT_DICT)

        # Draw the joints and pairings
        drawing.draw_connections(frame, selected_joints, keypoint_pairings)
        drawing.draw_keypoints(frame, selected_joints)
        
        out.write(frame)

        cv2.imshow('MoveNet Lightning', frame)

        # ESC para sair
        k = cv2.waitKey(25) & 0xFF
        if k == 27:
            break
            
    cap.release()
    cv2.destroyAllWindows()
    out.release()

#-------------------------------------------------------------------------------------

if __name__ == "__main__":
    interpreter = tf.lite.Interpreter(model_path='lite-model_movenet_singlepose_lightning_3.tflite')
    interpreter.allocate_tensors()
    video_path, video_out_path, profile = userInterface.initialMenu()
    print(video_path)
    predictionToVideo(interpreter, video_path, video_out_path, profile)


#-------------------------------------------------------------------------------------
