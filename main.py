from viterbi import use_viterbi
from parametrs import percent
from simple_model import predict_segment

path = input("Введите имя .wav файла для расшифровки из папки WAV: ")
decoded_path = f"WAV/{path}.wav"

clean_path = f"ORIG/{path}.txt"
clean = ""
try: 
    with open(clean_path, 'r', encoding='utf-8') as file:
        clean = file.read()
except FileNotFoundError:
    print("Файл {clean_path} не существует!")

decoded = predict_segment(decoded_path)
decoded_audio_path = f"audio/decoded_{path}.txt"

with open(decoded_audio_path, 'w', encoding='utf-8') as file:
    file.write(decoded)

after_path = f"TXT/{path}.txt"

before_p = percent(clean, decoded)
text = use_viterbi(clean, decoded)
after_p = percent(clean, text)

if after_p < before_p:
        print(f"Витерби ухудшил: было {before_p:.3f}%, стало {after_p:.3f}% — откатываемся.")
        text = decoded
        final_p = before_p
else:
    print(f"Витерби улучшил/не ухудшил: было {before_p:.3f}%, стало {after_p:.3f}%.")
    final_p = after_p

    with open(after_path, 'w', encoding='utf-8') as file:
        file.write(text)

    print(f"Итоговая точность: {final_p:.3f}%")