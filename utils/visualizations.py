import matplotlib.pyplot as plt
import numpy as np
import cv2

linewidth = 3
circle_radius = 5
detection_thres = 0.3

# Dictionary to map joints of body part
KEYPOINT_DICT = {
#     'nose':0,
#     'left_eye':1,
#     'right_eye':2,
#     'left_ear':3,
#     'right_ear':4,
#     'left_shoulder':5,
#     'right_shoulder':6,
#     'left_elbow':7,
#     'right_elbow':8,
#     'left_wrist':9,
#     'right_wrist':10,
#     'left_hip':11,
    'right_hip':12,
#     'left_knee':13,
    'right_knee':14,
#     'left_ankle':15,
    'right_ankle':16
} 

EDGES = {
#     (0, 1): 'm',
#     (0, 2): 'c',
#     (1, 3): 'm',
#     (2, 4): 'c',
    # (0, 5): 'm',
    # (0, 6): 'c',
#     (5, 7): 'm',
#     (7, 9): 'm',
#     (6, 8): 'c',
#     (8, 10): 'c',
#     (5, 6): 'y',
#     (5, 11): 'm',
#     (6, 12): 'c',
#     (11, 12): 'y',
#     (11, 13): 'm',
#     (13, 15): 'm',
    (12, 14): 'c',
    (14, 16): 'c'
}

def draw_keypoints(frame, keypoints, thres=0.1):
    y, x, c = frame.shape
    shaped = np.squeeze(np.multiply(keypoints, [y,x,1]))
    
    for i in range(len(shaped)):
        if i in list(KEYPOINT_DICT.values()):
            ky, kx, kp_conf = shaped[i]
            if kp_conf > thres:
                cv2.circle(frame, (int(kx), int(ky)), circle_radius, (0,255,0), -1)

def draw_connections(frame, keypoints, edges=EDGES, thres=0.1):
    y, x, c = frame.shape
    shaped = np.squeeze(np.multiply(keypoints, [y,x,1]))
    
    for edge, color in edges.items():
        p1, p2 = edge
        y1, x1, c1 = shaped[p1]
        y2, x2, c2 = shaped[p2]
        
        if (c1 > thres) & (c2 > thres):      
            cv2.line(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0,0,0), linewidth)

def plotJumpMoments(signal, t, jump_moments_idx, jump_moments_names, savefig=False, figname=None,
                    markers=['^', 's', 'p', 'h', '8'],
                    moments_colors=['red', 'green', 'blue', 'orange', 'purple']):
    
    plt.figure(figsize=[7, 3])
    plt.plot(t, signal, label='jump signal', color='gray')
    for i in range(len(jump_moments_names)):
        plt.scatter(t[jump_moments_idx[i]], signal[jump_moments_idx[i]],
                    marker=markers[i], color=moments_colors[i], label=jump_moments_names[i])
    plt.title("Jump moments")
    plt.ylabel("Force (N)")
    plt.xlabel("Time (s)")
    plt.grid(True)
    plt.legend(loc='center right', bbox_to_anchor=(1, 0.5))
    if savefig:
        plt.savefig("../images/" + figname + ".png", bbox_inches='tight')
    plt.show()


def plotSignals(time_list, signal_list, labels=[], colors=[], grid=True, title="", xlabel="", ylabel=""):
    if type(signal_list) is list:
        plt.figure(figsize=[9, 5])
        for i in range(len(signal_list)):
            if (len(labels) > 0) and (len(colors) > 0):
                plt.plot(time_list[i], signal_list[i], label=labels[i], color=colors[i])
                plt.legend()
            elif (len(labels) > 0) and (len(colors) == 0):
                plt.plot(time_list[i], signal_list[i], label=labels[i])
                plt.legend()
            elif (len(labels) == 0) and (len(colors) > 0):
                plt.plot(time_list[i], signal_list[i], color=colors[i])
            else:
                plt.plot(time_list[i], signal_list[i])
        if grid:
            plt.grid(True)
        if title != "":
            plt.title(title)
        if xlabel != "":
            plt.xlabel(xlabel)
        if ylabel != "":
            plt.xlabel(ylabel)
        plt.show()
    else:
        print('Invalid input format')

