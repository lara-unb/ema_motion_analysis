import pandas as pd
import numpy as np
import json
import sys

sys.path.append("../../utils/")
from file_format import *


# Read JSON file to Data Frame 
df = pd.read_json('data/coleta1_trike.json', lines=True)


# Drop rows before 0.1s
df = df.drop(df[df['time_stamp'] < 1].index)
df = df.reset_index(drop=True)


# Change data format to mach .sto
format_to_sto('quaternion_ankle', df)
format_to_sto('quaternion_thigh', df)


# Rename columns
df = df.rename(columns={'time_stamp':'time', 'quaternion_ankle': 'tibia_r_imu', 'quaternion_thigh': 'femur_r_imu'})

#df['calcn_r_imu'] = df['tibia_r_imu']

print(df)

# Save file .sto
nomeOut_position = 'data/coleta1_trike_posTESTE.sto'
nomeOut = 'data/coleta1_trike_movTESTE.sto'
df.head(1).to_csv(nomeOut_position, header=True, index=None, sep='\t', mode='a')

df.to_csv(nomeOut, header=True, index=None, sep='\t', mode='a')

# Add header 
list_of_lines = ['DataType=Quaternion', 'OpenSimVersion=4.4',  'endheader']
prepend_multiple_lines(nomeOut_position, list_of_lines)
prepend_multiple_lines(nomeOut, list_of_lines)

