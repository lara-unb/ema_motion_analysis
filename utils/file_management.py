from PyQt5 import QtGui
from PyQt5.QtWidgets import QWidget, QFileDialog
from PyQt5.QtWidgets import QApplication
import pickle
import cv2
import json
import pickle



import sys

from numpy import absolute
import colors

import os

#-------------------------------------------------------------------------------------
# Get absolute path to root project
def getAbsolutePath():
    absolute_main_path = os.path.dirname(os.path.abspath(__file__))
    return absolute_main_path

def getOutputsPaths(video_name, video_input_format, neural_network_name):
    absolute_path = getAbsolutePath()
    outputs_folder = absolute_path + "/../outputs/"
    examples_folder = absolute_path + "/../examples/"
    video_path = examples_folder + video_name + video_input_format
    video_out_path = outputs_folder + video_name + "-" +  neural_network_name + "-"+ "mnl.avi"
    file_out_path = outputs_folder + video_name + "-" +  neural_network_name
    return video_path, video_out_path, file_out_path
#-------------------------------------------------------------------------------------
# Function to open file dialog to choose video
def readFileDialog(neural_network, title="Open File", file_type="All Files"):
    app = QApplication(sys.argv)
    qfd = QFileDialog()
    if file_type == "All Files":
        type_filter = "All Files (*)"
    else:
        type_filter = file_type + " (*." + file_type + ")"
    video_path, _ = QFileDialog.getOpenFileName(qfd, title, "", type_filter)
    video_name = video_path.split("/")[-1].split(".")[0]
    video_format = video_path.split("/")[-1].split(".")[1]
    _, video_out_path, file_out_path = getOutputsPaths(video_name , video_format, neural_network)
    return video_name, video_path, video_out_path, file_out_path

#-------------------------------------------------------------------------------------
# Function to check if the video was opend 
def videoCheck(video):
    if(not video.isOpened()):
        print(colors.RED, "Couldn't open video!", colors.RESET)
        return False
    return True

def createOutputVideoFile(video_out_path, video_capture):
    has_frame, image = video_capture.read()
    fps = int(video_capture.get(cv2.CAP_PROP_FPS))
    n_frames = int(video_capture.get(cv2.CAP_PROP_FRAME_COUNT))
    frame_width = image.shape[0]
    frame_height = image.shape[1]

    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    fourcc = cv2.VideoWriter_fourcc('M','J','P','G')

    return cv2.VideoWriter(video_out_path, fourcc, fps, (frame_width,frame_height))
#-------------------------------------------------------------------------------------
# Generate output file - ISSO AQUI NÃO ESTÁ SENDO USADO - APAGA ? 
def save_to_file(data_dic, file_path):
    with open(file_path, 'wb') as f:
        for key in data_dic.keys():
            pickle.dump(key, f)
            pickle.dump(data_dic[key], f)

#-------------------------------------------------------------------------------------
# Set video metadata object
def setMetadata(video_name, mapping, pairs, video_path, summary="None"):
    # Open video
    video_capture = cv2.VideoCapture(video_path)
    videoCheck(video_capture)

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
    
def writeToJsonFile(file_out_path, data, write_mode='w'):
    with open(file_out_path+".data", write_mode) as f:
        f.write(json.dumps(data))
        f.write('\n')

#-------------------------------------------------------------------------------------

def writePickleFile(file_out_path, file_dictionary):
    with open(file_out_path+".pickle", 'wb') as f:
        pickle.dump(file_dictionary, f)

#------------------------------------------------------------------------------------

def readPickleFile(file_out_path):
    with open(file_out_path, "rb") as f:
        loaded_obj = pickle.load(f)
    return loaded_obj

