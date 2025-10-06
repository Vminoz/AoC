from itertools import accumulate

dirs = {}
for line in open('in.txt'):
    match line.split():
        case '$', 'cd', '/':
            curr = ['/']
        case '$', 'cd', '..':
            curr.pop()
        case '$', 'cd', x:
            curr.append(f'{x}/')
        case size, _:
            if size.isdigit():
                size = int(size)
                for p in accumulate(curr):
                    dirs[p] = size + dirs.get(p,0)

print(sum(s for s in dirs.values() if s <= 100_000),
      min(s for s in dirs.values() if s >= dirs[''] - 40_000_000))