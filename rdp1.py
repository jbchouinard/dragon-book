import fileinput


def inputgen():
    for line in fileinput.input():
        for c in line:
            yield c


input = inputgen()
lookahead = next(input)
matched = ""


def match(char):
    global lookahead
    global matched
    if lookahead == char:
        matched = matched + lookahead
        lookahead = next(input)
        return True
    else:
        raise SyntaxError


def s():
    if lookahead == '(':
        match("(")
        s()
        match(")")
        s()


s()
print(matched)
