# Cabeçalho ? 
# Esse código é uma modificação da solução demonstração disponível em:
# https://google.github.io/mediapipe/solutions/pose.html#python-solution-api

# General imports
import sys
from turtle import color
import cv2
import mediapipe as mp
import numpy as np
import matplotlib.pyplot as plt

# Ema motion analysis imports
sys.path.append("../utils/")
import colors
import fileManagement
import drawing
import poses
import userInterface

# Simplify variables
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose

# Set confidence predictions threshold
THRESHOLD = 0.3

def predictionToVideo(video_path, video_out_path, profile):
    # Get video object
    video = cv2.VideoCapture(video_path)

    # Check if it's possible to open the video
    if(not fileManagement.videoCheck(video)):
        return

    # Apply blazepose network - PERGUNTAR VICTOR: min_detection_confidence, min_tracking_confidence
    with mp_pose.Pose(
      min_detection_confidence=THRESHOLD,
      min_tracking_confidence=THRESHOLD) as pose: 

        # get video
        cap = cv2.VideoCapture(video_path)
        if(not fileManagement.videoCheck(cap)):
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

        # Create output video file
        print(colors.RED, video_out_path, colors.RESET)
        out = fileManagement.createOutputVideoFile(video_out_path, cap)

        # Pass by each frame of the video and draw points and connections
        while video.isOpened():
            ret, frame = video.read()
            if not ret:
                break

            # To improve performance, optionally mark the image as not writeable to
            # pass by reference.
            frame.flags.writeable = False
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Process image
            mp_results_object = pose.process(frame)

            # Draw the pose annotation on the image.
            frame.flags.writeable = True
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

            # Select correct pose
            pose_selected = poses.JUMP_FRONTAL
            if(profile == "left"):
                pose_selected = poses.JUMP_SAGITTAL_LEFT_FULL
            elif(profile == "right"):
                pose_selected = poses.JUMP_SAGITTAL_RIGHT_FULL

            # Get pairings of interest
            keypoint_pairings = poses.getPairings(pose_selected, poses.KEYPOINT_DICT_BLAZEPOSE, mp_pose.POSE_CONNECTIONS, neural_network="blazepose")
            selected_joints = poses.selectJoints(frame, mp_results_object.pose_landmarks, pose_selected, poses.KEYPOINT_DICT_BLAZEPOSE, 'blazepose')

            # Draw joints and pairings
            drawing.draw_connections(frame, selected_joints, keypoint_pairings)
            drawing.draw_keypoints(frame,selected_joints)

            out.write(frame)
            
            # Show image
            cv2.imshow('MediaPipe Pose', frame) 
            if cv2.waitKey(5) & 0xFF == 27:
                break
    
    # Close video
    video.release()


# Main functions, select video and apply blazepose algorithm
if __name__ == "__main__":
    video_path, video_out_path, profile = userInterface.initialMenu()
    predictionToVideo(video_path, video_out_path, profile)