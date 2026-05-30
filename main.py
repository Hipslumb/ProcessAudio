from viterbi import use_viterbi
from parametrs import percent

path = input("Введите имя .wav файла для расшифровки из папки WAV")
decoded_path = f"WAV/{path}.wav"
# проверь ток существование файла как у меня ниже!!!!!!!!!

# исходные чистые текста надо с тем же названием что и WAV сохранить оке доке??????
clean_path = f"text/{path}.txt"
clean = ""
try: 
    with open(clean_path, 'r', encoding='utf-8') as file:
        clean = file.read()
except FileNotFoundError:
    print("Файл {clean_path} не существует!")

# decoded = тут получи крч string текст из записи.
# перед этим все свои записи загрузи в папку WAV в .wav формате конечно

path = input("Введите имя файла для сохранения декодированного текста в папку TXT")
after_path = f"TXT/{path}.txt"

before_p = percent(clean, decoded)
text = use_viterbi(clean,decoded)
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