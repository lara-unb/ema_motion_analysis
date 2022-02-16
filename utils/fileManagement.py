from PyQt5 import QtGui
from PyQt5.QtWidgets import QWidget, QFileDialog
from PyQt5.QtWidgets import QApplication
import sys
import colors

import os

#-------------------------------------------------------------------------------------
# Get absolute path to root project
def getAbsolutePath():
    absolute_main_path = os.path.dirname(os.path.abspath(__file__)).split("\\")[:-1]
    return "\\".join(absolute_main_path)
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
        return

#-------------------------------------------------------------------------------------

    
