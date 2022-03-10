from audioop import getsample
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
import angles
import colors
from data_monitor import DataMonitor # https://github.com/bhartl/data-monitor


#-------------------------------------------------------------------------------------

# Threshold of a prediction confidence
THRESHOLD = 0.3

#-------------------------------------------------------------------------------------
def predictionToVideo(interpreter, video_name, video_path, video_out_path, file_out_path, profile):
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
    angle_data = [(0, 0)]
    # define meta-info for DataMonitor plotting (label of data-rows and coloring)
    channels = [
        {'label': 'Knee Angle', 'color': 'tab:pink'}
    ]
    # define plot format (dict of matplotlib.pyplot attributes and related (*args, **kwargs))
    plt_kwargs = dict(
        xlim=((0, file_metadata["n_frames"]), {}),
        ylim=((0, 200), {}),
        xlabel=(('Frame number', ), {}),
        ylabel=(('Angles in degrees',), {}),
    )

    with DataMonitor(channels=channels, ax_kwargs=plt_kwargs) as dm:
        while True:
            has_frame, frame = video_capture.read()
            if not has_frame:
                break
            
            # Reshape image
            reshaped_frame = frame.copy()
            reshaped_frame = tf.image.resize_with_pad(np.expand_dims(reshaped_frame, axis=0), 192,192)
            processed_frame = tf.cast(reshaped_frame, dtype=tf.float32)
            
            # Setup input and output 
            input_details = interpreter.get_input_details()
            output_details = interpreter.get_output_details()
            
            # Make predictions 
            interpreter.set_tensor(input_details[0]['index'], np.array(processed_frame))
            interpreter.invoke() 
            keypoints_with_scores = interpreter.get_tensor(output_details[0]['index'])
            
            # Key points
            frame_width = frame.shape[0]
            frame_height = frame.shape[1]
            keypoints = utils.transformDATA(keypoints_with_scores, THRESHOLD, frame_width, frame_height)

            # Select correct pose profile
            pose_selected = poses.JUMP_PROFILE_MOVENET[profile]
            
            keypoint_connections = poses.selectConnections(pose_selected, poses.KEYPOINT_DICT_MOVENET, poses.KEYPOINT_CONNECTIONS_MOVENET, "movenet")
            selected_keypoints = poses.selectKeypoints(frame, keypoints, pose_selected, poses.KEYPOINT_DICT_MOVENET, 'movenet')
            
            # Draw the keypoints and pairings
            drawing.drawConnections(frame, selected_keypoints, keypoint_connections)
            drawing.drawKeypoints(frame, selected_keypoints)

            # Get angles and draw it in the  screen
            _angles = angles.getAngles(selected_keypoints)
            cv2.putText(frame, str(round(_angles, 1)), (50,100), cv2.FONT_HERSHEY_PLAIN, 3, (128,0,255), 4)
            sample = (frame_iterator, _angles)
            angle_data.append(sample)
            dm.data = np.asarray(angle_data).T
            frame_iterator+=1 


            # Write video to file
            output_video.write(frame)

            # Save video to pickle
            pickle_output_list.append({'keypoints': selected_keypoints.tolist()})

            # Write data to file
            file_data = {'keypoints': selected_keypoints.tolist()}
            fileManagement.writeToJsonFile(file_out_path, file_data, write_mode='a')

            # Show video frame
            cv2.namedWindow('MoveNet Lightning', cv2.WINDOW_NORMAL)
            cv2.imshow('MoveNet Lightning', frame)

            # ESC to leave
            k = cv2.waitKey(25) & 0xFF
            if k == 27:
                break
    
    # Create pickle output data
    pickle_output_data = {"header": file_metadata, "data": pickle_output_list}
    fileManagement.writePickleFile(file_out_path, pickle_output_data)

    # Finish exhibition
    video_capture.release()
    cv2.destroyAllWindows()
    output_video.release()

#-------------------------------------------------------------------------------------

if __name__ == "__main__":
    # Start tensor flow
    interpreter = tf.lite.Interpreter(model_path='lite-model_movenet_singlepose_lightning_3.tflite')
    interpreter.allocate_tensors()


    # Select video
    video_name, video_path, video_out_path, file_out_path, profile = userInterface.initialMenu("movenet")

    # Make predictions
    predictionToVideo(interpreter, video_name, video_path, video_out_path, file_out_path, profile)

#-------------------------------------------------------------------------------------