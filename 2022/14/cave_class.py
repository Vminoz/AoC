import numpy as np
from matplotlib import pyplot as plt

class CaveScan:
    SYMBOLS = {0:'░', 1:'█', 2:'▓', 3:'▚', 4:'▔'}

    def __init__(self, file_name:str,
                 source:tuple[int,int], floor:bool=False,
                 animate:bool=False, interesting:set=None) -> None:
        self.paths, self.lt, self.rb = self.parse_file(file_name, source)
        if floor:
            self._add_floor(source)
        self.source = (source[0]-self.lt[0],
                       source[1]-self.lt[1])
        self.shape = tuple(1 + self.rb - self.lt)
        self.model = np.zeros(self.shape)
        self.full = False
        self._add_features()
        self.animate = animate
        self.sand_count = 0
        if animate:
            self.floor = floor
            self.interesting = interesting
            self.frame_num = 0
            fdpi = 1/plt.rcParams['figure.dpi']
            self.fig = plt.figure(figsize=(fdpi*self.shape[0],
                                           fdpi*self.shape[1]))
            ax = self.fig.add_axes([0,0,1,1])
            ax.axis('off')
            self.img = ax.imshow(self.model.T)

    def __str__(self) -> str:
        return '\n'.join([
                 ''.join(CaveScan.SYMBOLS[val] for val in row)
                            for row in self.model.T])

    def _mkframe(self):
        self.img.set_data(self.model.T)
        self.fig.savefig(f'frames/{1*(not self.floor)+2*(self.floor)}/'+
                         f'{self.frame_num:05}.png')
        if not self.frame_num % 10:
            print(self.frame_num,end='\r')
        self.frame_num += 1

    @staticmethod
    def parse_file(file_name:str, source:tuple[int,int]):
        paths = []
        ul = np.array(source)
        lr = np.array(source)
        with open(file_name) as f:
            for line in f:
                edges = line.rstrip().split(' -> ')
                for i,edge in enumerate(edges):
                    x,y = (int(v) for v in edge.split(','))
                    ul[0] = min(x,ul[0])
                    ul[1] = min(y,ul[1])
                    lr[0] = max(x,lr[0])
                    lr[1] = max(y,lr[1])
                    edges[i] = (x,y)
                paths.append(edges)
        return paths, ul, lr

    def _add_floor(self, source: tuple[int,int]):
        self.rb[1] += 2
        drop_height = self.rb[1] - source[1]
        self.rb[0] += drop_height
        self.lt[0] -= drop_height
        self.paths.append([(self.lt[0],self.rb[1]),tuple(self.rb)])

    def _add_features(self):
        self.model[self.source] = 4
        for path in self.paths:
            for i,end in enumerate(path[1:], start=1):
                start = path[i-1] - self.lt
                end = path[i] - self.lt
                if start[0]>end[0] or start[1]>end[1]:
                    start, end = end, start
                self.model[start[0]:end[0]+1,start[1]:end[1]+1] = 1

    def drop(self) -> bool:
        if self.full:
            return True
        self.sand = np.array(self.source)
        done = False
        while not done:
            done = self._trickle()
            if (self.sand == self.source).all():
                self.full = True
                if self.animate: plt.close()
                break
        return False

    def _trickle(self) -> bool:
        if self.animate and (
            self.interesting is None or self.sand_count in self.interesting):
            self._mkframe()
        if not (self.sand == self.source).all():
            self.model[self.sand[0], self.sand[1]] = 0
        for dir in [(0,1), (-1,1), (1,1)]:
            newpos = self.sand + dir
            if not self._in_bounds(newpos):
                self.full = True
                self.model[self.sand[0], self.sand[1]] = 3
                return True
            if not self.model[newpos[0], newpos[1]]:
                self.sand = newpos
                self.model[newpos[0], newpos[1]] = 3
                return False
        self.sand_count += 1
        self.model[self.sand[0], self.sand[1]] = 2
        return True

    def _in_bounds(self, index) -> bool:
        return 0<=index[0]<self.shape[0] and 0<=index[1]<self.shape[1]
