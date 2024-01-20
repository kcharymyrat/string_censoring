from constants import (
    PREPROCESSING,
    HORIZONTAL_RULE,
    LINE,
    BM_STARTED
)

from utils import log


def create_bad_char_table(pattern):
    bad_char_table = {}

    for i in range(len(pattern) - 1):
        bad_char_table[pattern[i]] = i
    log(f"BCT: {bad_char_table}")
    return bad_char_table


def preprocess_strong_suffix(shift, bpos, pattern, m):
    i = m
    j = m + 1
    bpos[i] = j
    while i > 0:
        while j <= m and pattern[i - 1] != pattern[j - 1]:
            if shift[j] == 0:
                shift[j] = j - i
            j = bpos[j]
        i -= 1
        j -= 1
        bpos[i] = j


def preprocess_case2(shift, bpos, m):
    j = bpos[0]
    for i in range(0, m):
        if shift[i] == 0:
            shift[i] = j
        if i == j:
            j = bpos[j]
    log(f"GST: {shift}")
    return shift


def create_good_suffix_table(pattern):
    m = len(pattern)

    bpos = [0] * (m + 1)

    # initialize all occurrence of shift to 0
    shift = [0] * (m + 1)
    #
    # # do preprocessing
    preprocess_strong_suffix(shift, bpos, pattern, m)
    preprocess_case2(shift, bpos, m)

    return shift


def bm_algo(text, pattern, bct, gst):
    log(f'{LINE}: "{text}"\n')
    result = []

    s = 0
    m = len(pattern)
    n = len(text)
    while s <= n - m:
        log("|" + text)
        log("|" + " " * s + pattern)
        j = m - 1
        while j >= 0 and pattern[j] == text[s + j]:
            j -= 1
        if j < 0:
            result.append(s)
            log(f"\tFound on {s} position")
            s += gst[0]
            log(f"\tGST[0] = {gst[0]}")
            log(f"\tShifted by {gst[0]}")
        else:
            bad_character = text[s + j]
            if bad_character in bct:
                shift_bc = j - bct[bad_character]
            else:
                shift_bc = j + 1
            shift_gs = gst[j + 1]
            log(f"\tBCT['{bad_character}'] = {shift_bc}")
            log(f"\tGST[{j + 1}] = {shift_gs}")
            # utils.log(f"\t{shift_bc} {'>' if shift_bc > shift_gs else '<'} {shift_gs}")
            s += max(shift_bc, shift_gs)
            log(f"\tShifted by {max(shift_bc, shift_gs)}")

    return result


def bm_choice(file_name, word):
    results = []
    match_found = False
    with open(file_name) as file:
        log(BM_STARTED)
        log(HORIZONTAL_RULE)
        log(PREPROCESSING)
        bct = create_bad_char_table(word)
        gst = create_good_suffix_table(word)
        log(HORIZONTAL_RULE)

        for line in file:
            line_lst = list(line.strip())
            match_indexes = bm_algo(line.strip(), word, bct, gst)
            if not match_indexes:
                results.append(line.strip())
                continue
            match_found = True
            for index in match_indexes:
                for i in range(len(word)):
                    line_lst[index + i] = "*"

            results.append("".join(line_lst))
    return results, match_found


