import re
TEXT_PATH = 'text/english.txt'
CLEAN_PATH = 'text/cleaned_text.txt'
ENCODED_PATH = 'text/encoded.txt'
# всякие вспомогашки хз

def percent(orig, decoded):
    n = min(len(orig), len(decoded))
    if n == 0:
        return 0.0
    
    match = 0
    for o, d in zip(orig[:n], decoded[:n]):
        if o == d:
            match += 1
    pers = match * 100.0 / n
    print(f"Восстановление текста: {pers} %")
    return pers

def clean_text(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
    
    text = text.lower()
    text = re.sub(r'[^a-z\s]', '', text)
    
    text = re.sub(r'\s+', ' ', text)
    
    return text

if __name__ == '__main__':
    clean_text = clean_text(TEXT_PATH)
    with open(CLEAN_PATH, 'w', encoding='utf-8') as file:
        file.write(clean_text)
    
def caesar_cipher(text, shift):
    result = ""
    for sim in text:
        if sim.isalpha():
            new_sim = chr((ord(sim) - ord('a') + shift) % 26 + ord('a') )
            result += new_sim
        else:
            result += sim
    return result

shift = 13
if __name__ == '__main__':
    encoded = caesar_cipher(clean_text,shift)
    with open(ENCODED_PATH, 'w', encoding='utf-8') as file:
        file.write(encoded)
#decoded = caesar_cipher(encoded,-shift)