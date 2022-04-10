"""Pose detection using BlazePose.
This code is inspired in the demo available in:
https://google.github.io/mediapipe/solutions/pose.html#python-solution-api

"""

# General imports
import sys
import cv2
import mediapipe as mp
import numpy as np
import matplotlib.pyplot as plt
import time

# Ema motion analysis imports
sys.path.append("../utils/")
import colors
import file_management
import drawing
import poses
import user_interface
import angles
from data_monitor import DataMonitor

# Simplify mediapipe variables
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose

# Set confidence predictions and tracking threshold
THRESHOLD = 0.3

def prediction_to_video(video_name, video_path, 
                      video_out_path, file_out_path,  profile):
    """Predicts a pose for the person in the video

    Predicts a pose for the person in the video (according to the selected
    profile)
    Displays in the screen the output video showing the selected joints and
    their connections and angles
    Displays a real time plot for the joint angles

    Args:
        video_name: a string with the name of the video to be used in the predicton
        video_path: a string with the path to the video to be used in the prediction
        video_out_path: a string with the path to the output prediction video
        file_out_path: a string with the path to the output prediction file
        profile: a string informing the profile os the person in the video
            ('frontal', 'right', 'left')

    Saves the output video (.avi) and two output files (.data and .pickle) with
    a header and the selected keypoint locations for each frame
    """

    # Get video
    video_capture = cv2.VideoCapture(video_path)
    if not file_management.videoCheck(video_capture):
        return

    # Create output video file
    output_video = file_management.createOutputVideoFile(video_out_path,
                                                        video_capture)
    video_capture.release()

    # Create output file data
    file_metadata = file_management.setMetadata(video_name, 
                                               poses.KEYPOINT_DICT_MOVENET, 
                                               poses.JUMP_PROFILE_MOVENET[profile], 
                                               video_path)
                                               
    file_management.writeToJsonFile(file_out_path, 
                                   file_metadata, 
                                   write_mode='w+')

    # Initialize pickle output list
    pickle_output_list = []

    # Create video file to process
    video_capture = cv2.VideoCapture(video_path)
    if not file_management.videoCheck(video_capture):
        return

    # define info for DataMonitor plotting
    channels = [
        {'title': "Knee Angle", 'color': 'pink', 
         'y_label': 'Angle(deg)', 'x_label': "Time(s)", "width": 2},
        {'title': "Feet Angle", 'color': 'cyan', 
         'y_label': 'Angle(deg)', 'x_label': "Time(s)", "width": 2}
    ]


    # Apply blazepose network
    with mp_pose.Pose(min_detection_confidence=THRESHOLD, 
                      min_tracking_confidence=THRESHOLD) as pose: 
        # Pass by each frame of the video and draw points and connections
        with DataMonitor(channels=channels) as dm:
            startTime = time.time()
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
                keypoint_connections = poses.selectConnections(pose_selected, 
                                                               poses.KEYPOINT_DICT_BLAZEPOSE, 
                                                               mp_pose.POSE_CONNECTIONS, 
                                                               neural_network="blazepose")

                selected_keypoints = poses.selectKeypoints(frame, 
                                                           mp_results_object.pose_landmarks, 
                                                           pose_selected, 
                                                           poses.KEYPOINT_DICT_BLAZEPOSE, 
                                                           'blazepose')

                # Draw joints and pairings
                drawing.drawConnections(frame, 
                                        selected_keypoints, 
                                        keypoint_connections)
                drawing.drawKeypoints(frame,
                                      selected_keypoints)

                # Get angles and draw it in the  screen
                poses_angles = angles.get_angles(selected_keypoints, 
                                                poses.ANGLES_BLAZEPOSE[profile], 
                                                pose_selected)

                # Write angles data in the screen
                drawing.writeAnglesLegends(frame, 
                                           poses_angles, 
                                           poses.ANGLES_BLAZEPOSE[profile])

                # Update realtime angle graphics
                dm.data = {
                    "data": poses_angles,
                    "time": time.time() - startTime
                }

                # Write video to file
                output_video.write(frame)

                # Save video to pickle
                pickle_output_list.append({'keypoints': selected_keypoints.tolist()})

                # Write data to file
                file_data = {'keypoints': selected_keypoints.tolist()}
                file_management.writeToJsonFile(file_out_path, 
                                               file_data, 
                                               write_mode='a')
                
                # Show image
                cv2.namedWindow('Blazepose Lite', cv2.WINDOW_NORMAL)
                cv2.imshow('Blazepose Lite', frame) 
                if cv2.waitKey(5) & 0xFF == 27:
                    break
    
    # Create pickle output data
    pickle_output_data = {"header": file_metadata, "data": pickle_output_list}
    file_management.writePickleFile(file_out_path, pickle_output_data)

    # Finish exhibition
    video_capture.release()
    cv2.destroyAllWindows()
    output_video.release()


# Main functions, select video and apply blazepose algorithm
if __name__ == "__main__":
    # Select video
    video_name, video_path, video_out_path, file_out_path, profile = user_interface.initialMenu("blazepose")

    # Make predictions
    prediction_to_video(video_name, 
                      video_path, 
                      video_out_path, 
                      file_out_path, 
                      profile)