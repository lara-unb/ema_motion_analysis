"""User interface functions and dicts.

"""

import colors
import fileManagement

# Add new examples by selecter an interger key, a profile and it's path
VIDEOS = {
    1: ("right","right-rafilsk1", ".mp4"),
    2: ("frontal", "frontal-girl", ".mp4"),
    3: ("frontal", "frontal-rafa", ".mp4"),
    4: ("left", "left-rafa", ".mp4"),
}


# Available poses
PROFILES = {
    1: "frontal",
    2: "right",
    3: "left",
}

def initialMenu(neural_network):
    """Displays inicial menu

    Used to get the information from the user about the video to 
    be used in the pose prediction
    
    Args:
        neural_network: neural network that will be used to make the pose 
            prediction ('movenet' or 'blazepose')

    Return:
        video_name: a string with the name of the video to be used in the predicton
        video_path: a string with the path to the video to be used in the prediction
        video_out_path: a string with the path to the output prediction video
        file_out_path: a string with the path to the output prediction file
        profile: a string informing the profile os the person in the video
            ('frontal', 'right', 'left')
    """

    print(colors.BLUE, "\nMOTION ANALYSIS DEMO!\n", colors.RESET)
    print("\nVocê deseja:")
    print("1 - Select video from computer")
    print("2 - Select video from examples")

    while True:
        escolha = int(input())
        # Select video from computer
        if escolha == 1:
            print("\nSelect the video profile:")
            print("1 - Frontal")
            print("2 - Sagittal Right")
            print("3 - Sagittal Left")

            while True:
                try:
                    profile = PROFILES[int(input())]
                    break
                except:
                    print(colors.RED, "Valor inválido!", colors.RESET)

            video_name, video_path, video_out_path, file_out_path = fileManagement.readFileDialog(neural_network, 
                                                                                                  "Open video file")
            break
        # Select video from examples
        elif escolha == 2:
            for key in VIDEOS.keys():
                print("{} - {}".format(key, VIDEOS[key][1]))
            while True:
                try:
                    selectedVideo = int(input())
                    profile = VIDEOS[selectedVideo][0] 
                    break
                except :
                    print(colors.RED, "Valor inválido!", colors.RESET)
            
            video_path, video_out_path, file_out_path = fileManagement.getOutputsPaths(VIDEOS[selectedVideo][1],
                                                                                       VIDEOS[selectedVideo][2], 
                                                                                       neural_network)
            video_name = VIDEOS[selectedVideo][1]
            break

        # Invalid entrance
        else:
            print(colors.RED, "Valor inválido!", colors.RESET)
            continue

    return video_name, video_path, video_out_path, file_out_path, profile



