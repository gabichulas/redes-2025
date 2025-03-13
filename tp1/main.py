from functions import *
import pandas as pd

path = r"path/to/log" # Cambiar por ruta a Tramas_802-15-4.log

def main():
    results = []
    with open(path, 'r') as file:
        text = file.read()
    
    tramas = split_tramas(text)
    
    for trama in tramas:
        longitud_correcta = calc_length(trama)
        checksum_correcto = calc_checksum(trama)
        sec_escape = True if "7D7E" in trama else False
        results.append({
            "trama": trama,
            "longitud_correcta": longitud_correcta,
            "checksum_correcto": checksum_correcto,
            "sec_escape": sec_escape
        })
    
    df = pd.DataFrame(data=results, columns=["trama", "longitud_correcta", "checksum_correcto", "sec_escape"])
    
    print(f"Tramas totales: {len(results)}")
    print(f"Tramas con longitud correcta: {df["longitud_correcta"].sum()}")
    print(f"Tramas con longitud incorrecta: {len(results) - df["longitud_correcta"].sum()}")
    print(f"Tramas con longitud correcta y checksum correcto: {len(df[(df["longitud_correcta"] == True) & (df["checksum_correcto"] == True)])}")
    print(f"Tramas con longitud correcta y checksum incorrecto: {len(df[(df["longitud_correcta"] == True) & (df["checksum_correcto"] == False)])}")
    print(f"Secuencias de escape: {df["sec_escape"].sum()}")
    
    print("\nLíneas con secuencias de escape:")
    for i, trama in enumerate(tramas):
        if "7D7E" in trama:
            cleaned_trama = trama.replace("7D7E", "7E")
            print(f"Línea {i}: {cleaned_trama}")

    print("\nLíneas con longitud o checksum incorrecto:")
    for i, trama in enumerate(tramas):
        if not df.loc[i, 'longitud_correcta'] or not df.loc[i, 'checksum_correcto']:
            print(f"Línea {i}: {trama}")

main()