def plotFilterZoom(time_list, signal_list, xlim=[], labels=[], colors=[], grid=True, title="", xlabel="", ylabel=""):
    if type(signal_list) is list:
        plt.figure(figsize=[9, 5])
        for i in range(len(signal_list)):
            if (len(labels) > 0) and (len(colors) > 0):
                plt.plot(time_list[i], signal_list[i], label=labels[i], color=colors[i])
                plt.legend()
            elif (len(labels) > 0) and (len(colors) == 0):
                plt.plot(time_list[i], signal_list[i], label=labels[i])
                plt.legend()
            elif (len(labels) == 0) and (len(colors) > 0):
                plt.plot(time_list[i], signal_list[i], color=colors[i])
            else:
                plt.plot(time_list[i], signal_list[i])
        if grid:
            plt.grid(True)
        if title != "":
            plt.title(title)
        if xlabel != "":
            plt.xlabel(xlabel)
        if ylabel != "":
            plt.xlabel(ylabel)

        plt.xlim(xlim[0], xlim[1])
        plt.show()
    else:
        print('Invalid input format')
    
def plotOffset(time, corrected_force, filtered_force, ifei, efei, 
          offset_segment, offset_num_samples, signal_min_idx):
    middle_offset_idx = int((ifei + efei) / 2.0)
    offset_segment_time = time[middle_offset_idx - int(offset_num_samples/2): middle_offset_idx + int(offset_num_samples/2)]
    lower_lim = ifei - int((efei-ifei)*0.1)
    upper_lim = efei + int((efei-ifei)*0.1)
    plt.figure(figsize=[9, 5])
    plt.plot(time[lower_lim:upper_lim], filtered_force[lower_lim:upper_lim], 'blue', label='filtered force')
    plt.plot(time[lower_lim:upper_lim], corrected_force[lower_lim:upper_lim], 'gray', label='corrected force')
    plt.plot(offset_segment_time, offset_segment, 'black', label='offset segment')
    plt.plot(time[ifei], filtered_force[ifei], '^', label='init flight estimate', color='green')
    plt.plot(time[efei], filtered_force[efei], 'v', label='end flight estimate', color='red')
    plt.plot(time[signal_min_idx], filtered_force[signal_min_idx], 'o', label='signal minimum', color='orange')
    plt.plot(time[middle_offset_idx - int(offset_num_samples/2)], filtered_force[middle_offset_idx - offset_num_samples], '*k')
    plt.plot(time[middle_offset_idx + int(offset_num_samples/2)], filtered_force[middle_offset_idx + offset_num_samples], '*k')
    plt.axhline(filtered_force[0], color='gray', linestyle='--', label="first sample")
    plt.title('Offset correction')
    plt.xlabel('Time (s)')
    plt.ylabel('Force (N)')
    plt.legend()
    plt.grid()
    plt.show()
    
def plotFirstMovEst(time, corrected_force, force_diff, safe_movement_estimate, first_movement_estimate, flgCMJ,
                    signal_min_idx, first_peak_idx, first_valley_idx):
    fig, ax1 = plt.subplots(figsize=[9, 5])

    color = 'tab:blue'
    ax1.set_xlabel('Time (s)')
    ax1.set_ylabel('Force (N)', color=color)
    ax1.plot(time[:signal_min_idx], corrected_force[:signal_min_idx], color=color)
    ax1.plot(time[first_peak_idx], corrected_force[first_peak_idx], 'v', label='first peak', color='red')
    if flgCMJ:
        ax1.plot(time[first_valley_idx], corrected_force[first_valley_idx], '^', label='first valley', color='red')
    ax1.plot(time[first_movement_estimate], corrected_force[first_movement_estimate], 'x', 
             label='first movement estimate', color='green')
    ax1.plot(time[safe_movement_estimate], corrected_force[safe_movement_estimate], '>', 
             label='safe movement estimate', color='green')
    ax1.tick_params(axis='y', labelcolor=color)
    amp = max(max(corrected_force[:signal_min_idx])-corrected_force[0], corrected_force[0] - min(corrected_force[:signal_min_idx]))*1.1
    ax1.set_ylim([corrected_force[0]-amp, corrected_force[0]+amp])
    ax1.grid()
    ax1.legend()

    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

    color = 'tab:gray'
    ax2.set_ylabel(r'Force Diff ($\Delta$N)', color=color)  # we already handled the x-label with ax1
    ax2.plot(time[1:signal_min_idx+1], force_diff[:signal_min_idx], color=color)
    ax2.tick_params(axis='y', labelcolor=color)
    amp = max(abs(force_diff[:signal_min_idx]))*1.1
    ax2.set_ylim([-amp, amp])

    plt.title("First estimate of the movement initiation")
    plt.show()

