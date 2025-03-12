import re

path = r"tp1\Tramas_802-15-4.log"

with open(path, 'r') as file:
    text = file.read()

def split_tramas(text):
    tramas = re.split(r'(?<!7D)7E', text)
    tramas = ['7E' + trama for trama in tramas[1:]]
    tramas[-1] = tramas[-1].replace('\n', '')
    return tramas