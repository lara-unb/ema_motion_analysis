import colors
import fileManagement

VIDEOS = {
    1: ("right","\\examples\\right-rafilsk1.mp4"),
    2: ("frontal", "\\examples\\frontal-girl.mp4")
}
PROFILES = {
    1: "frontal",
    2: "right",
    3: "left"
}

def initialMenu():
    print(colors.BLUE, "Motion analysis demo!", colors.RESET)
    print("Você deseja:")
    print("1 - Selecionar um vídeo do seu computador.")
    print("2 - Selecionar um dos nossos exemplos.")
    while(True):
        escolha = int(input())
        if(escolha == 1):
            print("O vídeo tem perfil:")
            print("1 - Frontal")
            print("2 - Lateral Direito")
            print("3 - Lateral Esquerdo")
            while(True):
                try:
                    profile = PROFILES[int(input())] # Não sei se desrespeitei o inglês aqui !!!!
                    break
                except:
                    print("Valor inválido!")
            video_path, video_out_path = fileManagement.readFileDialog("Open video file")
            print(video_path)
            break
        else:
            for key in VIDEOS.keys():
                print("{} - {}".format(key, VIDEOS[key][1]))
            while(True):
                try:
                    videoSelected = int(input())
                    profile = VIDEOS[videoSelected][0] # Não sei se desrespeitei o inglês aqui !!!!
                    break
                except :
                    print("Valor inválido!")
            
            video_path = fileManagement.getAbsolutePath() + VIDEOS[videoSelected][1]
            video_out_path = video_path + "mnl.avi"
            break
    return video_path, video_out_path, profile
