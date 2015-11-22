i1 = ["hello", [1,2,3], 4, []]
i2 = [None, 3, 4, []]
i3 = ["pew pew", [1,2,3], 'a', []]
i4 = ["World", [1,2,3], 4, 3]
i5 = ["yop yop", [1,2,3], 3, []]

inputs = [i1, i2, i3, i4, i5]

def foobar(a, b, c, d):
    f = str(a)
    if f == "hello":
        raise Exception("example exception")
    for e in b:
        c = c + 1
    d.append("Hello")


def barfoo(a, b, c, d):
    c = c - 4
    if c == 0:
        raise Exception('c < 4')
    c = c + 3
    return c


def test(res):
    return True