from constants import (
    PREPROCESSING,
    LPS,
    HORIZONTAL_RULE,
)


def prefix_function(string):
    s = string
    p = [0 for i in s]

    # Iterate though the substrings
    for i in range(1, len(s)):
        sub_s = s[:i]
        # Iterate through characters - num of iterations shall be one less than chars
        for j in range(len(sub_s) - 1):
            first_half = sub_s[:j + 1]
            last_halt = sub_s[len(sub_s) - j - 1: len(sub_s)]
            if first_half == last_halt:
                p[i - 1] = j + 1

    return p


def prefix_function_efficient(s):
    n = len(s)
    p = [0 for _ in s]
    p[0] = 0

    # Iterate though the substrings
    for i in range(1, n):
        j = p[i - 1]

        while (j > 0) and (s[j] != s[i]):
            j = p[j - 1]

        if s[j] == s[i]:
            p[i] = j + 1
        else:
            p[i] = 0

    return p


if __name__ == "__main__":
    print(prefix_function_efficient("mammamia"))
    print(prefix_function("mammamia"))
