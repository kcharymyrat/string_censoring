from constants import (
    HORIZONTAL_RULE,
    PREPROCESSING,
    RK_STARTED,
    SPACES,
    LINE,
    PRIME,
    BASE,
    WORDS_HASH_VALS,
    BASE_NUM,
    PRIME_NUM,
)

import utils
from utils import log


def create_hash(pattern, base, prime):
    max_e = len(pattern.strip()) - 1
    hash_val = 0
    for i, c in enumerate(pattern):
        hash_val += (ord(c) * base ** (max_e - i)) % prime
        # if pattern == "e":
        #     print(f"ord(c) = {ord(c)}")
        #     print(f"base = {base}")
        #     print("max_e =", max_e)
        #     print("i =", i)
        #     print("hash_val =", hash_val)

    hash_val %= prime
    return hash_val


def create_hash_table(patterns, base, prime):
    hash_table = {}
    for pattern in patterns:
        hash_val = create_hash(pattern, base, prime)
        hash_table[hash_val] = pattern
    return hash_table


def get_words(file_name):
    words = []
    try:
        with open(file_name) as file:
            for word in file:
                words.append(word.strip())
        return words
    except FileNotFoundError:
        return [file_name]


def rk_algo(text, word_len, hash_table, base, prime):
    log(f'{LINE}: "{text}"\n')

    match_indexes = []
    t_len = len(text)
    p_len = word_len

    hash_sub_s = create_hash(text[:p_len], base, prime)

    for i in range(t_len - p_len + 1):
        log(f"|{text}")
        log(f"|{' ' * i}{'^' * p_len}")
        log(f"{SPACES}Hash: {hash_sub_s}")
        for h, s in hash_table.items():
            if h == hash_sub_s:
                log(f"{SPACES}Hash equality on {i} position ({hash_table[hash_sub_s]})")
                if hash_table[hash_sub_s] == text[i:i + p_len]:
                    log(f"{SPACES}Found on {i} position ({hash_table[hash_sub_s]})")
                    match_indexes.append(i)
                else:
                    log("False positive error!")


        if i < t_len - p_len:
            hash_sub_s = ((hash_sub_s - ord(text[i]) * pow(base, p_len - 1)) * base + ord(text[i + p_len])) % prime

    return match_indexes


def rk_choice(file_name, words_file):
    results = []
    match_found = False
    with open(file_name) as file:
        log(RK_STARTED)
        log(HORIZONTAL_RULE)
        log(PREPROCESSING)

        words = get_words(words_file)
        hash_table = create_hash_table(words, BASE_NUM, PRIME_NUM)
        # if words_file == "e":
        #     print(words, hash_table)

        log(f"{PRIME}: {PRIME_NUM}")
        log(f"{BASE}: {BASE_NUM}")
        log(f"{WORDS_HASH_VALS}:")

        for k, v in hash_table.items():
            log(f"{SPACES}{k}: {v}")

        log(HORIZONTAL_RULE)

        for line in file:
            line_lst = list(line.strip())
            match_indexes = rk_algo(line.strip(), len(words[0]), hash_table, BASE_NUM, PRIME_NUM)
            # if words_file == "bcb":
            #     print("match_indexes =", match_indexes)
            if not match_indexes:
                results.append(line.strip())
                continue
            match_found = True
            for index in match_indexes:
                for i in range(len(words[0])):
                    line_lst[index + i] = "*"

            results.append("".join(line_lst))

    # if words_file == "bcb":
    #     print("results =", results)
    #     print("match_found =", match_found)
    return results, match_found


# print(create_hash("hello", 256, 101))
# print(create_hash_table(["eya", "ann", "mea", "e", "rl"], BASE_NUM, PRIME_NUM))
# hash_table = create_hash_table(["e"], BASE_NUM, PRIME_NUM)
# print(rk_algo("test", 1, hash_table, BASE_NUM, PRIME_NUM))