def plotWeighingInterval(time, corrected_force, init_weighing_idx, end_weighing_idx, first_movement_estimate, signal_min_idx):
    plt.figure(figsize=[9, 5])
    plt.plot(time[:signal_min_idx], corrected_force[:signal_min_idx], label="force")
    plt.scatter(time[init_weighing_idx], corrected_force[init_weighing_idx],
                marker="^", color='green', label="init weighing")
    plt.scatter(time[end_weighing_idx], corrected_force[end_weighing_idx],
                marker="v", color='red', label="end weighing")
    plt.axvline(time[first_movement_estimate], 0, max(corrected_force[:signal_min_idx]),
                color='gray', linestyle='--', label="first movement estimate")
    plt.title("Weighing interval")
    plt.xlabel('Time (s)')
    plt.ylabel('Force (N)')
    plt.grid()
    plt.legend()
    plt.show()
    
def plotAdjustedMovement(time, corrected_force, init_movement, first_movement_estimate, 
                         safe_movement_estimate, signal_min_idx):
    plt.figure(figsize=[9, 5])
    plt.plot(time[:signal_min_idx], corrected_force[:signal_min_idx], label="force")
    plt.scatter(time[first_movement_estimate], corrected_force[first_movement_estimate],
                marker="x", color='green', label="first movement estimate")
    plt.scatter(time[safe_movement_estimate], corrected_force[safe_movement_estimate],
                marker="x", color='red', label="safe movement estimate")
    plt.scatter(time[init_movement], corrected_force[init_movement],
                marker=">", color='green', label="adjusted movement estimate")
    plt.title("Adjusting movement initiation")
    plt.xlabel('Time (s)')
    plt.ylabel('Force (N)')
    plt.grid()
    plt.legend()
    plt.show()

def plotAcelVelDisp(cropped_time, acel, vel, disp):
    fig, acel_axis = plt.subplots(figsize=[9, 5])
    
    vel_axis = acel_axis.twinx()
    disp_axis = acel_axis.twinx()

    acel_axis.set_xlabel("Time (s)")
    acel_axis.set_ylabel(r'Aceleration ($m/s^2$)')
    vel_axis.set_ylabel(r'Velocity ($m/s$)')
    disp_axis.set_ylabel(r'CM Displacement ($m$)')

    p1, = acel_axis.plot(cropped_time, acel, color='red', label="acel")
    p2, = vel_axis.plot(cropped_time, vel, color='blue', label="vel")
    p3, = disp_axis.plot(cropped_time, disp, color='green', label="disp")

    acel_ylim = acel_axis.get_ylim()
    acel_prop = np.abs(acel_ylim[1]/acel_ylim[0])
    vel_min = vel_axis.get_ylim()[0]
    vel_upper_lim = np.abs(vel_min * acel_prop)
    vel_axis.set_ylim([vel_min, vel_upper_lim])
    if np.abs(vel_axis.get_ylim()[0]) > vel_axis.get_ylim()[1]:
        vel_min = vel_axis.get_ylim()[0]
        vel_upper_lim = np.abs(vel_min * acel_prop)
        vel_axis.set_ylim([vel_min, vel_upper_lim])
    else:
        disp_max = disp_axis.get_ylim()[1]
        disp_lower_lim = -disp_max * acel_prop
        disp_axis.set_ylim([disp_lower_lim, disp_max])
    if np.abs(disp_axis.get_ylim()[0]) > disp_axis.get_ylim()[1]:
        disp_min = disp_axis.get_ylim()[0]
        disp_upper_lim = np.abs(disp_min * acel_prop)
        disp_axis.set_ylim([disp_min, disp_upper_lim])
    else:
        disp_max = disp_axis.get_ylim()[1]
        disp_lower_lim = -disp_max * acel_prop
        disp_axis.set_ylim([disp_lower_lim, disp_max])

    lns = [p1, p2, p3]
    acel_axis.legend(handles=lns, loc='best')

    disp_axis.spines['right'].set_position(('outward', 60))

    acel_axis.tick_params(axis='x')

    acel_axis.yaxis.label.set_color(p1.get_color())
    vel_axis.yaxis.label.set_color(p2.get_color())
    disp_axis.yaxis.label.set_color(p3.get_color())

    plt.grid(True)
    plt.title("Aceleration, Velocity and CM Displacement")
    fig.tight_layout()
    plt.show()
    
