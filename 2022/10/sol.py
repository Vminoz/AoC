def print_crt(buffers):
    for row in buffers:
        st = ''.join('█'*letter +' '*(1-letter) for letter in row)
        print(st)

def main():
    cycle = 0
    x = 1
    buffers = [[]]
    samples = []
    with open("input.txt") as f:
        for line in f:
            cycle = step(x, cycle, buffers, samples)
            if line[0] == 'a':
                cycle = step(x, cycle, buffers, samples)
                x += int(line[5:].rstrip())
    print('P1:',sum(v*(20+40*i) for i,v in enumerate(samples)))
    print('P2:')
    print_crt(buffers)

def step(x, cycle, buffers, samples):
    buffers[-1].append(int(abs(x-cycle) < 2))
    cycle += 1
    if cycle == 20:
        samples.append(x)
    elif cycle == 40:
        buffers.append([])
        cycle = 0
    return cycle

if __name__ == "__main__":
    main()