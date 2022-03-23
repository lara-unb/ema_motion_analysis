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
import angles
from RealTimeDataMonitor import DataMonitor

# Simplify mediapipe variables
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose

# Set confidence predictions and tracking threshold
THRESHOLD = 0.3

def predictionToVideo(video_name, video_path, video_out_path, file_out_path,  profile):
    # Get video
    video_capture = cv2.VideoCapture(video_path)
    if(not fileManagement.videoCheck(video_capture)):
        return

    # Create output video file
    output_video = fileManagement.createOutputVideoFile(video_out_path, video_capture)
    video_capture.release()

    # Create output file data
    file_metadata = fileManagement.setMetadata(video_name, poses.KEYPOINT_DICT_MOVENET, poses.JUMP_PROFILE_MOVENET[profile], video_path)
    fileManagement.writeToJsonFile(file_out_path, file_metadata, write_mode='w+')

    # Initialize pickle output list
    pickle_output_list = []

    # Create video file to process
    video_capture = cv2.VideoCapture(video_path)
    if(not fileManagement.videoCheck(video_capture)):
        return

    # Angles plotting Configuration
    frame_iterator = 0
    angle_data = [(0, 0, 0)]

    # define info for DataMonitor plotting
    channels = [
        {'title': "Knee Angle", 'color': 'pink', 'y_label': 'Angle(deg)', 'x_label': "Time(s)", "width": 2},
        {'title': "Feet Angle", 'color': 'cyan', 'y_label': 'Angle(deg)', 'x_label': "Time(s)", "width": 2}
    ]


    # Apply blazepose network
    with mp_pose.Pose(min_detection_confidence=THRESHOLD, min_tracking_confidence=THRESHOLD) as pose: 
        # Pass by each frame of the video and draw points and connections
        with DataMonitor(channels=channels) as dm:
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

                # Get angles and draw it in the  screen
                poses_angles = angles.getAngles(selected_keypoints, poses.ANGLES_BLAZEPOSE, profile, pose_selected)

                # Write angles data in the screen
                drawing.writeAnglesLegends(frame, poses_angles, poses.ANGLES_BLAZEPOSE[profile])

                # Update realtime angle graphics
                dm.data = poses_angles

                # Write video to file
                output_video.write(frame)

                # Save video to pickle
                pickle_output_list.append({'keypoints': selected_keypoints.tolist()})

                # Write data to file
                file_data = {'keypoints': selected_keypoints.tolist()}
                fileManagement.writeToJsonFile(file_out_path, file_data, write_mode='a')
                
                # Show image
                cv2.namedWindow('Blazepose Lite', cv2.WINDOW_NORMAL)
                cv2.imshow('Blazepose Lite', frame) 
                if cv2.waitKey(5) & 0xFF == 27:
                    break
    
    # Create pickle output data
    pickle_output_data = {"header": file_metadata, "data": pickle_output_list}
    fileManagement.writePickleFile(file_out_path, pickle_output_data)

    # Finish exhibition
    video_capture.release()
    cv2.destroyAllWindows()
    output_video.release()


# Main functions, select video and apply blazepose algorithm
if __name__ == "__main__":
    # Select video
    video_name, video_path, video_out_path, file_out_path, profile = userInterface.initialMenu("blazepose")

    # Make predictions
    predictionToVideo(video_name, video_path, video_out_path, file_out_path, profile)