def plotCMJFirstPhases(cropped_time, acel, vel, disp, end_unweighting, end_braking, peak_vel_idx, acel_min_idx):
    fig, acel_axis = plt.subplots(figsize=[9, 5])

    vel_axis = acel_axis.twinx()
    disp_axis = acel_axis.twinx()

    acel_axis.set_xlabel("Time (s)")
    acel_axis.set_ylabel(r'Aceleration ($m/s^2$)')
    vel_axis.set_ylabel(r'Velocity ($m/s$)')
    disp_axis.set_ylabel(r'CM Displacement ($m$)')

    s1 = vel_axis.scatter(cropped_time[end_unweighting], vel[end_unweighting], 
                 label='end unweighting', color='blue', marker='o')
    s2 = disp_axis.scatter(cropped_time[end_braking], disp[end_braking], 
                 label='end braking', color='green', marker='o')
    a1 = acel_axis.axvspan(cropped_time[peak_vel_idx], cropped_time[acel_min_idx], alpha=0.3, 
                      color='gray', label='excluded region', hatch='//')
    a2 = acel_axis.axvspan(cropped_time[0], cropped_time[end_unweighting], alpha=0.3, 
                      color='blue', label='unweighting')
    a3 = acel_axis.axvspan(cropped_time[end_unweighting], cropped_time[end_braking], alpha=0.3, 
                      color='green', label='braking')

    p1, = acel_axis.plot(cropped_time[:acel_min_idx], acel[:acel_min_idx], color='red', label="acel")
    p2, = vel_axis.plot(cropped_time[:acel_min_idx], vel[:acel_min_idx], color='blue', label="vel")
    p3, = disp_axis.plot(cropped_time[:acel_min_idx], disp[:acel_min_idx], color='green', label="disp")
    
    acel_ylim = acel_axis.get_ylim()
    acel_prop = np.abs(acel_ylim[1]/acel_ylim[0])
    vel_min = vel_axis.get_ylim()[0]
    vel_upper_lim = np.abs(vel_min * acel_prop)
    vel_axis.set_ylim([vel_min, vel_upper_lim])
    if np.abs(vel_axis.get_ylim()[0]) > vel_axis.get_ylim()[1]:
        vel_min = vel_axis.get_ylim()[0]
        vel_upper_lim = np.abs(vel_min * acel_prop)
        vel_axis.set_ylim([vel_min, vel_upper_lim])
    else:
        disp_max = disp_axis.get_ylim()[1]
        disp_lower_lim = -disp_max * acel_prop
        disp_axis.set_ylim([disp_lower_lim, disp_max])
    if np.abs(disp_axis.get_ylim()[0]) > disp_axis.get_ylim()[1]:
        disp_min = disp_axis.get_ylim()[0]
        disp_upper_lim = np.abs(disp_min * acel_prop)
        disp_axis.set_ylim([disp_min, disp_upper_lim])
    else:
        disp_max = disp_axis.get_ylim()[1]
        disp_lower_lim = -disp_max * acel_prop
        disp_axis.set_ylim([disp_lower_lim, disp_max])

    lns = [p1, p2, p3, a1, a2, a3, s1, s2]
    acel_axis.legend(handles=lns, loc='best')

    disp_axis.spines['right'].set_position(('outward', 60))

    acel_axis.tick_params(axis='x')

    acel_axis.yaxis.label.set_color(p1.get_color())
    vel_axis.yaxis.label.set_color(p2.get_color())
    disp_axis.yaxis.label.set_color(p3.get_color())

    plt.grid(True)
    plt.title("Unweighting and Braking Phases CMJ")
    fig.tight_layout()
    plt.show()
    
