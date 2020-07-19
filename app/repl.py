from interpreter import *
import format


def main():
    while True:
        print('> ', end='')
        s = input()
        tokens = lex(s)
        program = parse(tokens)
        result = program.eval()
        result = str(result)
        if len(result) > 40:
            print(format.fmt(result))
        else:
            print(result)


if __name__ == "__main__":
    main()
