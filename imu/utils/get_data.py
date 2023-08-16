from tkinter import E
from sympy import re
# from fileManagement import readACPFile, openFileACP2
import json
import matplotlib.pyplot as plt
import numpy as np
import csv
# from constants import vicon_lower_body
from more_itertools import locate


# This part should be remove in the next collects - Fixed in save function
def remove_especial_chars(text: str):
    return text.replace('[', "").replace(']', "").replace(',', '.').split(' ')

def clean(vec: list):
    return list(filter(lambda x: x != '', vec))

def to_float(vec: list):
    return list(float(v) for v in vec)

def convert_list_of_strings_to_list_of_lists(list_of_strings: list):
    list_of_strings = [remove_especial_chars(a) for a in list_of_strings]
    list_of_strings = [clean(a) for a in list_of_strings]
    list_of_strings = [to_float(a) for a in list_of_strings]
    return np.array(list_of_strings)

def calc_resultant_acc(acc):
    # Calculate resultant accelartion vector
    resultant_acc = np.array([])
    for a in acc:
        aux = (a[0]**2+a[1]**2+a[2]**2)**0.5
        resultant_acc = np.append(resultant_acc, aux)
    return resultant_acc
    

# def read_acp(file_path):
#     fp_data, var_names, jump_type = readACPFile(file_path)
#     pp_dic, proc_dic = openFileACP2(file_path + '2')
#     force = fp_data['Raw Fz (N)']
#     time = fp_data['Time (s)']
#     fs = int(1/(time[1]-time[0]))
#     time_of_flight = proc_dic['Time of Flight (ms)']
#     jump_high = proc_dic['Jump Height ToF (cm)']
#     return force, time, time_of_flight, jump_high


def read_json(file_path, 
              data_format = {
                "sensor_acceleration": "acc",
                "quaternion": "quaternion"
              },
            convert_string_to_list = False,
            remove_redundant_data = False):

    data_list = [json.loads(line) for line in open(file_path, 'r')]
    data_list[-2:]

    # Initialize sensor data
    sensor_data = {}
    for required_data in data_format.keys():
        sensor_data[required_data] = {
            'time_stamp': [],
            'values' : []
        }


    time_stamp = []

    # Iterating through the json list and adding desired data
    for d in data_list:
        time_stamp.append(d['time_stamp'])  
        for required_data in data_format.keys():
            sensor_data[required_data]['values'].append(d[data_format[required_data]])

    if convert_string_to_list:
        for required_data in data_format:
            sensor_data[required_data]['values'] = np.array(convert_list_of_strings_to_list_of_lists(sensor_data[required_data]['values']))
    else:
        for required_data in data_format:
            sensor_data[required_data]['values'] = np.array(sensor_data[required_data]['values'])
    
    # Some data where recorded redundantly, this script remove it
    if remove_redundant_data:
        for required_data in data_format.keys():
            cleaned_sensor_time = []
            cleaned_sensor_data = []
            print
            for index in range(len(sensor_data[required_data]['values'])):
                
                if(index != 0):
                    # print(index, "Current:", sensor_data[required_data]['values'][index])
                    # print(index-1, "Previous:", sensor_data[required_data]['values'][index-1])
                    if(not np.array_equal(sensor_data[required_data]['values'][index],sensor_data[required_data]['values'][index-1])):
                        cleaned_sensor_data.append(sensor_data[required_data]['values'][index])
                        cleaned_sensor_time.append(time_stamp[index])
                else:
                    cleaned_sensor_data.append(sensor_data[required_data]['values'][index])
                    cleaned_sensor_time.append(time_stamp[index])

            sensor_data[required_data]['values'] = np.array(cleaned_sensor_data) 
            sensor_data[required_data]['time_stamp']  = np.array(cleaned_sensor_time)

    return time_stamp, sensor_data

def contain_header(row):
    for column in row:
        if 'Devices' in column:
            return True, 'Devices'
        elif "Trajectories" in column:
            return True, 'Trajectories'
    return False, ''

def read_csv(path):
    data = {}

    rows = []
    with open(path, 'r') as file:
        csvreader = csv.reader(file)
        type = None
        for row in csvreader:
            if contain_header(row)[0]:
                has_header, metric_type = contain_header(row)
                device_fps = next(csvreader)
                device_details = next(csvreader)
                metrics = next(csvreader)
                metrics_units = next(csvreader)
                data[metric_type] = {
                    "device_fps": device_fps,
                    "device_details": device_details,
                    "metrics": metrics,
                    "metrics_units": metrics_units,
                    "values": []
                }
            elif metric_type is not None:
                if(len(row) != 0):
                    data[metric_type]["values"].append(row)

    return data

def find_indices(list_to_check, item_to_find):
    indices = locate(list_to_check, lambda x: x == item_to_find)
    return list(indices)

# def read_file_vicon(file_path, 
#         data_format={ 
#             "force":"two_platforms"
#         },
#         subject="Davi Muniz", 
#         types = ["Trajectories", "Devices"], makers=["RTOE"]):
#     data = read_csv(file_path)
#     forces = {}
#     position_fps, force_fps = 0, 0
#     positions = {}
#     velocities = {}
#     accelerations = {}
#     data_returned = {}

#     if "Devices" in types:
#         data_values = data["Devices"]["values"]
#         data_values = np.array(data_values, dtype=np.float64)
        
#         try:
#             force1_index = data["Devices"]["device_details"].index("AMTI 400600 V1.0 #1 - Force")
#         except:
#             force1_index = data["Devices"]["device_details"].index("Imported AMTI 400600 V1.0 #1 - Force")
#         force1 = data_values[:, force1_index:force1_index+3]
#         forces["force1"] = force1
        
#         if data_format["force"] == "two_platforms":
#             try:
#                 force2_index = data["Devices"]["device_details"].index("AMTI 400600 V1.0 #2 - Force")
#             except:
#                 force2_index = data["Devices"]["device_details"].index("Imported AMTI 400600 V1.0 #2 - Force")
#             force2 = data_values[:, force2_index:force2_index+3]
#             forces["force2"] = force2 

#         force_fps = float(data["Devices"]["device_fps"][0])
    
#     if "Trajectories" in types:
#         data_values = data["Trajectories"]["values"]
#         # Fill gaps with zeros (could be better - i.e.: average)
#         for i in range(len(data_values)): 
#             for j in range(len(data_values[i])):
#                 if data_values[i][j] == "": data_values[i][j] = '0'
        
#         data_values = np.array(data_values, dtype=np.float64)
#         i = 0
#         for model_key in vicon_lower_body.keys():
#             try:
#                 indexes = find_indices(data["Trajectories"]["device_details"], subject+":"+model_key)
#                 position_index = indexes[0]
#                 velocity_index = indexes[1]
#                 acceleration_index = indexes[2]


#                 positions[model_key] = data_values[:, position_index:position_index+3]
#                 velocities[model_key] = data_values[:, velocity_index:velocity_index+3]
#                 accelerations[model_key] = data_values[:, acceleration_index:acceleration_index+3]


#             except:
#                 position_index = data["Trajectories"]["device_details"].index(subject+":"+model_key)
                

#                 if(position_index != -1):
#                     positions[model_key] = data_values[:, position_index:position_index+3]
        
        
#         data_fps = float(data["Trajectories"]["device_fps"][0])
#         data_returned = {
#             "positions": positions,
#         }
#         if(not not velocities):
#             data_returned["velocities"] = velocities
#         if(not not accelerations):
#              data_returned["accelerations"] = accelerations


#     return forces, force_fps, data_returned, data_fps