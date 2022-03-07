# ema_motion_analysis

Demonstração de análise automática do movimento humano.

<!-- COLOCAR AQUI GIF DE UMA DETECÇÃO DE POSE -->

<!-- COLOCAR AQUI GRÁFICO DE UMA DETECÇÃO DE MOVIMENTO -->

## Pré-requisitos

- Ambiente de desenvolvimento Anaconda
- Python 3


## Instalação do pacotes Pacotes

Primeiramente, crie um ambiente de desenvolvimento:

- conda create --no-default-packages -n ema_motion_env python=3.9.1

Ative o ambiente de desenvolvimento com:

- conda activate ema_motion_env

Instale os seguintes pacotes com o comando conda (Windows e Linux):

- conda install -c anaconda numpy=1.21.2
- pip install matplotlib==3.5.1

- pip install mediapipe==0.8.9.1
- pip install PyQt5==5.12.3

Exclusivo Linux
- conda install -c conda-forge tensorflow=2.7.0
- pip install opencv-python==4.5.2.54
Exclusivo Windows
- conda install -c conda-forge tensorflow=2.7.0
- pip install opencv-python==4.5.1.48

## Execução dos programas

Navegue para a pasta de scrpits:
- cd scripts

Execute a detecção de pose com alguma das redes:

- python blazepose.py

ou

- python movenet.py

Então será aberto um menu do usuário em que este pode escolher entre executar alguns dos exemplos prontos disponíveis ou carregar um exemplo próprio:

- Nas pasta "outputs" serão salvos os arquivos com os dados do processamento (localização dos pontos para cada frame) e os vídeos com as identificações das poses.

