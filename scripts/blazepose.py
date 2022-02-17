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
import userInterface

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose


THRESHOLD = 0.3

def predictionToVideo(video_path, video_out_path, profile):
  # Get video object
  video = cv2.VideoCapture(video_path)
  if(not fileManagement.videoCheck(video)):
    return

  # Aqui ele já aplica a rede -> ver qual parâmetro desses que é o threshold - PERGUNTAR VICTOR
  with mp_pose.Pose(
      min_detection_confidence=THRESHOLD,
      min_tracking_confidence=THRESHOLD) as pose: 

    while video.isOpened():
      ret, frame = video.read()
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
      pose_selected = poses.JUMP_FRONTAL
      if(profile == "left"):
        pose_selected = poses.JUMP_SAGITTAL_LEFT
      elif(profile == "right"):
        pose_selected = poses.JUMP_SAGITTAL_RIGHT

      # selected_joints = selectJoints(results, frame)
      keypoint_pairings = poses.getPairings(pose_selected, poses.KEYPOINT_DICT_BLAZEPOSE, mp_pose.POSE_CONNECTIONS, neural_network="blazepose")
      selected_joints = poses.selectJoints(frame, results.pose_landmarks, pose_selected, poses.KEYPOINT_DICT_BLAZEPOSE, 'blazepose')

      # Draw joints and pairings
      drawing.draw_connections(frame, selected_joints, keypoint_pairings)
      drawing.draw_keypoints(frame,selected_joints)

      # Show image
      cv2.imshow('MediaPipe Pose', frame) 
      if cv2.waitKey(5) & 0xFF == 27:
        break
  video.release()


if __name__ == "__main__":
  video_path, video_out_path, profile = userInterface.initialMenu()
  predictionToVideo(video_path, video_out_path, profile)