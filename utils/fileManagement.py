from PyQt5 import QtGui
from PyQt5.QtWidgets import QWidget, QFileDialog
from PyQt5.QtWidgets import QApplication
import pickle

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
#-------------------------------------------------------------------------------------
# Generate output file
def save_to_file(data_dic, file_path):
    with open(file_path, 'wb') as f:
        for key in data_dic.keys():
            pickle.dump(key, f)
            pickle.dump(data_dic[key], f)

    # Exemplo de uso
    
    # 'force': force_cropped, 'force_time': time_cropped,
    # 'audio': audio_cropped, 'audio_time': audiot_cropped,
    data = {​​​​​​​
    'f_info': {​​​​​​​'fs': fs}​​​​​​​, 
    'v_info': v_info,
    'kp': kp_vec, # 'angles': ang,
    'kp_w_scores_vec': kp_w_scores_vec,
    'kp_time': video_time
    }

    save_to_file(data, out_path)   
    
