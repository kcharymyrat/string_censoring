from constants import (
    HORIZONTAL_RULE,
    SPACES,
    BRUTE_FORCE,
    BRUTE_STARTED,
    LINE
)


def brute_force_algo_log(text, word):
    text_len = len(text)
    word_len = len(word)
    text_lst = list(text)
    print(f'{LINE}: "{text}"')

    for i in range(text_len - word_len + 1):
        print(f"|{text}")
        print(f"|{' ' * i}{word}")

        match = True
        for j in range(0, word_len):
            if word[j] != text[i + j]:
                print(f"{SPACES}{text[i + j]} != {word[j]}")
                match = False
                break
            else:
                print(f"{SPACES}{word[j]} = {text[i + j]}")

        if match:
            print(f"{SPACES}Found on {i} position")
            for k in range(word_len):
                text_lst[i + k] = "*"

    return "".join(text_lst)


def brute_force_algo_no_log(text, word):
    text_len = len(text)
    word_len = len(word)

    text_lst = list(text)
    match = False

    for i in range(text_len - word_len + 1):
        match = True
        for j in range(0, word_len):
            if word[j] != text[i + j]:
                match = False
                break

        if match:
            for k in range(word_len):
                text_lst[i + k] = "*"

    return "".join(text_lst)


def brute_force_choice(file_name, word, is_log):
    lines = []
    with open(file_name) as file:
        results = []
        if is_log:
            print(BRUTE_STARTED)
            print(HORIZONTAL_RULE)
            print("Not needed")
            print(HORIZONTAL_RULE)

            for line in file:
                lines.append(line.strip())
                result = brute_force_algo_log(line.strip(), word)
                results.append(result)
        else:
            for line in file:
                lines.append(line.strip())
                result = brute_force_algo_no_log(line.strip(), word)
                results.append(result)
    return results, lines
