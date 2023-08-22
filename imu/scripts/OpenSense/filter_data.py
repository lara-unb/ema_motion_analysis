
import sys
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


sys.path.append("../../utils/")
from get_data import *
from filters import *
from file_format import *


if __name__ == '__main__':


    file_name = "coleta2_trike"

    # Read JSON file to Data Frame 
    df = pd.read_json(f"data/{file_name}.json", lines=True)


    # Drop rows before 0.1s
    df = df.drop(df[df['time_stamp'] < 1].index)
    df = df.reset_index(drop=True)

    # print(df)


    # Change data format to mach .sto
    format_to_sto('quaternion_ankle', df)
    format_to_sto('quaternion_thigh', df)


    #separate dataframes
    df_thigh = df[['time_stamp', 'quaternion_thigh']].copy()
    df_ankle = df[['time_stamp', 'quaternion_ankle']].copy()

    # print(df_thigh)
    # print(df_ankle)



    #remove duplicadas
    df_thigh_sf = df_thigh.drop_duplicates(subset=['quaternion_thigh'])
    df_thigh_sf = df_thigh_sf.reset_index(drop=True)

    # #remove duplicadas
    df_ankle_sf = df_ankle.drop_duplicates(subset=['quaternion_ankle'])
    df_ankle_sf = df_ankle_sf.reset_index(drop=True)



    # sampling rate
    print(df_thigh_sf.index[-1])
    print(df_thigh_sf.time_stamp.iloc[-1])
    imu_sampling_frequency_thigh = df_thigh_sf.index[-1]/df_thigh_sf.time_stamp.iloc[-1]
    print(imu_sampling_frequency_thigh)

    # sampling rate
    print(df_ankle_sf.index[-1])
    print(df_ankle_sf.time_stamp.iloc[-1])
    imu_sampling_frequency_ankle = df_ankle_sf.index[-1]/df_ankle_sf.time_stamp.iloc[-1]
    print(imu_sampling_frequency_ankle)



    #separate quaterions
    df_thigh[['x', 'y', 'z', 'w']] = df_thigh.quaternion_thigh.str.split(",", expand = True)
    #separate quaternions
    df_ankle[['x', 'y', 'z', 'w']] = df_ankle.quaternion_ankle.str.split(",", expand = True)

    #parametros da filtragem
    quaternions_cols = ['x', 'y', 'z', 'w']
    cutoff = 10 #hz
    order = 2

    df_thigh = filter_quaternions_dataframe(df_thigh, quaternions_cols, cutoff, imu_sampling_frequency_thigh, order)
    df_ankle = filter_quaternions_dataframe(df_ankle, quaternions_cols, cutoff, imu_sampling_frequency_ankle, order)




    # #plot data thigh
    # plt.plot(df_thigh.time_stamp, np.asarray(df_thigh.x, float))
    # plt.plot(df_thigh.time_stamp, np.asarray(df_thigh.y, float))
    # plt.plot(df_thigh.time_stamp, np.asarray(df_thigh.z, float))
    # plt.plot(df_thigh.time_stamp, np.asarray(df_thigh.w, float))
    # #plot data ankle
    # plt.plot(df_ankle.time_stamp, np.asarray(df_ankle.x, float))
    # plt.plot(df_ankle.time_stamp, np.asarray(df_ankle.y, float))
    # plt.plot(df_ankle.time_stamp, np.asarray(df_ankle.z, float))
    # plt.plot(df_ankle.time_stamp, np.asarray(df_ankle.w, float))
    # plt.show()

    df_thigh['quaternion_thigh'] = df_thigh.x.astype(str) +", "+ df_thigh.y.astype(str) + ", " + df_thigh.z.astype(str) + ", " + df_thigh.w.astype(str)
    df_ankle['quaternion_ankle'] = df_ankle.x.astype(str) +", "+ df_ankle.y.astype(str) + ", " + df_ankle.z.astype(str) + ", " + df_ankle.w.astype(str)

    df_final = df_thigh[['time_stamp', 'quaternion_thigh']].copy()
    df_final['quaternion_ankle'] =  df_ankle['quaternion_ankle']


    # Rename columns
    df_final = df_final.rename(columns={'time_stamp':'time', 'quaternion_ankle': 'tibia_r_imu', 'quaternion_thigh': 'femur_r_imu'})


    print(df_final)

    # Save file .sto
    nomeOut_position = f"data/{file_name}_{cutoff}hz_pos.sto"
    nomeOut = f"data/{file_name}_{cutoff}hz_mov.sto"
    df_final.head(1).to_csv(nomeOut_position, header=True, index=None, sep='\t', mode='a')
    df_final.to_csv(nomeOut, header=True, index=None, sep='\t', mode='a')

    # Add header to sto files
    list_of_lines = ['DataType=Quaternion', 'OpenSimVersion=4.4',  'endheader']
    prepend_multiple_lines(nomeOut_position, list_of_lines)
    prepend_multiple_lines(nomeOut, list_of_lines)







    
