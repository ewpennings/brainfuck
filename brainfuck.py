import sys
from getch import getch
from os import path


def check_syntax(script):
    l = len(script)

    try:
        # Match all '[' and ']' before execution
        i = 0
        while i < l:
            ch = script[i]
            j = i
            if ch is '[':
                n = 0
                # skip to matching ']'
                while True:
                    j += 1
                    if j >= l:
                        raise SyntaxError("Unmatched '['")
                    ch = script[j]
                    if ch is '[':
                        n += 1
                    elif ch is ']':
                        if n == 0:
                            break
                        else:
                            n -= 1
            elif ch is ']':
                n = 0
                # find matching '['
                while True:
                    j -= 1
                    if j < 0:
                        raise SyntaxError("Unmatched ']'")
                    ch = script[j]
                    if ch is ']':
                        n += 1
                    elif ch is '[':
                        if n == 0:
                            break
                        else:
                            n -= 1
            i += 1
    except SyntaxError as e:
        print(e)
        exit(1)


def interpret(script):
    # Initialize tape with a byte array of size 30000
    # The tape may grow in size if needed
    tape = bytearray(30000)

    # Point to the first cell
    p = 0

    # Filter all non-brainfuck characters from the script
    min_script = ''.join([ch for ch in script if ch in "><+-[].,"])
    l = len(min_script)

    check_syntax(min_script)

    try:
        # Interpret the script
        i = 0
        while i < l:
            ch = min_script[i]
            if ch is '>':
                p += 1
                if p >= len(tape):
                    tape.extend(bytearray(100))
            elif ch is '<':
                p -= 1
                if p < 0:
                    raise IndexError("Pointer out of bounds")
            elif ch is '+':
                tape[p] += 1
            elif ch is '-':
                tape[p] -= 1
            elif ch is '[':
                if tape[p] == 0:
                    n = 0
                    # skip to matching ']'
                    while True:
                        i += 1
                        ch = min_script[i]
                        if ch is '[':
                            n += 1
                        elif ch is ']':
                            if n == 0:
                                break
                            else:
                                n -= 1
            elif ch is ']':
                if tape[p] != 0:
                    n = 0
                    # return to matching '['
                    while True:
                        i -= 1
                        ch = min_script[i]
                        if ch is ']':
                            n += 1
                        elif ch is '[':
                            if n == 0:
                                break
                            else:
                                n -= 1
            elif ch is '.':
                sys.stdout.write(chr(tape[p]))
            elif ch is ',':
                ch = getch()
                x = ord(ch)
                if x == 13:
                    # Convert return to newline
                    tape[p] = 10
                elif x == 26:
                    # Leave cell unchanged on EOF
                    pass
                else:
                    tape[p] = x
            i += 1
    except IndexError as e:
        print(e)
        exit(1)


def main(argv):
    if len(argv) < 2:
        print("Usage: brainfuck.py <filename>")
        exit(1)

    filename = argv[1]

    if not path.exists(filename):
        print("File not found: {0}".format(filename))
        exit(1)

    with open(filename, "r") as fh:
        script = fh.read()

    interpret(script)

if __name__ == "__main__":
    main(sys.argv)
