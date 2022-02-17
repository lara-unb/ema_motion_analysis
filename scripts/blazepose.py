# Cabeçalho ? 
# Esse código é uma modificação da solução demonstração disponível em:
# https://google.github.io/mediapipe/solutions/pose.html#python-solution-api


import sys
from turtle import color
import cv2
import mediapipe as mp
import numpy as np

sys.path.append("../utils/")
import colors
import fileManagement
import drawing
import poses

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose

# Importar de outro arquivo...
VIDEOS = {
    1: ("right","/../examples/right-rafilsk1.mp4"),
    2: ("frontal", "/../examples/frontal-girl.mp4")
}

THRESHOLD = 0.3


# Usar interface de usuário aqui -> já feita
video_path = fileManagement.getAbsolutePath() + VIDEOS[2][1]
cap = cv2.VideoCapture(video_path)

with mp_pose.Pose(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as pose: 

  while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
      break

    # To improve performance, optionally mark the image as not writeable to
    # pass by reference.
    frame.flags.writeable = False
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(frame)

    # Draw the pose annotation on the image.
    frame.flags.writeable = True
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

    # Select correct pose 
    profile = 'frontal'
    pose_selected = poses.JUMP_FRONTAL
    if(profile == "left"):
      pose_selected = poses.JUMP_SAGITTAL_LEFT
    elif(profile == "right"):
      pose_selected = poses.JUMP_SAGITTAL_RIGHT

    # selected_joints = selectJoints(results, frame)
    keypoint_pairings = poses.getPairings(pose_selected, poses.KEYPOINT_DICT_BLAZEPOSE, mp_pose.POSE_CONNECTIONS, neural_network="blazepose")
    selected_joints = poses.selectJoints(frame, results.pose_landmarks, poses.JUMP_FRONTAL, poses.KEYPOINT_DICT_BLAZEPOSE, 'blazepose')

    # Tudo feio, mas tudo funcionando // Melhorar isso!!
    print(keypoint_pairings)
    #  {(1, 0): 'y', (1, 3): 'm', (3, 5): 'm', (0, 2): 'c', (2, 4): 'c'}
    drawing.draw_connections(frame, selected_joints, keypoint_pairings)
    drawing.draw_keypoints(frame,selected_joints)

    print(colors.RED, "---", colors.RESET)

    # Show image
    cv2.imshow('MediaPipe Pose', frame) 
    if cv2.waitKey(5) & 0xFF == 27:
      break
cap.release()