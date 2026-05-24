from symspellpy import SymSpell, Verbosity
from freq import DECODED_PATH

AI_PATH = 'text/ai_decoded.txt'

with open(DECODED_PATH, 'r', encoding='utf-8') as file:
    decoded = file.read()

sym_spell = SymSpell(max_dictionary_edit_distance=2)
sym_spell.load_dictionary('frequency_dictionary_en_82_765.txt', 0, 1)

words = decoded.split()
result = []

for word in words:
    sug = sym_spell.lookup(word, Verbosity.CLOSEST, max_edit_distance=2)
    if sug:
        result.append(sug[0].term)
    else:
        result.append(word)

corrected_text = ' '.join(result)

with open(AI_PATH, 'w', encoding='utf-8') as file:
    file.write(corrected_text)