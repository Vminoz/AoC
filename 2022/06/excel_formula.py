N = 14
ROW0 = 1
ands = ''
for i in range(N):
    row = ROW0 + i
    for j in range(i+1,N):
        other_row = ROW0 + j
        ands += f'A{row}<>A{other_row};'

print(f'=AND({ands[:-1]})')