import argparse

import utils
import brute_force
import kmp
import bm_algo
import rabin_karp

from constants import (
    HORIZONTAL_RULE,
    NO_INAPPROPRIATE,
    BRUTE_FORCE,
    KMP,
    BM,
    RK,
)


def parse_input(args):
    algo = args.algorithm
    word = args.word
    file_name = args.file
    is_log = args.logging
    multiple = args.multiple
    if multiple:
        # then word is a filename, loop over the file
        pass

    # Load text of the file
    if algo == BRUTE_FORCE:
        results, lines = brute_force.brute_force_choice(file_name, word, is_log)
        if is_log:
            print(HORIZONTAL_RULE)
        if results == lines:
            print(NO_INAPPROPRIATE)
        else:
            for result in results:
                print(result)
        return results

    elif algo == KMP:
        results, match = kmp.kmp_choice(file_name, word)
        utils.log(HORIZONTAL_RULE)
        if not match:
            print(NO_INAPPROPRIATE)
            return
        for result in results:
            print(result)

    elif algo == BM:
        results, match = bm_algo.bm_choice(file_name, word)
        utils.log(HORIZONTAL_RULE)
        if not match:
            print(NO_INAPPROPRIATE)
            return
        for result in results:
            print(result)

    elif algo == RK:
        results, match = rabin_karp.rk_choice(file_name, word)
        utils.log(HORIZONTAL_RULE)
        if not match:
            print(NO_INAPPROPRIATE)
            return
        for result in results:
            print(result)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--algorithm", type=str,
                        choices=['brute-force', 'knuth-morris-pratt',
                                 'boyer-moore', 'rabin-karp', 'aho-corasick',
                                 'aho-corasick-wildcard'],
                        help="String-searching algorithm", required=True)
    parser.add_argument("-w", "--word", type=str,
                        help="Inappropriate content", required=True)
    parser.add_argument("-f", "--file", type=str,
                        help="Text file that should be processed",
                        required=True)
    parser.add_argument("-l", "--logging", action='store_true',
                        help="Enable logging")
    parser.add_argument("-m", "--multiple", action='store_true',
                        help="Use multiple words for inappropriate content")
    arguments = parser.parse_args()

    if arguments.multiple and (arguments.algorithm not in
                               ['rabin-karp', 'aho-corasick']):
        parser.error("--multiple requires rabin-karp or aho-corasick usage.")

    utils.is_log = arguments.logging
    parse_input(arguments)

