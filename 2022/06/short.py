BS = 14
f = open("input.txt").read()
print(next(i+BS for i,_ in enumerate(f) if len(set(f[i:i+BS]))==BS))