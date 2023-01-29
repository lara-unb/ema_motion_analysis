# Simplest IMU YostLabs Data Acquisition

A ideia deste branch é isolar as funcionalidades de obtenção de dados das IMU's para uma simples coleta.

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
pip install PyQt5==5.12.3
pip install pyserial==3.5
pip install pyqtgraph==0.12.4
pip install pyquaternion==0.9.9
pip install scipy==1.7.3
```

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