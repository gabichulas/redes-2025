import re

path = r"path/to/log" # Cambiar por ruta a Tramas_802-15-4.log

with open(path, 'r') as file:
    text = file.read()

def split_tramas(text):
    tramas = re.split(r'(?<!7D)7E', text)
    tramas = ['7E' + trama for trama in tramas[1:]]
    tramas[-1] = tramas[-1].replace('\n', '')
    return tramas

def calc_checksum(trama):
    suma = 0
    res = 0
    trama_m = trama[6:-2]
    if "7D7E" in trama_m:
        trama_m = trama_m.replace("7D7E", "7E")
    for i in range(0,len(trama_m),2):
        suma += int(trama_m[i] + trama_m[i + 1], 16)
    res = int("FF", 16) - (suma % 256)
    res = format(res, "02x").upper()
    return res == str(trama[-2:])

def calc_length(trama):
    length = int(trama[2:6], 16)
    trama = trama[6:-2]
    if "7D7E" in trama:
        trama = trama.replace("7D7E", "7E")
    return len(trama)/2 == length