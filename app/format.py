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
            for i in range(1, min(10, n-head)):
                if s[head+i] == '(':
                    break
                if s[head+i] == ')':
                    k = i+1
                    break
            lines.append(''.join([
                base_indent*dep,
                s[tail:head+1+k],
            ]))
            tail = head+1+k
            head = tail
            if k == 0:
                dep += 1
        elif s[head] == ',':
            lines.append(''.join([
                base_indent*dep,
                s[tail:head+1],
            ]))
            tail = head+1
        elif s[head] == ')':
            lines.append(''.join([
                base_indent*dep,
                s[tail:head],
            ]))
            dep -= 1
            k = 2 if head+1 < n and s[head+1] == ',' else 1
            lines.append(''.join([
                base_indent*dep,
                s[head:head+k],
            ]))
            tail = head+k
            head = tail
        head += 1
    if tail + 1 < head:
        lines.append(s[tail:head])

    return '\n'.join(lines)


def main():
    s = input()
    print(fmt(s))


if __name__ == "__main__":
    main()
