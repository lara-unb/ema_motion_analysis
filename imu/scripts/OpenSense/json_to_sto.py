import pandas as pd
import numpy as np
import json


# Read JSON file to Data Frame 
df = pd.read_json('data/teste.json', lines=True)

# Drop rows before 0.1s
df = df.drop(df[df['time_stamp'] < 0.1].index)
df = df.reset_index(drop=True)


# Change data format to mach .sto
df['quaternion_ankle'] = df['quaternion_ankle'].str.replace('[','', regex=True)
df['quaternion_ankle'] = df['quaternion_ankle'].str.replace(']','', regex=True)
df['quaternion_ankle'] = df['quaternion_ankle'].str.replace('   ',',', regex=True)
df['quaternion_ankle'] = df['quaternion_ankle'].str.replace('  ',',', regex=True)
df['quaternion_ankle'] = df['quaternion_ankle'].str.lstrip()
df['quaternion_ankle'] = df['quaternion_ankle'].str.replace('/^\w+/\s', '', regex=True)

df['quaternion_thigh'] = df['quaternion_thigh'].str.replace('[','', regex=True)
df['quaternion_thigh'] = df['quaternion_thigh'].str.replace(']','', regex=True)
df['quaternion_thigh'] = df['quaternion_thigh'].str.replace('   ',',', regex=True)
df['quaternion_thigh'] = df['quaternion_thigh'].str.replace('  ',',', regex=True)
df['quaternion_thigh'] = df['quaternion_thigh'].str.lstrip()
df['quaternion_thigh'] = df['quaternion_thigh'].str.replace(' ',',', regex=True)


# Rename columns
df = df.rename(columns={'time_stamp':'time', 'quaternion_ankle': 'tibia_r_imu', 'quaternion_thigh': 'femur_r_imu'})


print(df)

# Save file .sto
nomeOut = 'teste.sto'
df.to_csv(nomeOut, header=True, index=None, sep='\t', mode='a')

