
import sys
import matplotlib.pyplot as plt


sys.path.append("../../utils/")
from get_data import *
from filters import *


if __name__ == '__main__':

    file_name = "coleta1_trike"
    # try: 
    imu_time, quaternion_data = read_json(
    f"data/{file_name}.json",
    data_format = {
        "quaternion_thigh": "quaternion_thigh",
        "quaternion_ankle": "quaternion_ankle"
    },
    convert_string_to_list=False,
    remove_redundant_data = True)
    # except:
    #     print("Erro coletando dado da IMU.")
    #     print(f"Arquivo: {file_name}")
    #     return dataframe
    

    
    # Get time axis
    time_stamp = quaternion_data['quaternion_thigh']['time_stamp']
    # Get imu quaternion data
    quaternion_thigh = quaternion_data['quaternion_thigh']['values']
    imu_sampling_frequency = len(imu_time)/(imu_time[-1]-imu_time[0])

    # Get imu quaternion data
    quaternion_ankle = quaternion_data['quaternion_ankle']['values']

    print(quaternion_thigh)
    print(quaternion_ankle)


    # plt.plot(time_stamp, quaternion_thigh[:, 0])
    # #plt.savefig("data/coleta1_coxa_acc3"+ ".pdf") # str(time.time()) +
    # plt.show()

    # butter_highpass_filter(data, cutoff, fs, order=5)


    
