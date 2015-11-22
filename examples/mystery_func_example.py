# These are the input values you should test the mystery function with
mysteryInputs = [["aaaaa223%"], ["aaaaaaaatt41@#"], ["asdfgh123!"], ["007001007"], ["143zxc@#$ab"], ["3214&*#&!("], ["qqq1dfjsns"], ["12345%@afafsaf"]]


def mystery(magic):
    assert len(magic) > 0

    r1 = f1(magic)

    r2 = f2(magic)

    r3 = f3(magic)

    return  [r1, r2, r3]

def test_func(listt):
    if listt[0] < 0 or listt[2] < 0:
        return False
    elif (listt[0] + listt[1] + listt[2]) < 0:
        return False
    elif listt[0] == 0 and listt[1] == 0:
        return False
    else:
        return True


def f1(ml):
    if len(ml) <6:
        return -1
    elif len(ml) > 12 :
        return 1
    else:
        return 0

def f2(ms):
    digits = 0
    letters = 0
    for c in ms:
        if c in "1234567890":
            digits += 1
        elif c.isalpha():
            letters += 1
    other = len(ms) - digits - letters
    grade = 0

    if (other + digits) > 3:
        grade += 1
    elif other < 1:
        grade -= 1

    return grade

def f3(mn):
    forbidden = ["pass", "123", "qwe", "111"]
    grade = 0
    for word in forbidden:
        if word in mn:
            grade -= 1
    if "%" in mn:
        grade += 1
    return grade