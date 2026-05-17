
import nltk
from nltk.corpus import words
from collections import defaultdict
import re
from collections import Counter

def clean_text(file_path):

    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
    
    text = text.lower()
    text = re.sub(r'[^a-z\s]', '', text)
    
    text = re.sub(r'\s+', ' ', text)
    
    return text

clean_text = clean_text('C:/Users/Admin/source/repos/3 sem for git/english.txt')
with open('C:/Users/Admin/source/repos/3 sem for git/cleaned_text.txt', 'w', encoding='utf-8') as file:
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

encoded = caesar_cipher(clean_text,shift)
with open('C:/Users/Admin/source/repos/3 sem for git/encoded.txt', 'w', encoding='utf-8') as file:
    file.write(encoded)
#decoded = caesar_cipher(encoded,-shift)

FREQUENCY = [
    'e', 't', 'a', 'o', 'i', 'n', 's', 'h', 'r', 'd', 
    'l', 'c', 'u', 'm', 'w', 'f', 'g', 'y', 'p', 'b', 
    'v', 'k', 'j', 'x', 'q', 'z'
]
def get_frequency(text):
    freq = {}
    for sim in text:
        if 'a' <= sim <= 'z':
            if sim not in freq:
                freq[sim] = 0
            freq[sim] += 1
    return freq

def get_index(order):
    return {l: i for i, l in enumerate(order)}

def swap_order(order, index_of, i, j):
    order[i], order[j] = order[j], order[i]
    index_of[order[i]] = i
    index_of[order[j]] = j
    
BIGRAMS = [
    'th', 'he', 'in', 'er', 'an', 're', 'nd', 'at', 'on', 'nt',
    'ha', 'es', 'st', 'en', 'ed', 'to', 'it'
]

def get_bigrams(text):
    bigrams = {}
    for i in range(len(text) - 1):
        if 'a' <= text[i] <= 'z' and 'a' <= text[i+1] <= 'z':
            bg = text[i] + text[i+1]
            bigrams[bg] = bigrams.get(bg, 0) + 1
    return bigrams

def best_bigrams(text, sorted_bigrams, order, index_of, score_levl):
    k = 0
    MAX_K = 3
    for bg, _ in sorted_bigrams[:10]:
            if k > MAX_K: break
            if bg[0] not in index_of or bg[1] not in index_of:
                continue
            idx1 = index_of[bg[0]]
            idx2 = index_of[bg[1]]
            current = FREQUENCY[idx1] + FREQUENCY[idx2]
            
            if current not in BIGRAMS:
                best_score = len(BIGRAMS) + 1
                best_change = None
                for tmp_bg in BIGRAMS:
                    #"меняем" вторую букву
                    if tmp_bg[0] == FREQUENCY[idx1]:
                        for j in range(len(FREQUENCY)):
                            if FREQUENCY[j] == tmp_bg[1] and j < len(order):
                                score = BIGRAMS.index(tmp_bg)
                                if score < best_score:
                                    best_score = score
                                    best_change = ('second',j)
                                break

                    #"меняем" первую букву
                    if tmp_bg[1] == FREQUENCY[idx2]:
                        for j in range(len(FREQUENCY)):
                            if FREQUENCY[j] == tmp_bg[0] and j < len(order):
                                score = BIGRAMS.index(tmp_bg)
                                if score < best_score:
                                    best_score = score
                                    best_change = ('first',j)
                                break
                if best_change is None:
                    continue
                #лучшее изменение
                type,j = best_change
                new_order = order.copy()
                new_index_of = index_of.copy()
                
                if type == 'second':
                    swap_order(new_order, new_index_of, idx2, j)
                else:
                    swap_order(new_order, new_index_of, idx1, j)
                    
                new_score = score_dictionary(text, new_order)
                if new_score >= score_levl:
                    score_levl = new_score
                    order = new_order
                    index_of = new_index_of
                    k += 1
    return order, index_of, score_levl

TRIGRAMS = ['the', 'and', 'ing', 'her', 'hat', 'was', 'you', 'for', 'are', 'but','not', 'had', 'him']

def get_trigrams(text):
    trigrams = {}
    for i in range(len(text) - 2):
        if 'a' <= text[i] <= 'z' and 'a' <= text[i+1] <= 'z' and 'a' <= text[i+2] <= 'z':
            tg = text[i] + text[i+1] + text[i+2]
            trigrams[tg] = trigrams.get(tg, 0) + 1
    return trigrams

def best_trigrams(text, sorted_trigrams, order, index_of, score_levl):
    k = 0
    MAX_K = 2
    for tg, _ in sorted_trigrams[:10]:
            if k > MAX_K: break

            if tg[0] not in index_of or tg[1] not in index_of or tg[2] not in index_of:
                continue
            idx1 = index_of[tg[0]]
            idx2 = index_of[tg[1]]
            idx3 = index_of[tg[2]]
            
            current = FREQUENCY[idx1] + FREQUENCY[idx2] + FREQUENCY[idx3]
            new_order = None
            if current not in TRIGRAMS:
                for tmp_tg in TRIGRAMS:
                    if tmp_tg[0] == FREQUENCY[idx1] and tmp_tg[1] == FREQUENCY[idx2]:
                        for j in range(len(FREQUENCY)):
                            if FREQUENCY[j] == tmp_tg[2] and j < len(order):
                                new_order = order.copy()
                                new_index_of = index_of.copy()
                                swap_order(new_order, new_index_of, idx3, j)
                                break
                        break
                    
                    if tmp_tg[1] == FREQUENCY[idx2] and tmp_tg[2] == FREQUENCY[idx3]:
                        for j in range(len(FREQUENCY)):
                            if FREQUENCY[j] == tmp_tg[0] and j < len(order):
                                new_order = order.copy()
                                new_index_of = index_of.copy()
                                swap_order(new_order, new_index_of, idx1, j)
                                break
                        break
            
            if new_order is None:
                continue
            
            new_score = score_dictionary(text,new_order)
            if new_score >= score_levl:
                score_levl = new_score
                order = new_order
                index_of = new_index_of
                k += 1
    return order, index_of, score_levl

