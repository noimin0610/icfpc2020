import sys
from interpreter import *

sys.setrecursionlimit(200000)

SUCCESS_RESULT_FILE = 'check_result_success.txt'
ERROR_RESULT_FILE = 'check_result_error.txt'


def main():
    row_number = 0
    with open(SUCCESS_RESULT_FILE, 'w') as success_file:
        with open(ERROR_RESULT_FILE, 'w') as error_file:
            try:
                while True:
                    s = input()
                    row_number += 1

                    print('{}\t{}'.format(row_number, s), file=sys.stderr)
                    tokens = lex(s)
                    # print(tokens, file=sys.stderr)
                    program = None
                    try:
                        program = parse(tokens[2:])
                    except ValueError as e:
                        error_file.write(str(e))
                        error_file.write('\n')
                        error_file.write(s)
                        error_file.write('\n')
                        continue
                    # print(program, file=sys.stderr)
                    try:
                        result = program.eval()
                        display = '{} = {} = {}'.format(
                            tokens[0], result, tokens[2:])
                        success_file.write(display)
                        success_file.write('\n')
                    except EOFError:
                        pass
            except EOFError:
                pass


if __name__ == "__main__":
    main()
