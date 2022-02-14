import numpy as np
import sys
import os
import pickle
import importlib
import pandas as pd
import math
import cv2
import json
from scipy import integrate
from PyQt5.QtWidgets import QApplication, QFileDialog
from pykalman import KalmanFilter

# Dictionary to map joints of body part
KEYPOINT_DICT = {
    'nose':0,
    'left_eye':1,
    'right_eye':2,
    'left_ear':3,
    'right_ear':4,
    'left_shoulder':5,
    'right_shoulder':6,
    'left_elbow':7,
    'right_elbow':8,
    'left_wrist':9,
    'right_wrist':10,
    'left_hip':11,
    'right_hip':12,
    'left_knee':13,
    'right_knee':14,
    'left_ankle':15,
    'right_ankle':16
} 

# Mover isso aqui para outra pasta!!!
EDGES = {
    (0, 1): 'm',
    (0, 2): 'c',
    (1, 3): 'm',
    (2, 4): 'c',
    (0, 5): 'm',
    (0, 6): 'c',
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

def writeToDATA(file_path, data, write_mode='w'):
    with open(file_path, write_mode) as f:
        json.dump(data, f)

def transformDATA(kp_w_scores_vec, confidence_threshold, frame_width, frame_height):
    keypoints_vec = np.zeros([len(list(KEYPOINT_DICT.values())), 2])
    
    y, x, c = frame_width, frame_height, 3
    shaped = np.squeeze(np.multiply(kp_w_scores_vec, [y,x,1]))
    
    j = 0
    for i in range(len(shaped)):
        if i in list(KEYPOINT_DICT.values()):
            ky, kx, kp_conf = shaped[i]
            if kp_conf > confidence_threshold:
                keypoints_vec[j, 0] = kx
                keypoints_vec[j, 1] = ky
            else:
                keypoints_vec[j, 0] = np.nan
                keypoints_vec[j, 1] = np.nan
            j+=1
    return keypoints_vec

def norm_signal(sig):
#     sig_first = 0
#     for i in range(len(sig)):
#         if not np.isnan(sig[i]):
#             sig_first = sig[i]
#             break
    sig_mean = np.nanmean(sig)
    sig_std = np.nanstd(sig)
    norm_sig = (sig - sig_mean) / sig_std
#     norm_sig += sig_first
    return norm_sig

def getVideoInfo(video_path):
    video_info = {}
    cap = cv2.VideoCapture(video_path)
    has_frame, image = cap.read()
    video_info['fps'] = int(cap.get(cv2.CAP_PROP_FPS))
    video_info['n_frames'] = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    video_info['frame_width'] = image.shape[0]
    video_info['frame_height'] = image.shape[1]
    cap.release()
    return video_info

def readFolderDialog(title="Open folder"):
    app = QApplication(sys.argv)
    qfd = QFileDialog()
    folder_path = QFileDialog.getExistingDirectory(
        qfd, title, "")
    return folder_path

def getFolderInDirectory(dir_path):
    directory_list = [name for name in os.listdir(dir_path) if os.path.isdir(os.path.join(dir_path, name))]
    return directory_list

def getFilesInDirectory(dir_path, file_ext):
    output_list = []
    files_list = [f for f in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, f))]
    for f in files_list:
        if f.endswith(file_ext):
            output_list.append(f)
    return output_list

def readFileDialog(title="Open file", file_type="All Files"):
    app = QApplication(sys.argv)
    qfd = QFileDialog()
    if file_type == "All Files":
        type_filter = "All Files (*)"
    else:
        type_filter = file_type + " (*." + file_type + ")"
    file_path, _ = QFileDialog.getOpenFileName(qfd, title, "", type_filter)
    return file_path

def readExcelFile(file_path):
    data_excel = pd.read_excel(file_path)
    var_names = [col for col in data_excel.columns if 'Unnamed' not in col]
    data = {}
    for key in var_names:
        data[key] = data_excel[key][0]
    return data, var_names

