import re
from collections import Counter
from nltk.corpus import words as nltk_words
from nltk.corpus import brown as nltk_brown
import itertools

def frequency_analysis(ciphertext):
    return Counter(filter(str.isalpha, ciphertext))

def match_pattern(frequency_order, hints):
    eng_freq_order = 'ETAOINSHRDLCUMWFGYPBVKJXQZ'
    key = {cipher: eng for cipher, eng in zip(frequency_order, eng_freq_order) if cipher not in hints}
    key.update(hints)  # Apply hints to the key
    return key

def decrypt(ciphertext, key):
    return ''.join(key.get(c, c) for c in ciphertext)

def update_key_for_word_match(key, word, segment):
    for w, s in zip(word, segment):
        if w.isalpha() and s.isalpha() and key.get(s.upper(), s) != w:
            key[s.upper()] = w.lower()
    return key

def find_segment_start_positions(decrypted_text, word):
    return [m.start() for m in re.finditer(r'\b' + re.escape(word) + r'\b', decrypted_text.lower())]

def get_common_words(min_length=3, frequency_threshold=50):
    words = nltk_words.words() + nltk_brown.words()
    word_freq = Counter(words)
    common_words = {word.upper() for word, freq in word_freq.items() if freq > frequency_threshold and len(word) >= min_length}
    return common_words

def identify_double_letters(ciphertext):
    double_letters = re.findall(r'(\w)\1', ciphertext)
    common_double_letters = ['EE', 'OO', 'LL', 'SS', 'TT']
    possible_matches = {dl: common_double_letters for dl in double_letters}
    return possible_matches

def map_consonants():
    consonants = "BCDFGHJKLMNPQRSTVWXYZ"
    mappings = {}
    for c in consonants:
        # Map each consonant to its adjacent letters in the alphabet
        index = consonants.find(c)
        adjacent = consonants[max(0, index-1):min(len(consonants), index+2)]
        mappings[c] = adjacent
    return mappings

def check_decryption(decrypted_text, common_words):
    words = decrypted_text.split()
    return any(word.upper() in common_words for word in words)

def test_consonant_mappings(ciphertext, key, mappings, common_words):
    best_key = key.copy()
    best_match_count = 0
    for c, adjacent in mappings.items():
        for replacement in adjacent:
            new_key = key.copy()
            new_key[c] = replacement.lower()
            decrypted = decrypt(ciphertext, new_key)
            match_count = sum(word.upper() in common_words for word in decrypted.split())
            if match_count > best_match_count:
                best_match_count = match_count
                best_key = new_key
    return best_key
def refine_key(ciphertext, key):
    common_words = get_common_words()
    double_letter_matches = identify_double_letters(ciphertext)
    consonant_mappings = map_consonants()

    for dl, matches in double_letter_matches.items():
        for match in matches:
            new_key = key.copy()
            new_key[dl] = match.lower()
            key = test_consonant_mappings(ciphertext, new_key, consonant_mappings, common_words)

    return key

# Example usage
ciphertext = "HPPI AP QXX TPF"
hints = {}
freq_analysis = frequency_analysis(ciphertext)
frequency_order = ''.join([item[0] for item in freq_analysis.most_common()])
initial_key = match_pattern(frequency_order, hints)
refined_key = refine_key(ciphertext, initial_key)
refined_decryption = decrypt(ciphertext, refined_key)
print("Refined Decryption with Hints:", refined_decryption)

# ciphertext_1 = "JF JKKMU J JZG"
# ciphertext_2 = "P DGS'W WGEZ BPFOW SUT"
# ciphertext_3 = "FMSFT ADI WDCBSW XJXSI GSADIS YCWWCKU EDHK"
