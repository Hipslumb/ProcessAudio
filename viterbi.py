import numpy as np
from hmmlearn import hmm
from freq import letters_reliability, load_order, DECODED_PATH, ORDER_PATH
AFTER_PATH = 'text/after_viterbi.txt'

def get_weights(arr):
    weights = {}
    for rank, smf in enumerate(arr):
        weights[smf] = len(arr) - rank + 1
    return weights

FREQUENCY = ['e','t','a','o','i','n','s','h','r','d','l','c','u','m','w','f','g','y','p','b','v','k','j','x','q','z',' ']

BIGRAMS = [
    'th', 'he', 'in', 'er', 'an', 're', 'nd', 'at', 'on', 'nt',
    'ha', 'es', 'st', 'en', 'ed', 'to', 'it', 'ou', 'ea', 'hi',
    'is', 'or', 'ti', 'as', 'te', 'et', 'ng', 'of', 'al', 'de',
    ' t', ' a', ' i', ' w', ' s', 'e ', 't ', 's ', 'd ', 'n ', 'y ', 'r ', 'f ', 'm '
]

def transition_matrix(bg_w):
    alphabet = 'abcdefghijklmnopqrstuvwxyz '
    n = len(alphabet)
    
    A = np.ones((n, n)) * 0.0001 # переход от буквы к букве
    for i, ch1 in enumerate(alphabet):
        for j, ch2 in enumerate(alphabet):
            bg = ch1 + ch2
            if bg in bg_w:
                A[i, j] = bg_w[bg] 
    A[26,26] = 0
        
    for i in range(n):
        row_sum = A[i].sum()
        if row_sum > 0:
            A[i] /= row_sum

    return A

def start_probs(letter_w):
    alphabet = 'abcdefghijklmnopqrstuvwxyz '
    pi = np.array([letter_w.get(ch, 1) for ch in alphabet])
    pi = pi / pi.sum()
    return pi

def use_viterbi(text,order):
    letter_w = get_weights(FREQUENCY)
    bg_w = get_weights(BIGRAMS)
    
    model = hmm.CategoricalHMM(n_components=27, init_params='')
    A = transition_matrix(bg_w)
    pi = start_probs(letter_w)
    model.startprob_ = pi
    model.transmat_ = A
    
    alphabet = 'abcdefghijklmnopqrstuvwxyz '
    n_states = len(alphabet)
    n_symbols = n_states
    # same_p = 0.97
    # other_p = (1.0 - same_p) / (n_symbols - 1)
        # emission = np.full((n_states, n_symbols), other_p)
    # np.fill_diagonal(emission, same_p)
    # model.emissionprob_ = emission
    
    reliab = letters_reliability(text.lower(), order)
    
    # P(наблюдаем символ j | истинное состояние/буква i)
    emission = np.zeros((n_states, n_symbols), dtype=float)
    for i, ch in enumerate(alphabet):
        r = reliab.get(ch, 0.5)
        same_p = 0.9 + 0.029 * r
        same_p = min(max(same_p, 0.97), 0.999)
        other_p = (1.0 - same_p) / (n_symbols - 1)
        emission[i, :] = other_p
        emission[i, i] = same_p
    
    space_idx = alphabet.index(' ')
    emission[space_idx, :] = (1.0 - 0.9999) / (n_symbols - 1)
    emission[space_idx, space_idx] = 0.9999
    model.emissionprob_ = emission
    
    to_idx = {ch: i for i, ch in enumerate(alphabet)}
    # что-то типа [[0], [8], [15], [26]], из букв в индексы цифры
    cripter_text = np.array([to_idx[ch] for ch in text]).reshape(-1, 1)
    
    hidden_text = model.predict(cripter_text)
    
    to_letters = dict(enumerate(alphabet))
    decoded = ''.join(to_letters[s] for s in hidden_text)
    return decoded


print ("HI")
decoded = ""
with open(DECODED_PATH, 'r', encoding='utf-8') as file:
    decoded = file.read()

order = load_order(ORDER_PATH)
text = use_viterbi(decoded,order)

with open(AFTER_PATH, 'w', encoding='utf-8') as file:
    file.write(text)