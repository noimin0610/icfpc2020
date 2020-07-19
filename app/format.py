import sys


def fmt(s):
    s = s.replace(', ', ',') + '.'
    dep = 0
    n = len(s)
    head = 0
    tail = 0
    lines = []
    base_indent = '    '
    while head < n:
        if s[head] == '(':
            k = 0
            for i in range(1, min(30, n-head)):
                if s[head+i] == '(':
                    break
                if s[head+i] == ')':
                    k = i
                    if s[head+i+1] == ',':
                        k = i+1
                    break
            lines.append(''.join([
                base_indent*dep,
                s[tail:head+1+k],
            ]))
            head += 1+k
            tail = head
            if k == 0:
                dep += 1
        elif s[head] == ',':
            lines.append(''.join([
                base_indent*dep,
                s[tail:head+1],
            ]))
            head += 1
            tail = head
        elif s[head] == ')':
            if tail < head:
                lines.append(''.join([
                    base_indent*dep,
                    s[tail:head],
                ]))
                tail = head
            dep -= 1
            k = 2 if (head+1 < n and s[head+1] == ',') else 1
            lines.append(''.join([
                base_indent*dep,
                s[head:head+k],
            ]))
            head += k
            tail = head
        else:
            head += 1
    if tail + 1 < head:
        lines.append(s[tail:head])

    return '\n'.join([line for line in lines if line])


def main():
    s = input()
    print(fmt(s))


if __name__ == "__main__":
    main()
