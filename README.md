# ema_motion_analysis

Este repositório tem como objetivo a implementação de uma demonstração
da detecção automática do movimento humano por meio de redes neurais e sensores inerciais
(IMU's). Este foi desenvolvido com o intuito de analisar o salto vertical, no entanto
pode ser adaptado para outros movimentos. 

<!-- Funciona no github -->
Exemplo do funcionamento da detecção de pose. 
<p align="center">
  <img src="/examples/blazepose-example.gif" alt="Exemplo de detecção de pose com o blazepose." />
</p>

<!-- Funciona no github -->
Exemplo do funcionamento do uso de 2 IMU's calculando o menor ângulo entre elas. 
<p align="center">
  <img src="/examples/imu-example.gif" alt="Exemplo de visualização 3d com angulos em tempo real entre IMU's." />
</p>

## Pré-requisitos

- Ambiente de desenvolvimento Anaconda
- Python 3

## Instalação do pacotes Pacotes

Primeiramente, crie um ambiente de desenvolvimento:
```
conda create --no-default-packages -n ema_motion_env python=3.9.1
```
Ative o ambiente de desenvolvimento com:
```
conda activate ema_motion_env
```
Instale os seguintes pacotes com o comando conda (Windows, Linux e MacOS):
```
conda install -c anaconda numpy=1.21.2
pip install matplotlib==3.5.1
pip install mediapipe==0.8.9.1
pip install PyQt5==5.12.3
pip install pyserial==3.5
pip install pyqtgraph==0.12.4
pip install pyquaternion==0.9.9
pip install scipy==1.7.3
```

Exclusivo Linux e MacOs
```
conda install -c conda-forge tensorflow=2.7.0
pip install opencv-python==4.5.2.54
```

Exclusivo Windows
```
conda install -c conda-forge tensorflow=2.6.0
pip install opencv-python==4.5.1.48
```
## Execução dos programas de deteção de pose

Navegue para a pasta pose_detection e depois scripts:
```
cd pose_detection
cd scripts
```

Execute a detecção de pose com alguma das redes:

```
python blazepose.py
```
ou

```
python movenet.py
```

Então será aberto um menu do usuário em que este pode escolher entre executar alguns dos exemplos prontos disponíveis ou carregar um exemplo próprio.

Nas pasta "outputs" serão salvos os arquivos com os dados do processamento (localização dos pontos para cada frame) e os vídeos com as identificações das poses.

## Execução dos programas de IMU

Navegue para a pasta imu e em seguida para a pasta scripts:
```
cd imu
cd scripts
```

Para uma visualização 3D da IMU, execute:
```
python 3d_visualization.py
```

Para visualização dos gráficos de ângulos de Euler execute:
```
python 2imus_3d_visualization.py
```

Para a execução dos programas da IMU certifique-se de que o dongle está conectado a seu 
computador e que a IMU a ser utilizada está ligada e com bateria, além disso é necessário
configurar o endereço das IMU's na memória do dongle com o auxílio da suite do fabricante
[Ver página 10 do manual disponível na pasta manual deste repositório].

Para melhor entendimento do código das IMU's é necessária a leitura do manual do
dispositivo disponível na pasta manual deste repositório, sendo tópicos mais importantes
o modo como são enviados os comandos (neste repositório usa-se ASCII por simplicidade), 
o formato em que são recebidas as respostas, o modo streaming e o significado de cada
comando. Apesar de ser fortemente recomendada a leitura do manual, as funções implementadas
no modulo serial_operations foram implementadas de modo que seja possível realizar a 
obtenção de dados simplesmente configurando a IMU para o modo streaming como é feito
nos dos arquivos exemplos com o dicionário imu_configuration e em seguida com a leitura dos
dados e extração dos mesmos de acordo com o formato previamente configurado. No quesito extração
de dados foram feitas as configurações para extração de quaternions, angulos de euler e 
matrizes de rotação de forma isolada, para extração destes em uma mesma configuração de streaming 
é necessária a implementação de novas funções.

OBS: para a visualização em 3d ser fidedigna (sem espelhamentos ou inversões de eixos) é necessário
realizar a tara das imu's em pés como apresentado na figura abaixo com relação à tela em que a 
representação é visualizada.
<p align="center">
  <img src="/examples/tara-imu.jpeg" alt="Modo correto de tarar a IMU em relação ao PC." />
</p>

## Styleguide

Os códigos desta demonstração foram escritos com base no style guide disponível 
em: https://peps.python.org/pep-0008/#introduction.