def plotFlightPhase(cropped_time, acel, vel, disp, end_braking, end_propulsion, end_flight, 
                    center_flight_idx, aux1, aux2, max_acel_idx, samples_time, samples_segment,
                    aux_thres, flight_thres):
    fig, acel_axis = plt.subplots(figsize=[9, 5])

    vel_axis = acel_axis.twinx()
    disp_axis = acel_axis.twinx()

    acel_axis.set_xlabel("Time (s)")
    acel_axis.set_ylabel(r'Aceleration ($m/s^2$)')
    vel_axis.set_ylabel(r'Velocity ($m/s$)')
    disp_axis.set_ylabel(r'CM Displacement ($m$)')

    m1 = acel_axis.axvline(cropped_time[end_propulsion], max(acel), min(acel), 
                 label='end propulsion', color='green', linestyle='--')
    m2 = acel_axis.axvline(cropped_time[end_flight], max(acel), min(acel), 
                 label='end flight', color='red', linestyle='--')
    l1 = acel_axis.axhline(flight_thres, color='black', linestyle='--', label="flight threshold")
    l2 = acel_axis.axhline(aux_thres, color='gray', linestyle='--', label="aux threshold")
    s1 = acel_axis.scatter(cropped_time[aux1], acel[aux1], 
                      marker='^', color='green', label="aux1")
    s2 = acel_axis.scatter(cropped_time[aux2], acel[aux2], 
                      marker='v', color='red', label="aux2")
    s5 = acel_axis.scatter(cropped_time[center_flight_idx], acel[center_flight_idx], 
                      marker='o', color='black', label="flight center")
    a1 = acel_axis.axvspan(cropped_time[end_braking], cropped_time[end_propulsion], alpha=0.2, color='green', label='propulsion')
    len_arr = cropped_time[aux1]-cropped_time[end_braking]
    arr1 = acel_axis.arrow(cropped_time[end_braking], 0, len_arr, 0, length_includes_head=True,
                      width=2, head_width=5, head_length=len_arr*0.25, fc='green')
    a2 = acel_axis.axvspan(cropped_time[end_flight], cropped_time[max_acel_idx], alpha=0.2, color='red', label='landing')
    len_arr = cropped_time[max_acel_idx]-cropped_time[aux2]
    arr2 = acel_axis.arrow(cropped_time[max_acel_idx], 0, -len_arr, 0, length_includes_head=True,
                      width=2, head_width=5, head_length=len_arr*0.25, fc='red')
    a3 = acel_axis.axvspan(cropped_time[end_propulsion], cropped_time[end_flight], alpha=0.2, color='gray', label='flight')

    p1, = acel_axis.plot(cropped_time[end_braking:max_acel_idx], acel[end_braking:max_acel_idx], color='red', label="acel")
    p12, = acel_axis.plot(samples_time, samples_segment, color='black', label="samples segment")
    p2, = vel_axis.plot(cropped_time[end_braking:max_acel_idx], vel[end_braking:max_acel_idx], color='blue', label="vel")
    p3, = disp_axis.plot(cropped_time[end_braking:max_acel_idx], disp[end_braking:max_acel_idx], color='green', label="disp")

    acel_ylim = acel_axis.get_ylim()
    acel_prop = np.abs(acel_ylim[1]/acel_ylim[0])
    vel_min = vel_axis.get_ylim()[0]
    vel_upper_lim = np.abs(vel_min * acel_prop)
    vel_axis.set_ylim([vel_min, vel_upper_lim])
    if np.abs(vel_axis.get_ylim()[0]) > vel_axis.get_ylim()[1]:
        vel_min = vel_axis.get_ylim()[0]
        vel_upper_lim = np.abs(vel_min * acel_prop)
        vel_axis.set_ylim([vel_min, vel_upper_lim])
    else:
        disp_max = disp_axis.get_ylim()[1]
        disp_lower_lim = -disp_max * acel_prop
        disp_axis.set_ylim([disp_lower_lim, disp_max])
    if np.abs(disp_axis.get_ylim()[0]) > disp_axis.get_ylim()[1]:
        disp_min = disp_axis.get_ylim()[0]
        disp_upper_lim = np.abs(disp_min * acel_prop)
        disp_axis.set_ylim([disp_min, disp_upper_lim])
    else:
        disp_max = disp_axis.get_ylim()[1]
        disp_lower_lim = -disp_max * acel_prop
        disp_axis.set_ylim([disp_lower_lim, disp_max])

    lns = [p1, p2, p3, p12, s1, s2, s5, l1, l2, m1, m2, a1, a2, a3]
    acel_axis.legend(handles=lns, loc='best')

    disp_axis.spines['right'].set_position(('outward', 60))

    acel_axis.tick_params(axis='x')

    acel_axis.yaxis.label.set_color(p1.get_color())
    vel_axis.yaxis.label.set_color(p2.get_color())
    disp_axis.yaxis.label.set_color(p3.get_color())

    plt.grid(True)
    plt.title("Directions to Search for the Flight Phase")
    fig.tight_layout()
    plt.show()