def readForceFile(file_path):
    i=1
    var_names = []
    with open(file_path, 'r') as f:
        for line_str in f:
            if 'Time (s)' in line_str:
                var_names = line_str.split(f'\t')
                break
            i+=1
    force_data_arr = np.loadtxt(file_path, skiprows=i)
    force_data_dic = {}
    for key in var_names:
        force_data_dic[key] = force_data_arr[:, var_names.index(key)]
    
    return force_data_dic, var_names

def save_to_file(data_dic, file_path):
    with open(file_path, 'wb') as f:
        for key in data_dic.keys():
            pickle.dump(key, f)
            pickle.dump(data_dic[key], f)

def parse_pickle_file(file_path):
    data = {}
    # Load data
    with open(file_path, 'rb') as f:
        try:
            while True:
                data.update({pickle.load(f): pickle.load(f)})

        except EOFError:
            pass

    var_names = []
    for k, v in data.items():
        var_names.append(k)

    return data, var_names

def parse_data_file(file_path):
    keypoints_vec = []
    angles_vec = []
    with open(file_path, 'r') as f:
        for i, line in enumerate(f):
            if i == 0:
                metadata = json.loads(line)
            else:
                data_line = json.loads(line)
                keypoints_vec.append(data_line["keypoints"])
                try:
                    angles_vec.append(data_line["angles"])
                except:
                    angles = []
    data = {}
    data["keypoints"] = np.array(keypoints_vec).astype(float)
    data["angles"] = np.array(angles_vec).astype(float)
    data["metadata"] = metadata
    var_names = ["metadata", "keypoints", "angles"]
    return data, var_names

def function_from_file(file_path, function_name):
    folder_path = ""
    for string in file_path.split("/")[:-1]:
        folder_path += string + "/"
    file_name = file_path.split("/")[-1].split(".")[0]
    if folder_path not in sys.path:
        sys.path.append(folder_path)
    processing = __import__(file_name)
    importlib.reload(sys.modules[file_name])
    processing = __import__(file_name)
    processing_function = getattr(processing, function_name)
    return processing_function

def closestValueIdx(array, value):
    arr = np.array(array)
    idx = (np.abs(array - value)).argmin()
    return idx

def find(array_condition, start=0, end=-1, num=1, order='first', direction='foward'):
    if direction == 'foward':
        if end == -1:
            end = len(array_condition)
        values = []
        arr_values = np.where(array_condition[start:end])[0]
        if order == 'first':
            values = arr_values[:num]
        elif order == 'last':
            values = arr_values[-num:len(arr_values)]
        elif order == 'mean':
            values.append(np.mean(arr_values))
        if len(values) == 1:
            return values[0] + start
        else:
            return np.array(values) + start
    elif direction == 'backwards':
        values = []
        arr_values = np.where(array_condition[end:start])[0]
        if order == 'first':
            values = arr_values[-num:len(arr_values)]
        elif order == 'last':
            values = arr_values[:num]
        elif order == 'mean':
            values.append(np.mean(arr_values))
        if len(values) == 1:
            return values[0] + end
        else:
            return np.array(values) + end
    
def findBestWeighingInterval(corrected_force, first_movement_estimate, weighing_interval_n):
    std_1s = np.std(corrected_force[:weighing_interval_n])
    mean_1s = np.mean(corrected_force[:weighing_interval_n])
    
    min_std = std_1s
    best_interval = [0, weighing_interval_n-1]
    for idx in range(weighing_interval_n+1, first_movement_estimate):
        next_std = np.std(corrected_force[idx-weighing_interval_n:idx])
        if next_std < min_std:
            min_std = next_std
            best_interval = [idx-weighing_interval_n, idx-1]
#     for j in range(best_interval[0], best_interval[1]+1):
#         if np.abs(corrected_force[j]-mean_1s) > std_1s*5:
#             break
#         lower_best_interval = [best_interval[0], j]
#     if sum(lower_best_interval) < sum(best_interval):
#         for j in range(best_interval[1], best_interval[0]-1, -1):
#             if np.abs(corrected_force[j]-mean_1s) > std_1s*5:
#                 break
#             upper_best_interval = [best_interval[0], j]

