import pandas as pd
import json



df = pd.read_json('teste.json', lines=True)

df = df.drop(df[df['time_stamp'] < 0.1].index)

df = df.reset_index(drop=True)

print(df.to_string())

#---------------------------------------------------------


#file = open(stateFile, 'r')
nomeOut = 'teste.sto'
#fileOut = open(nomeOut, 'w')

# linhaHeader = 0
# for linha in file:
#     if linha.find("endheader") >= 0:
#         break
#     else:
#         linhaHeader = linhaHeader + 1
#         fileOut.write(linha)

# fileOut.write("endheader\n")
# fileOut.close()
# file.close()

#dados = pd.read_table(stateFile, header=linhaHeader + 1)

#dadosOut = dados

colunas = ['time',
            'quaternions_thigh',
            'quaternions_ankle']

# Remover colunas que não estão na lista
# for col in df.columns:
#     if not(col in colunas):
#         del dadosOut[col]

# Deixando os valores simetricos lateralmente
# dadosOut['/jointset/hip_l/hip_flexion_l/value'] = dadosOut['/jointset/hip_r/hip_flexion_r/value']
# dadosOut['/jointset/knee_l/knee_angle_l/value'] = dadosOut['/jointset/knee_r/knee_angle_r/value']
# dadosOut['/jointset/ankle_l/ankle_angle_l/value'] = dadosOut['/jointset/ankle_r/ankle_angle_r/value']

#dadosOut['/jointset/back/lumbar_extension/value'] = np.zeros(len(dadosOut['time']))

df.to_csv(nomeOut, header=True, index=None, sep='\t', mode='a')

