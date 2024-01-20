import prefix_function

from utils import log

from constants import (
    HORIZONTAL_RULE,
    SPACES,
    PREPROCESSING,
    KMP_STARTED,
    LPS,
    LINE
)


def kmp_choice(file_name, word):
    results = []
    match_found = False
    with open(file_name) as file:
        log(KMP_STARTED)
        log(HORIZONTAL_RULE)
        log(PREPROCESSING)
        prefix = prefix_function.prefix_function_efficient(word)
        log(f"{LPS}: {prefix}")
        log(HORIZONTAL_RULE)

        for line in file:
            line_lst = list(line.strip())
            match_indexes = kmp(line.strip(), word, prefix)
            if not match_indexes:
                results.append(line.strip())
                continue
            match_found = True
            for index in match_indexes:
                for i in range(len(word)):
                    line_lst[index + i] = "*"

            results.append("".join(line_lst))

    return results, match_found


def kmp(text, pattern, prefix):
    log(f'{LINE}: "{text}"\n')

    text_index = 0
    pattern_index = 0

    match_indexes = []
    is_shifted = True

    while text_index < len(text):
        if is_shifted:
            log(f"|{text}")
            log(f"|{' ' * (text_index - pattern_index)}{pattern}")

        if text[text_index] == pattern[pattern_index]:
            log(f"{SPACES}{text[text_index]} = {pattern[pattern_index]}")
            is_shifted = False
        else:
            log(f"{SPACES}{text[text_index]} != {pattern[pattern_index]}")
            is_shifted = True

        if text[text_index] == pattern[pattern_index]:
            text_index += 1
            pattern_index += 1

            if pattern_index == len(pattern):
                match_index = text_index - pattern_index
                match_indexes.append(match_index)
                log(f"{SPACES}Found on {match_index} position")
                is_shifted = True
                log(f"{SPACES}Shifted by {pattern_index - prefix[pattern_index - 1]}")
                pattern_index = prefix[pattern_index - 1]
        else:
            if pattern_index != 0:
                log(f"{SPACES}Shifted by {pattern_index - prefix[pattern_index - 1]}")
                pattern_index = prefix[pattern_index - 1]
            else:
                log(f"{SPACES}Shifted by 1")
                text_index += 1

    return match_indexes