def plotLandingPhase(cropped_time, acel, vel, disp, end_propulsion, end_flight, end_landing, max_acel_idx):
    fig, acel_axis = plt.subplots(figsize=[9, 5])

    vel_axis = acel_axis.twinx()
    disp_axis = acel_axis.twinx()

    acel_axis.set_xlabel("Time (s)")
    acel_axis.set_ylabel(r'Aceleration ($m/s^2$)')
    vel_axis.set_ylabel(r'Velocity ($m/s$)')
    disp_axis.set_ylabel(r'CM Displacement ($m$)')

    s1 = acel_axis.scatter(cropped_time[end_landing], acel[end_landing], 
                      marker='o', color='red', label="end landing")
    s2 = acel_axis.scatter(cropped_time[max_acel_idx], acel[max_acel_idx], 
                      marker='>', color='orange', label="max acel")
    a1 = acel_axis.axvspan(cropped_time[end_propulsion], cropped_time[end_flight], alpha=0.2, color='gray', label='flight')
    a2 = acel_axis.axvspan(cropped_time[end_flight], cropped_time[end_landing], alpha=0.2, color='blue', label='landing')

    p1, = acel_axis.plot(cropped_time[end_propulsion:], acel[end_propulsion:], color='red', label="acel")
    p2, = vel_axis.plot(cropped_time[end_propulsion:], vel[end_propulsion:], color='blue', label="vel")
    p3, = disp_axis.plot(cropped_time[end_propulsion:], disp[end_propulsion:], color='green', label="disp")

    acel_ylim = acel_axis.get_ylim()
    acel_prop = np.abs(acel_ylim[1]/acel_ylim[0])
    vel_min = vel_axis.get_ylim()[0]
    vel_upper_lim = np.abs(vel_min * acel_prop)
    vel_axis.set_ylim([vel_min, vel_upper_lim])
    if np.abs(vel_axis.get_ylim()[0]) > vel_axis.get_ylim()[1]:
        vel_min = vel_axis.get_ylim()[0]
        vel_upper_lim = np.abs(vel_min * acel_prop)
        vel_axis.set_ylim([vel_min, vel_upper_lim])
    else:
        disp_max = disp_axis.get_ylim()[1]
        disp_lower_lim = -disp_max * acel_prop
        disp_axis.set_ylim([disp_lower_lim, disp_max])
    if np.abs(disp_axis.get_ylim()[0]) > disp_axis.get_ylim()[1]:
        disp_min = disp_axis.get_ylim()[0]
        disp_upper_lim = np.abs(disp_min * acel_prop)
        disp_axis.set_ylim([disp_min, disp_upper_lim])
    else:
        disp_max = disp_axis.get_ylim()[1]
        disp_lower_lim = -disp_max * acel_prop
        disp_axis.set_ylim([disp_lower_lim, disp_max])

    lns = [p1, p2, p3, s1, s2, a1, a2]
    acel_axis.legend(handles=lns, loc='best')

    disp_axis.spines['right'].set_position(('outward', 60))

    acel_axis.tick_params(axis='x')

    acel_axis.yaxis.label.set_color(p1.get_color())
    vel_axis.yaxis.label.set_color(p2.get_color())
    disp_axis.yaxis.label.set_color(p3.get_color())

    vel_axis.grid(True)
    plt.title("Landing Phase")
    fig.tight_layout()
    plt.show()
    
