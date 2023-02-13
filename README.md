# Simplest IMU YostLabs Data Acquisition TESTEE

A ideia deste branch é isolar as funcionalidades de obtenção de dados das IMU's para uma simples coleta.

## Pré-requisitos

- Instalar e conhecer minimamente Python 3
- (Recomendado) Ler manual da IMU Yost Labs e manual da suíte.

## Instalação do pacotes


Instale os seguintes pacotes com o comandos com pip no windows, para o linux os mesmos comandos podem ser executados sem a flag --user:
```
pip install matplotlib==3.5.1 --user 
pip install pyserial==3.5 --user
pip install numpy=1.21.2 --user
pip install pyquaternion==0.9.9 --user
pip install scipy==1.7.3 --user
```

## Organização das pastas e programas de interesse
- /data_visualization -> Contém definição de constantes para imprimir colorido no terminal.
- /imu
  - /scripts
    - get_1imu_data.py para obter dados com a imu que deve ser executado.
    - /data -> dados coletados no script de aquisição
  - /utils
    - file_management.py -> funções para escrita em  arquivo.
    - quaternion_operations.py -> funções para manipulação de dados com quaternions
    - serial_operations.py -> Funções para interação com interface serial do dongle da imu da Yost Labs

OBS: Antes de executar o programa, passe por todo o código e entenda seu funcionamento, assim será possível realizar ajustes simples caso haja problemas na execução.

## Execução dos programas de IMU

Navegue para a pasta imu e em seguida para a pasta scripts:
```
cd imu
cd scripts
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
dados e extração dos mesmos de acordo com o formato previamente configurado. No quesito extração de dados foram feitas as configurações para extração de quaternions, angulos de euler e matrizes de rotação de forma isolada, para extração destes em uma mesma configuração de streaming é necessária a implementação de novas funções.

Para para iniciar a coleta com a IMU, execute:
```
python get_1imu_data.py (Windows)
python3 get_1imu_data.py (Linux)
```
OBS: Ao exeutar o programa, por alguns segundos deixa a IMU parada por alguns segundos até que no console do PC seja impresso "Movement is beeing captured.". Então, o programa vai executar infinitamente até que seja pressionado "ctrl+c". Então a IMU mostra os gráficos e os salva dentro da pasta /data. 

OBS: ao executar o programa em linux pode ser necessário executar o comando que permite todos poderem escrever na porta /dev/ttyACM0 que está conectada o usb:
```
sudo chmod 666 /dev/ttyACM0 
```
OBS2: se o dongle não está conectado na porta acima, liste as portas e identifique-as com o comando:
```
dmesg | grep tty
```



