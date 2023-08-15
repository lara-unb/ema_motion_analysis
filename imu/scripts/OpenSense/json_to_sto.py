import pandas as pd
import numpy as np
import json


# Read JSON file to Data Frame 
df = pd.read_json('data/coleta1_trike.json', lines=True)


# Drop rows before 0.1s
df = df.drop(df[df['time_stamp'] < 1].index)
df = df.reset_index(drop=True)


# Change data format to mach .sto
#remove []
df['quaternion_ankle'] = df['quaternion_ankle'].str.strip('[]')
df['quaternion_thigh'] = df['quaternion_thigh'].str.strip('[]')

#remove first white space
df['quaternion_ankle'] = df['quaternion_ankle'].str.lstrip()
df['quaternion_ankle'] = df['quaternion_ankle'].str.rstrip()
df['quaternion_thigh'] = df['quaternion_thigh'].str.lstrip()
df['quaternion_thigh'] = df['quaternion_thigh'].str.rstrip()

# create list spliting by whitespace
df['quaternion_ankle'] = df['quaternion_ankle'].str.split(' +')
df['quaternion_thigh'] = df['quaternion_thigh'].str.split(' +')

#convert list to string removing space
df['quaternion_ankle'] = [','.join(map(str, l)) for l in df['quaternion_ankle']]
df['quaternion_thigh'] = [','.join(map(str, l)) for l in df['quaternion_thigh']]


# Rename columns
df = df.rename(columns={'time_stamp':'time', 'quaternion_ankle': 'tibia_r_imu', 'quaternion_thigh': 'femur_r_imu'})

#df['calcn_r_imu'] = df['tibia_r_imu']

print(df)

# Save file .sto
nomeOut_position = 'data/coleta1_trike.sto'
nomeOut = 'data/coleta1_trike.sto'
df.head(1).to_csv(nomeOut_position, header=True, index=None, sep='\t', mode='a')

df.to_csv(nomeOut, header=True, index=None, sep='\t', mode='a')

