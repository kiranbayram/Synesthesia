def foobar(a):
    a = 4 + 5
    b = 12
    a, b = b, a
    return b


def barfoo(a):
    s = 'pew pew'
    b = a + 5
    return [s, b]