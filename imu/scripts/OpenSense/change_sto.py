import pandas as pd
import numpy as np
import json
import sys

sys.path.append("../../utils/")
from file_format import *



# Read JSON file to Data Frame 
df = pd.read_csv('file.sto', sep='\t')


df2 = df[["time", "Gear_imu"]].copy()
print(df2)

# Save file .sto
df2.to_csv('new_file.sto', header=True, index=None, sep='\t', mode='a')



# Drop rows before 0.1s
# df = df.drop(df[df['time_stamp'] < 1].index)
# df = df.reset_index(drop=True)


# # Change data format to mach .sto
# format_to_sto('quaternion_ankle', df)
# format_to_sto('quaternion_thigh', df)


# # Rename columns
# df = df.rename(columns={'time_stamp':'time', 'quaternion_ankle': 'tibia_r_imu', 'quaternion_thigh': 'femur_r_imu'})


# print(df)

# # Save file .sto
# nomeOut_position = 'data/coleta3_trike_pos.sto'
# nomeOut = 'data/coleta3_trike_mov.sto'
# df.head(1).to_csv(nomeOut_position, header=True, index=None, sep='\t', mode='a')
# df.to_csv(nomeOut, header=True, index=None, sep='\t', mode='a')

# # Add header to sto files
# list_of_lines = ['DataType=Quaternion', 'OpenSimVersion=4.4',  'endheader']
# prepend_multiple_lines(nomeOut_position, list_of_lines)
# prepend_multiple_lines(nomeOut, list_of_lines)

