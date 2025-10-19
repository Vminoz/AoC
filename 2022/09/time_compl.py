from time import perf_counter

from matplotlib import pyplot as plt
from sol import simulate_rope

lens = [2**i for i in range(1, 11)]
lens = [10]
times = []
for i in lens:
    st = perf_counter()
    simulate_rope(i)
    st = perf_counter() - st
    times.append(st)
    print(f"{i=} : {st}", end="\r")

plt.plot(lens, times)
plt.show()
