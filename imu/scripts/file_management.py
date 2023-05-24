""" Defines file managements functions

"""
from PyQt5.QtWidgets import QFileDialog
import pickle
import cv2
import json
import pickle
import sys

sys.path.append("../../data_visualization")
import colors as colors
import os

def get_current_module_path():
    """ Get absolute path to the current module
    
    Returns:
        absolute_main_path: returns a string to this module path 
    """
    absolute_main_path = os.path.dirname(os.path.abspath(__file__))

    return absolute_main_path

def get_outputs_paths(video_name, video_input_format, neural_network_name):
    """ Get a tuple of paths for video file

    Args:
        video_name: string with video name
        video_input_format: string with video input format. Ex: ".mp4"
        neural_network_name: string with neural network name
    Returns:
        video_path: complete path of processed video
        video_out_path: complete path of output video
        file_out_path: complete path of text output file

    """
    absolute_path = get_current_module_path()
    outputs_folder = absolute_path + "/../outputs/"
    examples_folder = absolute_path + "/../examples/"
    video_path = examples_folder + video_name + video_input_format
    video_out_path = outputs_folder + video_name + "-" + neural_network_name + "-" + "mnl.avi" 
    file_out_path = outputs_folder + video_name + "-" +  neural_network_name
    return video_path, video_out_path, file_out_path

def read_file_dialog(neural_network, title="Open File", file_type="All Files"):
    """ Creates a visual interface that user can select a vide path

    Args:
        neural_network_name: string with neural network name
        title: string with the name of the file dialog box
        file_type: string kind of files that should be visible to user 
    Returns:
        video_name: string with video name
        video_path: complete path of processed video
        video_out_path: complete path of output video
        file_out_path: complete path of text output file
    """
    qfd = QFileDialog()
    if file_type == "All Files":
        type_filter = "All Files (*)"
    else:
        type_filter = file_type + " (*." + file_type + ")"
    video_path, _ = QFileDialog.getOpenFileName(qfd, title, "", type_filter)
    video_name = video_path.split("/")[-1].split(".")[0]
    video_format = video_path.split("/")[-1].split(".")[1]
    _, video_out_path, file_out_path = get_outputs_paths(video_name, 
                                                        video_format, 
                                                        neural_network)
    return video_name, video_path, video_out_path, file_out_path


def video_check(video):
    """ Check if video is opened

    Args: 
        video: opencv video object
    
    Returns:
        Boolean that indicates video was opened
    """
    if not video.isOpened():
        print(colors.RED, "Couldn't open video!", colors.RESET)
        return False
    return True

def create_output_video_file(video_out_path, video_capture):
    """ Creates an output video file

    Args: 
        video_out_path: absolute path that the video should be writen
        video_capture: opencv video object instance
    
    Returns:
        Opencv video writer object
    """
    has_frame, image = video_capture.read()
    fps = int(video_capture.get(cv2.CAP_PROP_FPS))
    frame_width = image.shape[0]
    frame_height = image.shape[1]

    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    fourcc = cv2.VideoWriter_fourcc('M','J','P','G')

    return cv2.VideoWriter(video_out_path, 
                          fourcc, 
                          fps, 
                          (frame_width,frame_height))

def set_video_metadata(video_name, mapping, pairs, video_path, summary="None"):
    """ Set video metadata object
    Args:
        video_name: string of video name
        mapping: keypoints names
        pairs: list of points of a correspondent profile
        video_path: a string with the path to the video to be used in the 
        prediction
        summary: string with short summary of the video
    Returns:
        file_metadata: dictionary containing meta informatio about the video
    """

    video_capture = cv2.VideoCapture(video_path)
    video_check(video_capture)

    length = int(video_capture.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = int(video_capture.get(cv2.CAP_PROP_FPS))

    has_frame, frame = video_capture.read()
    
    frame_width = frame.shape[0]
    frame_height = frame.shape[1]
    
    video_capture.set(2, 0.0)

    video_capture.release()

    file_metadata = {
        'video_name': video_name,
        'n_frames': length,
        'n_points': len(mapping),
        'frame_width': frame_width,
        'frame_height': frame_height,
        'fps': fps,
        'keypoints_names': mapping,
        'keypoints_pairs': pairs,
        'summary': summary
    }
    
    return file_metadata
    
def write_to_json_file(file_out_path, data, write_mode='w'):
    """ Write video information to a json file

    Args:
        file_out_path: string with path of the text file
        data: dictionary with the data that should be writen
        write_mode: a string that defines write mode
    """

    # Create outputs directory if needed
    if not os.path.isdir("../outputs"):  os.makedirs("../outputs")

    with open(file_out_path, write_mode) as f:
        f.write(json.dumps(data))
        f.write('\n')

def write_pickle_file(file_out_path, data):
    """ Write video information to a pickle file

    Args:
        file_out_path: string with path of the text file
        data: dictionary with the data that should be writen
    """
    with open(file_out_path+".pickle", 'wb') as f:
        pickle.dump(data, f)

def read_pickle_file(file_out_path):
    """ Read video information of pickle files

    Args:
        file_out_path: string with path of the text file
    Returns:
        Loaded pickle file
    """
    with open(file_out_path, "rb") as f:
        loaded_obj = pickle.load(f)
    return loaded_obj

