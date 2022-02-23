
import colors
import fileManagement

#-------------------------------------------------------------------------------------
# Add new examples by selecter an interger key, a profile and it's path
VIDEOS = {
    1: ("right","/../examples/right-rafilsk1", ".mp4"),
    2: ("frontal", "/../examples/frontal-girl", ".mp4"),
    3: ("frontal", "/../examples/frontal-rafa", ".mp4"),
    4: ("left", "/../examples/left-rafa", ".mp4"),
}

#-------------------------------------------------------------------------------------
# Available poses
PROFILES = {
    1: "frontal",
    2: "right",
    3: "left"
}

#-------------------------------------------------------------------------------------
# Function to show inicial menu
def initialMenu():
    print(colors.BLUE, "\nMOTION ANALYSIS DEMO!\n", colors.RESET)
    print("\nVocê deseja:")
    print("1 - Select video from computer")
    print("2 - Select video from examples")
    while(True):
        escolha = int(input())
        # Select video from computer
        if escolha == 1:
            print("\nSelect the video profile:")
            print("1 - Frontal")
            print("2 - Sagittal Right")
            print("3 - Sagittal Left")
            while(True):
                try:
                    profile = PROFILES[int(input())]
                    break
                except:
                    print(colors.RED, "Valor inválido!", colors.RESET)
            video_path, video_out_path = fileManagement.readFileDialog("Open video file")
            break
        # Select video from examples
        elif escolha == 2:
            for key in VIDEOS.keys():
                print("{} - {}".format(key, VIDEOS[key][1]))
            while(True):
                try:
                    selectedVideo = int(input())
                    profile = VIDEOS[selectedVideo][0] 
                    break
                except :
                    print(colors.RED, "Valor inválido!", colors.RESET)
            
            video_path = fileManagement.getAbsolutePath() + VIDEOS[selectedVideo][1] + VIDEOS[selectedVideo][2]
            video_out_path = fileManagement.getAbsolutePath() + VIDEOS[selectedVideo][1] + "mnl.avi"
            file_out_path = fileManagement.getAbsolutePath() + VIDEOS[selectedVideo][1] + "-json.data"
            break

        # Invalid entrance
        else:
            print(colors.RED, "Valor inválido!", colors.RESET)
            continue
    return video_path, video_out_path, file_out_path, profile

#-------------------------------------------------------------------------------------

