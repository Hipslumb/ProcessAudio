import numpy as np
from hmmlearn import hmm

# словарь оч медленный пупупууппупу
import nltk
from nltk.corpus import words
from collections import defaultdict, Counter
import re
from freq import DECODED_PATH, ENCODED_PATH, CLEAN_PATH
from parametrs import percent
# текст после декодирования частотами, зашифрованный текст, оригинальный текст

# текст после этого Витерби
AFTER_PATH = 'text/a_viterbi.txt'

def get_weights(arr):
    weights = {}
    for rank, smf in enumerate(arr):
        weights[smf] = len(arr) - rank + 1
    return weights

def get_frequency(text):
    freq = {}
    for sim in text:
        if 'a' <= sim <= 'z' or sim == ' ':
            if sim not in freq:
                freq[sim] = 0
            freq[sim] += 1
    return freq

def get_bigrams(text):
    bigrams = {}
    for i in range(len(text) - 1):
        if ('a' <= text[i] <= 'z' or text[i] == ' ') and ('a' <= text[i+1] <= 'z' or text[i+1] == ' '):
            bg = text[i] + text[i+1]
            bigrams[bg] = bigrams.get(bg, 0) + 1
    return bigrams

if __name__ == '__main__':
    nltk.download('words')
    dictionary = set(words.words())
    dict_by_len = defaultdict(list)
    for w in dictionary:
        dict_by_len[len(w)].append(w)

def letters_reliability(text):
    words = re.findall(r'[a-z]+', text.lower())
    if not words:
        return {}

    cnt = Counter(words)
    words_list = list(cnt.keys())
    
    good_words = set()
    close_words = {}
    for w in words_list:
        n = len(w)
        if n < 4:
            continue
        candidates = dict_by_len[n]
        if w in candidates:
            good_words.add(w)
            continue

        best_word = None
        best_diff_idx = None
        best_diff = 4  # до 3 отличий

        for dict_word in candidates:
            diff_idx = []
            for i in range(n):
                if dict_word[i] != w[i]:
                    diff_idx.append(i)
                    if len(diff_idx) > 3:
                        break
            d = len(diff_idx)
            if 1 <= d <= 3 and d < best_diff:
                best_diff = d
                best_word = dict_word
                best_diff_idx = diff_idx
                if d == 1:
                    break
        if best_word is not None and best_diff <= 3:
            close_words[w] = best_diff_idx

    letter_words = defaultdict(list)
    for w in words_list:
        for ch in set(w):
            letter_words[ch].append(w)
            
    reliability = {}
    for l, ws in letter_words.items():
        total = sum(cnt[w] for w in ws)
        if total < 5:
            reliability[l] = 0.5
            continue
        good = 0
        long_good = 0
        for w in ws:
            w_count = cnt[w]
            n = len(w)
            if w in good_words:
                good += w_count
                if n > 7:
                    long_good += w_count
            elif w in close_words:
                bad_here = False
                for i in close_words[w]:
                    if i < n and w[i] == l:
                        bad_here = True
                        break
                if not bad_here:
                    good += w_count
                    if n > 7:
                        long_good += w_count
        if total == 0:
            reliability[l] = 0.5
            continue
        base = good / total
        bonus = (long_good / total)*0.5
        reliability[l] = min(1.0, base + bonus)
    return reliability 

# переход от буквы к букве
def transition_matrix(bg_w):
    alphabet = 'abcdefghijklmnopqrstuvwxyz '
    n = len(alphabet)
    
    A = np.ones((n, n)) * 0.0001
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

# оригинальный текст чисто для сбора частот биграмм и букв
def use_viterbi(orig_text, text):
    letter_w = get_weights(get_frequency(orig_text))
    bg_w = get_weights(get_bigrams(orig_text))
    
    model = hmm.CategoricalHMM(n_components=27, init_params='')
    A = transition_matrix(bg_w)
    pi = start_probs(letter_w)
    model.startprob_ = pi
    model.transmat_ = A
    
    alphabet = 'abcdefghijklmnopqrstuvwxyz '
    n_states = len(alphabet)
    n_symbols = n_states
    
    reliab = letters_reliability(text)
    
    min_p = 0.7
    max_p = 0.999
    # ???????
    emission = np.zeros((n_states, n_symbols), dtype=float)
    for i, ch in enumerate(alphabet):
        r = reliab.get(ch, 0.5)
        same_p = min_p + (max_p - min_p) * r
        same_p = min(max(same_p, min_p), max_p)
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

if __name__ == '__main__':
    decoded = ""
    with open(DECODED_PATH, 'r', encoding='utf-8') as file:
        decoded = file.read()

    clean = ""
    with open(CLEAN_PATH, 'r', encoding='utf-8') as file:
        clean = file.read()
    
    text = use_viterbi(clean,decoded)
    with open(AFTER_PATH, 'w', encoding='utf-8') as file:
        file.write(text)
    
    print("ПОСЛЕ ВИТЕРБИ ")
    pers = percent(clean, text)