#         if sum(lower_best_interval) >= sum(upper_best_interval):
#             best_interval = lower_best_interval
#         else:
#             best_interval = upper_best_interval
    return best_interval

def integrateSignal(signal, fs):
    out = []
    aux = 0
    for i in range(0, len(signal) - 1):
        sigInst = integrate.trapz(signal[i:i + 2]) / fs
        aux = aux + sigInst
        out.append(aux)

    out.append(out[-1])
    out = np.array(out)
    return out

def getImpulse(signal, fs):
    integral = 0
    for i in range(0, len(signal)):
        velInst = integrate.trapz(signal[i:i + 2]) / fs
        integral = integral + velInst
    return integral

def missingDataInterpolation(X, interp='cubic'):
    X = np.where(X==0, np.nan, X)
    X = pd.Series(X)
    X_out = X.interpolate(limit_direction='both', kind=interp)
    return X_out

def fillwInterp(keypoints_vector):
    for i in range(keypoints_vector.shape[1]):
        keypoints_vector[:,i,0] = missingDataInterpolation(keypoints_vector[:, i, 0])
        keypoints_vector[:,i,1] = missingDataInterpolation(keypoints_vector[:, i, 1])
    return keypoints_vector.astype(int)

def kalmanFilter(measurements):

	initial_state_mean = [measurements[0, 0], 0,
											measurements[0, 1], 0]

	transition_matrix = [[1, 1, 0, 0],
											[0, 1, 0, 0],
											[0, 0, 1, 1],
											[0, 0, 0, 1]]

	observation_matrix = [[1, 0, 0, 0],
											[0, 0, 1, 0]]

	kf1 = KalmanFilter(transition_matrices = transition_matrix,
									observation_matrices = observation_matrix,
									initial_state_mean = initial_state_mean)

	kf1 = kf1.em(measurements, n_iter=5)
	(smoothed_state_means, smoothed_state_covariances) = kf1.smooth(measurements)

	kf2 = KalmanFilter(transition_matrices = transition_matrix,
						observation_matrices = observation_matrix,
						initial_state_mean = initial_state_mean,
						observation_covariance = 10*kf1.observation_covariance,
						em_vars=['transition_covariance', 'initial_state_covariance'])

	kf2 = kf2.em(measurements, n_iter=5)
	(smoothed_state_means, smoothed_state_covariances)  = kf2.smooth(measurements)
	
	return smoothed_state_means[:, 0], smoothed_state_means[:, 2]

def processing_function(keypoints_vec):
	print("Starting Kalman")
	for i in range(keypoints_vec.shape[1]):
		measurements = np.copy(keypoints_vec[:, i])
		keypoints_vec[:, i, 0], keypoints_vec[:, i, 1] = kalmanFilter(measurements)
        # print(f"[{i}/{keypoints_vec.shape[1]-1}]", end='\r')
	keypoints_vec = np.array(keypoints_vec)
	return keypoints_vec

def getAngleLimited(A, B, O, allow_neg=False):
    if allow_neg:
        try:
            ang = math.degrees(math.atan2(
                B[1]-O[1], B[0]-O[0]) - math.atan2(A[1]-O[1], A[0]-O[0]))
            if ang > 180:
                ang = 360 - ang
        except:
            ang = np.nan
    else:
        try:
            ang = math.degrees(math.atan2(
                B[1]-O[1], B[0]-O[0]) - math.atan2(A[1]-O[1], A[0]-O[0]))
            if ang < 0:
                ang += 360
            if ang > 180:
                ang = 360 - ang
        except:
            ang = np.nan
    return ang

def getAngles(kp_vec):
    angles = np.zeros(len(kp_vec))
    for i in range(len(kp_vec)):
        angles[i] = getAngleLimited(kp_vec[i, 0], kp_vec[i, 2], kp_vec[i, 1])
    return angles