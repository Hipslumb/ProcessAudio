import numpy as np
import soundfile as sf
import os

def text_to_wav(text, wav_folder, output_file, silence_ms=0):
    sr = None
    segments = []
    
    for char in text.lower():
        if char == ' ':
            filename = f'{wav_folder}/space_1.wav'
        elif char.isalpha():
            filename = f'{wav_folder}/{char}_5.wav'
        else:
            continue  
        
        try:
            signal, file_sr = sf.read(filename)
            if sr is None:
                sr = file_sr
            segments.append(signal)
        except Exception:
            print(f'Файл не найден: {filename}')
            continue
    
    if segments:
        merged = np.concatenate(segments)
        sf.write(output_file, merged, sr)
        print(f'Сохранено: {output_file}, длина: {len(merged)/sr:.1f} сек')

# Использование
text = input('Введи текст: ')
text_to_wav(text, 'sounds', 'output.wav', silence_ms=0)