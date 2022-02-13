import tensorflow as tf
import numpy as np
from matplotlib import pyplot as plt
import cv2

import sys

sys.path.append("../utils/")
import fileManagement
import drawing
import colors


# Mover isso aqui para outra pasta!!!
EDGES = {
    (0, 1): 'm',
    (0, 2): 'c',
    (1, 3): 'm',
    (2, 4): 'c',
    # (0, 5): 'm',
    # (0, 6): 'c',
    (5, 7): 'm',
    (7, 9): 'm',
    (6, 8): 'c',
    (8, 10): 'c',
    (5, 6): 'y',
    (5, 11): 'm',
    (6, 12): 'c',
    (11, 12): 'y',
    (11, 13): 'm',
    (13, 15): 'm',
    (12, 14): 'c',
    (14, 16): 'c'
}





def predictionToVideo(interpreter, video_path, video_out_path):
    cap = cv2.VideoCapture(video_path)
    if(not cap.isOpened()):
        print(colors.RED, "Couldn't open video!", colors.RESET)
        return

    has_frame, image = cap.read()
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    n_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    frame_width = image.shape[0]
    frame_height = image.shape[1]
    cap.release() 

    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    fourcc = cv2.VideoWriter_fourcc('M','J','P','G')

    cap = cv2.VideoCapture(video_path)

    out = cv2.VideoWriter(video_out_path, fourcc, fps, (frame_width,frame_height))
    while True:
        ret, frame = cap.read()
        # frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
        if not ret:
            break
        
        # Reshape image
        img = frame.copy()
        img = tf.image.resize_with_pad(np.expand_dims(img, axis=0), 192,192)
        input_image = tf.cast(img, dtype=tf.float32)
        
        # Setup input and output 
        input_details = interpreter.get_input_details()
        output_details = interpreter.get_output_details()
        
        # Make predictions 
        interpreter.set_tensor(input_details[0]['index'], np.array(input_image))
        interpreter.invoke()
        keypoints_with_scores = interpreter.get_tensor(output_details[0]['index'])
        
        # Rendering 
        drawing.draw_connections(frame, keypoints_with_scores, EDGES, 0.3)
        drawing.draw_keypoints(frame, keypoints_with_scores, 0.3)
        
        out.write(frame)

        cv2.imshow('MoveNet Lightning', frame)

        
        k = cv2.waitKey(25) & 0xFF
        if k == 27:
            break
            
    cap.release()
    cv2.destroyAllWindows()
    out.release()


if __name__ == "__main__":
    interpreter = tf.lite.Interpreter(model_path='lite-model_movenet_singlepose_lightning_3.tflite')
    interpreter.allocate_tensors()
    video_path = fileManagement.readFileDialog("Open video file")
    video_out_path = video_path.split(".")[0] + "_mnl.avi"
    predictionToVideo(interpreter, video_path, video_out_path)