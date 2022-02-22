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

# Simplify mediapipe variables
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose

# Set confidence predictions and tracking threshold
THRESHOLD = 0.3

def predictionToVideo(video_path, video_out_path, profile):
    # Get video
    video_capture = cv2.VideoCapture(video_path)
    if(not fileManagement.videoCheck(video_capture)):
        return

    # Create output video file
    output_video = fileManagement.createOutputVideoFile(video_out_path, video_capture)
    video_capture.release()

    # Create video file to process
    video_capture = cv2.VideoCapture(video_path)
    if(not fileManagement.videoCheck(video_capture)):
        return

    # Apply blazepose network
    with mp_pose.Pose(min_detection_confidence=THRESHOLD, min_tracking_confidence=THRESHOLD) as pose: 
        # Pass by each frame of the video and draw points and connections
        while video_capture.isOpened():
            has_frame, frame = video_capture.read()
            if not has_frame:
                break

            # To improve performance
            frame.flags.writeable = False
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Process frame
            mp_results_object = pose.process(frame)

            # Draw the pose annotation on the frame.
            frame.flags.writeable = True
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

            # Select correct pose profile
            pose_selected = poses.JUMP_PROFILE_BLAZEPOSE[profile]

            # Get pairings of interest
            keypoint_connections = poses.selectConnections(pose_selected, poses.KEYPOINT_DICT_BLAZEPOSE, mp_pose.POSE_CONNECTIONS, neural_network="blazepose")
            selected_keypoints = poses.selectKeypoints(frame, mp_results_object.pose_landmarks, pose_selected, poses.KEYPOINT_DICT_BLAZEPOSE, 'blazepose')

            # Draw joints and pairings
            drawing.drawConnections(frame, selected_keypoints, keypoint_connections)
            drawing.drawKeypoints(frame,selected_keypoints)

            # Write video to file
            output_video.write(frame)
            
            # Show image
            cv2.imshow('MediaPipe Pose', frame) 
            if cv2.waitKey(5) & 0xFF == 27:
                break
    
    # Finish exhibition
    video_capture.release()
    cv2.destroyAllWindows()
    output_video.release()


# Main functions, select video and apply blazepose algorithm
if __name__ == "__main__":
    # Select video
    video_path, video_out_path, profile = userInterface.initialMenu()

    # Make predictions
    predictionToVideo(video_path, video_out_path, profile)