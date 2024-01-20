def create_bad_char_table(pattern):
    bad_char_table = {}

    for i in range(len(pattern)):
        bad_char_table[pattern[i]] = len(pattern) - i - 1
    # utils.log(f"BCT: {bad_char_table}")
    bad_char_table["*"] = len(pattern)
    return bad_char_table


def create_helper_table(pattern):
    m = len(pattern)
    helper_table = {}  # Create an empty dictionary

    for shift in range(m - 1, 0, -1):
        pointer_1 = m - 1  # Adjusted for 0-based indexing
        pointer_2 = m - 1 - shift  # Adjusted for 0-based indexing

        while pointer_2 >= 0:
            # If the characters match, we move the pointers to the left
            if pattern[pointer_1] == pattern[pointer_2]:
                pointer_1 -= 1
                pointer_2 -= 1
                if pointer_2 == -1:  # Adjusted for 0-based indexing
                    helper_table[shift] = m - shift
                    break
            else:
                helper_table[shift] = m - 1 - shift - pointer_2
                break
    helper_table[m] = 0  # There is no match if we shift the whole pattern

    return helper_table


def create_good_suffix_table(pattern):
    m = len(pattern)
    table = {0: 1}  # Create an empty dictionary
    helper_table = create_helper_table(pattern)

    # Initially fill the table using m+|t|
    for i in range(1, m):
        table[i] = i + m

    # Update the table if the suffix t is available elsewhere
    for i in range(m, 0, -1):
        if helper_table[i] > 0:
            table[helper_table[i]] = i + helper_table[i]

    # Update the table if there is any suffix that matches the prefix
    for i in range(m, 0, -1):
        if helper_table[i] + i == m:
            for j in range(helper_table[i] + 1, m):
                table[j] = min(table[j], j + i)

    return table


def create_border_table(pattern):
    """ Create the border table used in the good suffix rule. """
    m = len(pattern)
    border_table = [0] * (m + 1)
    border = 0

    for i in range(1, m):
        while border > 0 and pattern[i] != pattern[border]:
            border = border_table[border - 1]
        if pattern[i] == pattern[border]:
            border += 1
        else:
            border = 0
        border_table[i] = border

    return border_table


def boyer_moore_algorithm(text, pattern):
    n = len(text) - 1
    m = len(pattern) - 1
    bad_char_table = create_bad_char_table(pattern)
    good_suffix_table = create_good_suffix_table(pattern)

    s = 0  # s is shift of the pattern with respect to text
    while s <= (n - m):
        j = m
        print("---------------")
        print("pattern =", pattern)
        print("j = ", j)
        print("pattern[j] =", pattern[j])
        print("text[s + j] =", text[s + j])

        while j >= 0 and pattern[j] == text[s + j]:
            print("in while j >= 0 and ...: j =", j)
            print("in while j >= 0 and ...:pattern[j] =", pattern[j])
            print("in while j >= 0 and ...:text[s + j] =", text[s + j])
            j -= 1

        if j >= 0:
            print("in if j >= 0: text[s + j] =", text[s + j])
            print("in if j >= 0: pattern[j] =", pattern[j])
            print("in if j >= 0: bad_char_table.get(text[s + j]) =", bad_char_table.get(text[s + j]))
            bad_char_shift = max(0, j - bad_char_table.get(text[s + j], 10))
            good_suffix_shift = good_suffix_table[j]
            print(bad_char_shift, good_suffix_shift)
            s += max(bad_char_shift, good_suffix_shift)
        else:
            return s  # Pattern found at position s

        print("m =", m)
        print("n =", n)
        print("s =", s)
        print("j =", j)

    return -1  # Pattern not found


def create_border_table(pattern):
    """ Create the border table used in the good suffix rule. """
    m = len(pattern)
    border_table = [0] * (m + 1)
    border = 0

    for i in range(1, m):
        while border > 0 and pattern[i] != pattern[border]:
            border = border_table[border - 1]
        if pattern[i] == pattern[border]:
            border += 1
        else:
            border = 0
        border_table[i] = border

    return border_table


def bm_good_suffix_rule(text, pattern):
    n = len(text)
    m = len(pattern)

    # If the pattern is empty return 0
    if m == 0:
        return 0

    good_suffix_table = create_good_suffix_table(pattern)
    text_pointer = m - 1  # Search from the end of the pattern

    while text_pointer < n:
        pattern_pointer = m - 1  # Adjusted for 0-based indexing

        # Check for match and shift pointers
        while pattern_pointer >= 0 and text[text_pointer] == pattern[pattern_pointer]:
            # print("shift =", text_pointer - 1)
            text_pointer -= 1
            pattern_pointer -= 1

        # Match found
        if pattern_pointer < 0:
            # print("shift =", text_pointer + m + 1)
            print(f"Pattern found at {text_pointer + 1}")
            text_pointer += m + 1

        # Determining shift size
        else:
            suffix_length = m - pattern_pointer
            good_suffix_shift = good_suffix_table[suffix_length - 1]

            # Update the text pointer
            # print("shift =", text_pointer + good_suffix_shift)
            text_pointer += good_suffix_shift
