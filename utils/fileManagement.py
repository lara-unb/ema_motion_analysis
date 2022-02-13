from PyQt5 import QtGui
from PyQt5.QtWidgets import QWidget, QFileDialog
from PyQt5.QtWidgets import QApplication
import sys


# COMENTARIOS BONITOS EM TUDO DEPOIS!
def readFileDialog(title="Open File", file_type="All Files"):
    app = QApplication(sys.argv)
    qfd = QFileDialog()
    if file_type == "All Files":
        type_filter = "All Files (*)"
    else:
        type_filter = file_type + " (*." + file_type + ")"
    file_path, _ = QFileDialog.getOpenFileName(qfd, title, "", type_filter)
    return file_path