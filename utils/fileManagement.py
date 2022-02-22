from PyQt5 import QtGui
from PyQt5.QtWidgets import QWidget, QFileDialog
from PyQt5.QtWidgets import QApplication
import pickle
import cv2

import sys
import colors

import os

#-------------------------------------------------------------------------------------
# Get absolute path to root project
def getAbsolutePath():
    absolute_main_path = os.path.dirname(os.path.abspath(__file__))
    return absolute_main_path

#-------------------------------------------------------------------------------------
# Function to open file dialog to choose video
def readFileDialog(title="Open File", file_type="All Files"):
    app = QApplication(sys.argv)
    qfd = QFileDialog()
    if file_type == "All Files":
        type_filter = "All Files (*)"
    else:
        type_filter = file_type + " (*." + file_type + ")"
    file_path, _ = QFileDialog.getOpenFileName(qfd, title, "", type_filter)
    return file_path, file_path.split(".")[0] + "_mnl.avi"

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
    video_capture.release() 

    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    fourcc = cv2.VideoWriter_fourcc('M','J','P','G')

    return cv2.VideoWriter(video_out_path, fourcc, fps, (frame_width,frame_height))
#-------------------------------------------------------------------------------------
# Generate output file
def save_to_file(data_dic, file_path):
    with open(file_path, 'wb') as f:
        for key in data_dic.keys():
            pickle.dump(key, f)
            pickle.dump(data_dic[key], f)

#-------------------------------------------------------------------------------------

    
