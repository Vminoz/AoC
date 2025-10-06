class CRT:
    def __init__(self, width:int=40) -> None:
        self.width = width
        self.half_width = width//2
        self.cycle = 0
        self.sprite = 1
        self.buffers = [[]]
        self.samples = []

    def _draw(self):
        return int(abs(self.sprite - self.cycle) < 2)

    def step(self, sprite_mv:int=0):
        self.buffers[-1].append(self._draw())
        self.cycle += 1
        if self.cycle == self.half_width:
            self.samples.append(self.sprite)
        elif self.cycle == self.width:
            self.buffers.append([])
            self.cycle = 0
        self.sprite += sprite_mv

    def collect_samples(self) -> list:
        return sum(v*(self.half_width+(i*self.width))
                for i,v in enumerate(self.samples))

    def __str__(self):
        return '\n'.join(''.join('█'*v +' '*(1-v)
                                 for v in b)
                         for b in self.buffers)

def main():
    crt = CRT(40)
    with open("input.txt") as f:
        for line in f:
            crt.step()
            if line[0] == 'a':
                crt.step(int(line[5:].rstrip()))
    print('P1:', crt.collect_samples())
    print(f'P2:\n{crt}')

if __name__ == "__main__":
    main()