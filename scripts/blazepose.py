import sys
from turtle import color
import cv2
import mediapipe as mp
import numpy as np

sys.path.append("../utils/")
import colors
import fileManagement
import drawing

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose

# For static images:
IMAGE_FILES = []
BG_COLOR = (192, 192, 192) # gray


VIDEOS = {
    1: ("right","/../examples/right-rafilsk1.mp4"),
    2: ("frontal", "/../examples/frontal-girl.mp4")
}

THRESHOLD = 0.5


def selectJoints(results, image):
  image_height, image_width, _ = image.shape
  landmarks_edited = [
    [
      results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_HIP].x * image_width, 
      results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_HIP].y * image_height
  ],
    [
      results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_KNEE].x * image_width, 
      results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_KNEE].y * image_height
  ],
    [
      results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_ANKLE].x * image_width, 
    results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_ANKLE].y * image_height

  ]]

  return landmarks_edited


# For webcam input:
video_path = fileManagement.getAbsolutePath() + VIDEOS[1][1]
print(video_path)
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

    # Landmarks
    # landmarks_edited = []



    selected_joints = selectJoints(results, frame)

    # mp_drawing.draw_landmarks(
    #     frame,
    #     results.pose_landmarks,
    #     mp_pose.POSE_CONNECTIONS,
    #     landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())

    # Tudo feio, mas tudo funcionando // Melhorar isso!!
    drawing.draw_connections(frame, selected_joints, {(0, 1): 'c', (1, 2): 'c'})
    drawing.draw_keypoints(frame,selected_joints)

    # Show image
    cv2.imshow('MediaPipe Pose', frame) 
    if cv2.waitKey(5) & 0xFF == 27:
      break
cap.release()