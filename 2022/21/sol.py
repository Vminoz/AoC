from collections import deque as DQ

OPERATOR = {
    '+' : int.__add__,
    '-' : int.__sub__,
    '*' : int.__mul__,
    '/' : int.__floordiv__
}

def parse_monkeys(file_name) -> dict:
    monkeys = {}
    with open(file_name) as f:
        for line in f:
            if len(line) > 16:
                monkeys[line[:4]] = (line[11], line[6:10], line[13:17])
            else:
                monkeys[line[:4]] = int(line[6:].rstrip())
    return monkeys

def get_monkey_val(monkey:str, monkeys:dict):
    m_val = monkeys[monkey]
    if isinstance(m_val, int):
        return m_val
    m_op, m_1, m_2 = m_val
    return OPERATOR[m_op](get_monkey_val(m_1, monkeys),
                          get_monkey_val(m_2, monkeys))

def path_to(target:str, monkey:str, monkeys:dict) -> list:
    if monkey == target:
        return [1]
    m_val = monkeys[monkey]
    if isinstance(m_val, int):
        return []
    for m in m_val[1:]:
        if path := path_to(target, m, monkeys):
            path.append(m)
            return path

def match_root(monkeys, target='humn'):
    monkeys['root'] = ('=', *monkeys['root'][1:])
    targ_path = DQ(path_to(target, 'root', monkeys)[1:])
    curr_m = monkeys['root']
    next_m = targ_path.pop()
    indep_m = curr_m[3 - curr_m.index(next_m)]
    ref_value = get_monkey_val(indep_m, monkeys)
    print('at, root we need',next_m,":", ref_value)
    while targ_path:
        curr_m:tuple = monkeys[next_m]
        print('at,', next_m ,'we need', ref_value)
        next_m = targ_path.pop()
        indep_i = 3 - curr_m.index(next_m)
        indep_m = curr_m[indep_i]
        indep_v = get_monkey_val(indep_m, monkeys)
        print('indep monkey val:', indep_v ,'operator', curr_m[0])
        match curr_m[0]:
            case '*': ref_value //= indep_v
            case '+': ref_value -= indep_v
            case '/':
                if indep_i == 1: # dependent divisor
                    ref_value = indep_v // ref_value
                else: ref_value *= indep_v
            case '-':
                if indep_i == 1: # dependent sub
                    ref_value = indep_v - ref_value
                else: ref_value += indep_v
    return ref_value

def main():
    monkeys = parse_monkeys("input.txt")
    print('P1:', get_monkey_val('root', monkeys))

    ref_value = match_root(monkeys)
    print('P2:', ref_value)

if __name__ == "__main__":
    main()