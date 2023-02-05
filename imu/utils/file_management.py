""" Defines file managements functions
"""
import pickle
import json
import sys

sys.path.append("../../data_visualization")
import colors as colors
import os
    
def write_to_json_file(file_out_path, data, write_mode='w'):
    """ Write video information to a json file
    Args:
        file_out_path: string with path of the text file
        data: dictionary with the data that should be writen
        write_mode: a string that defines write mode
    """

    # Create outputs directory if needed
    if not os.path.isdir("../data"):  os.makedirs("../data")

    with open(file_out_path+".data", write_mode) as f:
        f.write(json.dumps(data))
        f.write('\n')