nltk.download('words')
dictionary = set(words.words())
dict_by_len = defaultdict(list)
for w in dictionary:
    dict_by_len[len(w)].append(w)
    

def split_words(text,order):
    decoded = []
    index_of = get_index(order)
    for ch in text:
        if 'a' <= ch <= 'z':
            decoded.append(FREQUENCY[index_of[ch]])
        else:
            decoded.append(ch)
            
    return re.findall(r'[a-z]+', ''.join(decoded).lower())

#считаем норм слова
def score_dictionary(text, order):
    # упрощённая быстрая версия: только точные словарные совпадения
    words_list = split_words(text, order)
    if not words_list:
        return 0

    found = 0
    unique_words = set(words_list)
    for w in unique_words:
        n = len(w)
        if n < 4:
            continue
        if w in dict_by_len[n]:
            # вес можно подправить, но без перебора похожих слов
            found += 10
            if n > 7:
                found += 5

    return found

find_close_cache = {}
def find_close(word):
    if word in find_close_cache:
        return find_close_cache[word]
    
    if word in dictionary or len(word) < 4:
        find_close_cache[word] = (word, [])
        return word, []
    
    best_word = None
    best_diff_idx = None
    best_diff = 4
    
    candidates = dict_by_len[len(word)]
    for w in candidates:
        diff_idx = []

        for i in range(len(word)):
            if word[i] != w[i]:
                diff_idx.append(i)
            if len(diff_idx) >= best_diff or len(diff_idx) > 3:
                break
        d = len(diff_idx)
        if 1 <= d <= 3 and d < best_diff:
            best_diff = d
            best_word = w
            best_diff_idx = diff_idx
            if d == 1:
                break

    if best_word is not None and best_diff <= 3:
        result = (best_word, best_diff_idx)
    else:
        result = (None, [])

    find_close_cache[word] = result
    return result

def letters_reliability(text, order):
    words = split_words(text, order)
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

def decoding_byfrequency(text):
    freq = get_frequency(text)
    order = [ch for ch, _ in sorted(freq.items(),key = lambda x: x[1], reverse=True)]
    
    bigram_freq = get_bigrams(text)
    sorted_bigrams = sorted(bigram_freq.items(), key=lambda x: x[1], reverse=True)
    trigram_freq = get_trigrams(text)
    sorted_trigrams = sorted(trigram_freq.items(), key=lambda x: x[1], reverse=True)
    best_score = score_dictionary(text,order)
    
    index_of = get_index(order)
    
    # тут я в общем переставляю буквы в отсортированной по убывающей частоте символов очереди
    # на основе биограмм: по наилучшей из замены первой/второй буквы
    # на основе триограмм: меняем первые две или последние две
    # качество замены всегда оценивается по словарю
    for _ in range(30):
        old_score = best_score
        order, index_of, best_score = best_bigrams(text, sorted_bigrams, order, index_of, best_score)
        order, index_of, best_score = best_trigrams(text, sorted_trigrams, order, index_of, best_score)
        if best_score == old_score: break
    best_score = score_dictionary(text,order)
    # reliability = letters_reliability(text, order)
    
    # reliable_letters = set()
    # suspect_letters = set()
    # for l in order:
    #     r = reliability.get(l, 0.5)
    #     if r >= 0.85:
    #         reliable_letters.add(l)
    #     elif r < 0.5:
    #         suspect_letters.add(l)

    # тут я в общем-то меняю буквы в очереди на основе самого словаря
    # в длинных словах где 1-3 неверных буквы, опять же с оценкой качества замены
    for _ in range(10):
        old_score = best_score
        
        words = split_words(text, order)
        cnt = Counter(words)

        candidate_words = [w for w, c in cnt.most_common(300) if len(w) > 5]
        
        improved = False
        for w in candidate_words:
            dict_word, diff_idx = find_close(w)
            if dict_word is None or dict_word == w:
                continue
        
            for i in diff_idx:
                if i >= len(w):
                    continue
                idx = index_of[w[i]]
                for j in range(len(FREQUENCY)):
                    if dict_word[i] == FREQUENCY[j]:
                        new_order = order.copy()
                        new_index = index_of.copy()
                        swap_order(new_order, new_index, idx, j)
                        new_score = score_dictionary(text, new_order)
                        if new_score > best_score:
                            order = new_order
                            index_of = new_index
                            best_score = new_score
                            improved = True
                        break
                if improved: break
            if improved: break
        if not improved or best_score == old_score: break
    
    result = []
    index_final = get_index(order)
    for sim in text:
        if 'a' <= sim <= 'z':
            result.append(FREQUENCY[index_final[sim]])
        else:
            result.append(sim)
    
    return ''.join(result)

decoded = decoding_byfrequency(encoded)

with open('C:/Users/Admin/source/repos/3 sem for git/decoded.txt', 'w', encoding='utf-8') as file:
    file.write(decoded)