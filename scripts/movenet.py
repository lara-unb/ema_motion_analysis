"""Pose detection using Movenet.

"""

# General imports
import tensorflow as tf
import numpy as np
import cv2
import sys

# Ema motion analysis imports
sys.path.append("../utils/")
import file_management
import drawing
import utils
import poses
import user_interface
import angles
import colors
from data_monitor import DataMonitor
import time


# Threshold of a prediction confidence
THRESHOLD = 0.3


def predictionToVideo(interpreter, video_name, video_path,
                      video_out_path, file_out_path, profile):
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
         'y_label': 'Angle(deg)', 'x_label': "Time(s)", "width": 2}
    ]

    # Pass by each frame of the video and draw points and connections
    with DataMonitor(channels=channels) as dm:
        startTime = time.time()

        while True:
            has_frame, frame = video_capture.read()
            if not has_frame:
                break
            
            # Reshape image
            reshaped_frame = frame.copy()
            reshaped_frame = tf.image.resize_with_pad(np.expand_dims(reshaped_frame, axis=0),
                                                      192,192)
            processed_frame = tf.cast(reshaped_frame, dtype=tf.float32)
            
            # Setup input and output 
            input_details = interpreter.get_input_details()
            output_details = interpreter.get_output_details()
            
            # Make predictions 
            interpreter.set_tensor(input_details[0]['index'], 
                                   np.array(processed_frame))
            interpreter.invoke() 
            keypoints_with_scores = interpreter.get_tensor(output_details[0]['index'])
            
            # Key points
            frame_width = frame.shape[0]
            frame_height = frame.shape[1]
            keypoints = utils.transformDATA(keypoints_with_scores, 
                                            THRESHOLD, 
                                            frame_width, 
                                            frame_height)

            # Select correct pose profile
            pose_selected = poses.JUMP_PROFILE_MOVENET[profile]
            
            keypoint_connections = poses.selectConnections(pose_selected, 
                                                           poses.KEYPOINT_DICT_MOVENET, 
                                                           poses.KEYPOINT_CONNECTIONS_MOVENET, 
                                                           "movenet")
            selected_keypoints = poses.selectKeypoints(frame, 
                                                       keypoints, 
                                                       pose_selected, 
                                                       poses.KEYPOINT_DICT_MOVENET, 
                                                       'movenet')
            
            # Draw the keypoints and pairings
            drawing.drawConnections(frame, 
                                    selected_keypoints, 
                                    keypoint_connections)
            drawing.drawKeypoints(frame, 
                                  selected_keypoints)

            # Get angles and draw it in the  screen
            poses_angles = angles.getAngles(selected_keypoints, 
                                            poses.ANGLES_MOVENET, 
                                            profile, 
                                            pose_selected)

            # Draw angle to the screen
            drawing.writeAnglesLegends(frame, 
                                       poses_angles, 
                                       poses.ANGLES_MOVENET[profile])

            # Update real time graphics
            dm.data = {
                "data": poses_angles,
                "time": time.time() - startTime,
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

            # Show video frame
            cv2.namedWindow('MoveNet Lightning', cv2.WINDOW_NORMAL)
            cv2.imshow('MoveNet Lightning', frame)

            # ESC to leave
            k = cv2.waitKey(25) & 0xFF
            if k == 27:
                break
    
    # Create pickle output data
    pickle_output_data = {"header": file_metadata, "data": pickle_output_list}
    file_management.writePickleFile(file_out_path, pickle_output_data)

    # Finish exhibition
    video_capture.release()
    cv2.destroyAllWindows()
    output_video.release()



if __name__ == "__main__":
    # Start tensor flow
    interpreter = tf.lite.Interpreter(model_path='lite-model_movenet_singlepose_lightning_3.tflite')
    interpreter.allocate_tensors()

    # Select video
    video_name, video_path, video_out_path, file_out_path, profile = user_interface.initialMenu("movenet")

    # Make predictions
    predictionToVideo(interpreter, 
                      video_name, 
                      video_path, 
                      video_out_path, 
                      file_out_path, 
                      profile)

