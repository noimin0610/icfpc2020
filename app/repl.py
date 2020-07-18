from interpreter import *


def main():
    while True:
        print('> ', end='')
        s = input()
        tokens = lex(s)
        program = parse(tokens)
        result = program.eval()
        print(result)


if __name__ == "__main__":
    main()
