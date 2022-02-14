from ctypes import util
import tensorflow as tf
import numpy as np
from matplotlib import pyplot as plt
import cv2

import sys

sys.path.append("../utils/")
import fileManagement
import drawing
import colors
import utils
import poses









def predictionToVideo(interpreter, video_path, video_out_path):
    cap = cv2.VideoCapture(video_path)
    if(not cap.isOpened()):
        print(colors.RED, "Couldn't open video!", colors.RESET)
        return

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
        
        # Key points - Mudar nome de utils - Colocar Threshold em uma variável!
        key_points = utils.transformDATA(keypoints_with_scores, 0.3, frame_width, frame_height)

        # Rendering 
        jump_sagittal_left = ['left_hip', 'left_knee', 'left_ankle']
        jump_sagittal_right = ['right_hip', 'right_knee', 'right_ankle']
        key_point_pairings = poses.get_kp_pairings(jump_sagittal_right, poses.KEYPOINT_DICT, poses.EDGES)
        
        selected_joints = poses.select_joints(key_points, jump_sagittal_right, poses.KEYPOINT_DICT)
        print(colors.BLUE, key_point_pairings, colors.RESET)
        drawing.draw_connections(frame, selected_joints, key_point_pairings)
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


if __name__ == "__main__":
    interpreter = tf.lite.Interpreter(model_path='lite-model_movenet_singlepose_lightning_3.tflite')
    interpreter.allocate_tensors()
    video_path = fileManagement.readFileDialog("Open video file")
    video_out_path = video_path.split(".")[0] + "_mnl.avi"
    predictionToVideo(interpreter, video_path, video_out_path)