def plotAllPhases(time, corrected_force, cropped_time, acel, vel, disp, init_movement, init_weighing_idx,
                  end_weighing_idx, end_unweighting, end_braking, end_propulsion, end_flight, end_landing, flgCMJ):
    fig, force_axis = plt.subplots(figsize=[9, 5])

    vel_axis = force_axis.twinx()
    disp_axis = force_axis.twinx()
    acel_axis = force_axis.twinx()

    force_axis.set_xlabel("Time (s)")
    acel_axis.set_ylabel(r'Aceleration ($m/s^2$)')
    vel_axis.set_ylabel(r'Velocity ($m/s$)')
    disp_axis.set_ylabel(r'CM Displacement ($m$)')
    force_axis.set_ylabel(r'Force (N)')

    a0 = force_axis.axvspan(time[init_weighing_idx], time[end_weighing_idx], alpha=0.4, color='black', label='weighing')
    if flgCMJ:
        a1 = force_axis.axvspan(cropped_time[0], cropped_time[end_unweighting], alpha=0.5, color='#6d9197', label='unweighting')
        a2 = force_axis.axvspan(cropped_time[end_unweighting], cropped_time[end_braking], alpha=0.9, color='#d8e2dc', label='braking')
    a3 = force_axis.axvspan(cropped_time[end_braking], cropped_time[end_propulsion], alpha=0.9, color='#ffe5d9', label='propulsion')
    a4 = force_axis.axvspan(cropped_time[end_propulsion], cropped_time[end_flight], alpha=0.9, color='#ffcad4', label='flight')
    a5 = force_axis.axvspan(cropped_time[end_flight], cropped_time[end_landing], alpha=0.5, color='#9d8189', label='landing')

    p1, = force_axis.plot(time[:end_landing+init_movement], corrected_force[:end_landing+init_movement], color='black', label="force")
    p0, = acel_axis.plot(cropped_time[:end_landing], acel[:end_landing], color='red', label="acel")
    p2, = vel_axis.plot(cropped_time[:end_landing], vel[:end_landing], color='blue', label="vel")
    p3, = disp_axis.plot(cropped_time[:end_landing], disp[:end_landing], color='green', label="disp")

    acel_ylim = acel_axis.get_ylim()
    acel_prop = np.abs(acel_ylim[1]/acel_ylim[0])
    vel_min = vel_axis.get_ylim()[0]
    vel_upper_lim = np.abs(vel_min * acel_prop)
    vel_axis.set_ylim([vel_min, vel_upper_lim])
    if np.abs(vel_axis.get_ylim()[0]) > vel_axis.get_ylim()[1]:
        vel_min = vel_axis.get_ylim()[0]
        vel_upper_lim = np.abs(vel_min * acel_prop)
        vel_axis.set_ylim([vel_min, vel_upper_lim])
    else:
        disp_max = disp_axis.get_ylim()[1]
        disp_lower_lim = -disp_max * acel_prop
        disp_axis.set_ylim([disp_lower_lim, disp_max])
    if np.abs(disp_axis.get_ylim()[0]) > disp_axis.get_ylim()[1]:
        disp_min = disp_axis.get_ylim()[0]
        disp_upper_lim = np.abs(disp_min * acel_prop)
        disp_axis.set_ylim([disp_min, disp_upper_lim])
    else:
        disp_max = disp_axis.get_ylim()[1]
        disp_lower_lim = -disp_max * acel_prop
        disp_axis.set_ylim([disp_lower_lim, disp_max])
    
    if flgCMJ:
        lns = [p0, p1, p2, p3, a0, a1, a2, a3, a4, a5]
    else:
        lns = [p0, p1, p2, p3, a0, a3, a4, a5]
    force_axis.legend(handles=lns, loc='best')

    vel_axis.spines['right'].set_position(('outward', 50))
    disp_axis.spines['right'].set_position(('outward', 100))

    force_axis.tick_params(axis='x')

    force_axis.yaxis.label.set_color(p1.get_color())
    vel_axis.yaxis.label.set_color(p2.get_color())
    disp_axis.yaxis.label.set_color(p3.get_color())
    acel_axis.yaxis.label.set_color(p0.get_color())

    vel_axis.grid(True)
    if flgCMJ:
        plt.title("All Phases CMJ")
    else:
        plt.title("All Phases SJ")
    fig.tight_layout()
    
    plt.show()