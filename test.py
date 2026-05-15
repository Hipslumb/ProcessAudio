
import nltk
from nltk.corpus import words
from collections import defaultdict
import re

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

BIGRAMS = [
    'th', 'he', 'in', 'er', 'an', 're', 'nd', 'at', 'on', 'nt',
    'ha', 'es', 'st', 'en', 'ed', 'to', 'it', 'ou', 'ea', 'hi',
    'is', 'or', 'ti', 'as', 'te', 'et', 'ng', 'of', 'al', 'de'
]

def get_bigrams(text):
    bigrams = {}
    for i in range(len(text) - 1):
        if 'a' <= text[i] <= 'z' and 'a' <= text[i+1] <= 'z':
            bg = text[i] + text[i+1]
            bigrams[bg] = bigrams.get(bg, 0) + 1
    return bigrams

def best_bigrams(text, sorted_bigrams, order, score_levl):
    k = 0
    MAX_K = 3
    for bg, _ in sorted_bigrams[:10]:
            if k > MAX_K: break
            idx1 = order.index(bg[0])
            idx2 = order.index(bg[1])
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
                if type == 'second':
                    new_order[idx2], new_order[j] = new_order[j], new_order[idx2]
                else:
                    new_order[idx1], new_order[j] = new_order[j], new_order[idx1]
                    
                new_score = score_dictionary(text, new_order)
                if new_score >= score_levl:
                    score_levl = new_score
                    order = new_order
                    k += 1
    return order, score_levl

TRIGRAMS = [
    'the', 'and', 'ing', 'her', 'hat', 'was', 'you', 'for', 'are', 'but',
    'not', 'had', 'him', 'with', 'all', 'she', 'ere', 'his', 'tha', 'thi',
    'ere', 'hich', 'which', 'ould', 'this', 'from', 'have', 'they', 'will', 'said'
]

def get_trigrams(text):
    trigrams = {}
    for i in range(len(text) - 2):
        if 'a' <= text[i] <= 'z' and 'a' <= text[i+1] <= 'z' and 'a' <= text[i+2] <= 'z':
            tg = text[i] + text[i+1] + text[i+2]
            trigrams[tg] = trigrams.get(tg, 0) + 1
    return trigrams

def best_trigrams(text, sorted_trigrams, order, score_levl):
    k = 0
    MAX_K = 2
    for tg, _ in sorted_trigrams[:10]:
            if k > MAX_K: break

            idx1 = order.index(tg[0])
            idx2 = order.index(tg[1])
            idx3 = order.index(tg[2])
            
            current = FREQUENCY[idx1] + FREQUENCY[idx2] + FREQUENCY[idx3]
            new_order = None
            if current not in TRIGRAMS:
                for tmp_tg in TRIGRAMS:
                    if tmp_tg[0] == FREQUENCY[idx1] and tmp_tg[1] == FREQUENCY[idx2]:
                        for j in range(len(FREQUENCY)):
                            if FREQUENCY[j] == tmp_tg[2] and j < len(order):
                                new_order = order.copy()
                                new_order[idx3], new_order[j] = new_order[j], new_order[idx3]
                                break
                        break
                    
                    if tmp_tg[1] == FREQUENCY[idx2] and tmp_tg[2] == FREQUENCY[idx3]:
                        for j in range(len(FREQUENCY)):
                            if FREQUENCY[j] == tmp_tg[0] and j < len(order):
                                new_order = order.copy()
                                new_order[idx1], new_order[j] = new_order[j], new_order[idx1]
                                break
                        break
            
            if new_order is None:
                continue
            
            new_score = score_dictionary(text,new_order)
            if new_score >= score_levl:
                score_levl = new_score
                order = new_order
                k += 1
    return order, score_levl

nltk.download('words')
dictionary = set(words.words())
dict_by_len = defaultdict(list)
for w in dictionary:
    dict_by_len[len(w)].append(w)
    

def split_words(text,order):
    decoded = []
    for ch in text:
        if 'a' <= ch <= 'z':
            decoded.append(FREQUENCY[order.index(ch)])
        else:
            decoded.append(ch)
            
    words = re.findall(r'[a-z]+', ''.join(decoded).lower())
    return words

#считаем норм слова
def score_dictionary(text,order):
    words = split_words(text,order)
    if not words:
        return 0
    
    found = 0
    unique_words = list(set(words))
    for w in unique_words:
        if w in dictionary:
            found += 1
            if len(w) > 7:
                found += 1
        elif len(w) > 7:
            found -= 3
    return found

find_close_cache = {}
def find_close(word):
    if word in find_close_cache:
        return find_close_cache[word]
    
    if word in dictionary or len(word) < 7:
        return word, []
    
    candidates = dict_by_len[len(word)]
    for w in candidates:
        if len(w) != len(word):
            continue
        
        diff_idx = []
        for i in range(len(w)):
            if word[i] != w[i]:
                diff_idx.append(i)
            if len(diff_idx) == 3:
                break
        if len(diff_idx) < 3:
            find_close_cache[word] = (w, diff_idx)
            return w, diff_idx
    find_close_cache[word] = (None, [])
    return None, []

def decoding_byfrequency(text):
    freq = get_frequency(text)
    order = [ch for ch, _ in sorted(freq.items(),key = lambda x: x[1], reverse=True)]
    
    bigram_freq = get_bigrams(text)
    sorted_bigrams = sorted(bigram_freq.items(), key=lambda x: x[1], reverse=True)
    trigram_freq = get_trigrams(text)
    sorted_trigrams = sorted(trigram_freq.items(), key=lambda x: x[1], reverse=True)
    best_score = score_dictionary(text,order)
    for _ in range(100):
        order,best_score = best_bigrams(text, sorted_bigrams,order,best_score)
        order,best_score = best_trigrams(text, sorted_trigrams,order,best_score)
    best_score = score_dictionary(text,order)
    

    for _ in range(10):
        order_copy = order.copy()
        words = split_words(text, order)
        unique_words = list(set(words))
        for w in unique_words:
            dict_word, diff_idx = find_close(w)
            if dict_word is not None and dict_word != w:
                for i in diff_idx:
                    idx = order_copy.index(w[i])
                    for j in range (len(FREQUENCY)):
                        if dict_word[i] == FREQUENCY[j]:
                            order_copy[idx], order_copy[j] = order_copy[j], order_copy[idx]
                            break
        
        score = score_dictionary(text,order_copy)
        if (score > best_score):
            order = order_copy
            best_score = score
        else:
            break
    result = []
    for sim in text:
        if 'a' <= sim <= 'z':
            result.append(FREQUENCY[order.index(sim)])
        else:
            result.append(sim)
    
    return ''.join(result)

decoded = decoding_byfrequency(encoded)

with open('C:/Users/Admin/source/repos/3 sem for git/decoded.txt', 'w', encoding='utf-8') as file:
    file.write(decoded)