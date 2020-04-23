from itertools import permutations
import re
import sys
import time


# excludes variants with element's format "01", "00", "0000" etc
def check_null(comb: list) -> bool:
    for el in comb:
        if bool(re.fullmatch('0{1,}\d{1,}', el)):
            return False
    return True


# generate list of permutations's variants of symbols from 'arr' with length 'n'
def shift(n: int, arr: list) -> list:
    c = [arr[0]] * n
    rez = [[arr[0]] * n]
    while c != [arr[-1]] * n:
        i = -1
        while True:
            if c[i] != arr[-1]:
                c[i] = arr[arr.index(c[i]) + 1]
                break
            else:
                c[i] = arr[0]
                i -= 1
        rez.append(c.copy())
    return rez


# generate sequence of combinations number's digits
def comb_numb(numb: str) -> list:
    # get variants of combinations number's digits,
    # where ',' will divide number's groups
    comb_var = shift(len(numb) - 1, [[','], []])
    rez = []
    numbs = [[n] for n in list(numb)]
    # divide 'numb' by digits's groups according to scheme from 'comb_var'
    for var in comb_var:
        var = var + [[]]
        subrez = []
        for el in list(map(list, zip(numbs, var))):
            subrez += el[0] + el[1]
        rez.append(''.join(subrez).split(','))
    rez.remove([numb])  # delete 'numb' self from sequence
    return rez


def calc(data: str, d: str) -> str:

    numbers = comb_numb(data)  # get variants of combinations number's digits

    for num in numbers:
        if not check_null(num):  # to exclude leading zeros in integer
            continue
        # get variants of operators's combinations
        operators = shift(len(num) - 1, [['+'], ['-'], ['*'], ['/']])
        for operator in operators:
            # generate sequence of variants turns of operators execution,
            # parenthesis analog
            turn = permutations(range(1, len(operator) + 1))
            # form to expressions
            for step in turn:
                st = list(step)
                op = (list(operator)).copy()
                n = num.copy()
                expr = ''
                for i in range(len(st)):
                    ind = st.index(i + 1)
                    expr = ''.join(['('] + [n[ind]] + op[ind] + [n[ind + 1]] + [')'])
                    n.pop(ind)
                    n.pop(ind)
                    n.insert(ind, expr)
                    op.pop(ind)
                    st.pop(ind)

                try:
                    a = eval(expr)
                except ZeroDivisionError:
                    pass
                else:
                    if a == int(d):
                        return expr

    #return None


# MAIN CODE
while True:
    print('Enter numbers for calculation, or both "0" to exit.')
    source_number = input('Source number -> ')
    an_number = input('Another number -> ')
    t = time.time()
    if source_number != '0' or an_number != '0':
        if calc(source_number, an_number):
            print(f'{calc(source_number, an_number)} = {an_number}')
            print(f'Calculate time - {time.time() - t} sec.\n')
        else:
            print('Sorry, but no')
            print(f'Calculate time - {time.time() - t} sec.\n')
    else:
        print('Poka')
        sys.exit()
