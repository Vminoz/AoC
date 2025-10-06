import numpy as np

DIRECTION = ((1,0), (0,1), (-1,0), (0,-1), (0,0))

def add_2d(a:tuple, b:tuple) -> tuple[int,int]:
    return (a[0]+b[0],a[1]+b[1])

def manhattan_2d(a:tuple, b:tuple) -> int:
    return abs(a[0]-b[0]) + abs(a[1]-b[1])

def neighborhood_2d(tup:tuple) -> set[tuple[int,int]]:
    return {add_2d(tup,d) for d in DIRECTION}

def tup_swap(tup:tuple, idx:int, val:int):
    return tuple(val if idx == i else t for i,t in enumerate(tup))

class Valley:
    """ Holds a field attribute which is a ndarray where
            0: empty, 1:v, 2:>, 4:^, 8:<, 16:Wall
    """
    SYMBOLS = ('v', '>', '^', '<', '#', '.')

    def __init__(self, field:np.ndarray) -> None:
        self.field = field
        self.start = (0, np.argmax(field[0,:]==0))
        self.end = (field.shape[0]-1, np.argmax(field[-1,:]==0))
        self.time = 0
        self.reset_available(self.start)

    def __str__(self) -> str:
        return '\n'.join([
                 ''.join(Valley.SYMBOLS[int(np.log2(val))] if val
                         else Valley.SYMBOLS[-1] for val in row)
                            for row in self.field])

    def step_field(self, verbose:bool=False) -> None:
        next_field = np.zeros_like(self.field)
        for (i,j),v in np.ndenumerate(self.field):
            if v & 16: # Wall
                next_field[i,j] = v
                continue
            if not v: continue # Empty
            for exp, direction in enumerate(DIRECTION[:-1]):
                if v & 1<<exp:
                    new_pos = add_2d((i,j),direction)
                    if verbose: print((i,j),'→',new_pos)
                    if self.field[new_pos] & 16:
                        ax = exp%2
                        new_pos = tup_swap((i,j), ax,
                                           self.field.shape[ax] -
                                           1 - (i,j)[ax])
                        if verbose:
                            print('↑ wall in axis', ax)
                            print('Replaced by', self.field.shape[ax]-1,
                                '-', (i,j)[ax])
                            print((i,j), 'warp to' ,new_pos)
                    next_field[new_pos] |= 1<<exp
        self.field = next_field
        self.time += 1
        self._available.append(set(zip(*np.where(self.field==0))))
        self._memory_t +=1

    def valid_steps(self, pos:tuple[int,int], t:int):
        if t > self.time:
            for _ in range(t-self.time):
                self.step_field()
        return neighborhood_2d(pos) & self._available[t-(self.time-self._memory_t)]

    def reset_available(self, pos:tuple[int,int]):
        self._available = [{pos}] # available new positions as a 'function' of time
        self._memory_t = 0

    @property
    def available(self):
        return self._available

    @classmethod
    def from_file(cls, file_name):
        with open(file_name) as f:
            field = np.array([
                [1<<cls.SYMBOLS.index(ch) if cls.SYMBOLS.index(ch)<5
                  else 0 for ch in line]
                 for line in f.read().splitlines()])
        return cls(field)

def backtrack(state, prev):
    path = []
    while state is not None:
        path.append(state[0])
        state = prev[state]
    return path

def valley_a_star(valley: Valley, snacks:bool=False):
    """ A* where states are (position, time, h)
    """
    start = valley.start
    end = valley.end
    visited = [{start}]
    prev = {(start, 0): None}
    h_start = manhattan_2d(start, end)
    candidates = [(start, 0, h_start)]
    trips = 0
    cnt = 0
    while candidates:
        candidates = sorted(candidates, key=lambda x: -x[1]-x[2])
        pos,t,_ = candidates.pop()
        cnt += 1
        if not cnt % 1000:
            print('States seen:', cnt, end='\r')

        if pos == end:
            trips += 1
            print(f'Trip {trips}: {t=}'+' '*50)
            if snacks and trips < 3:
                start, end = end, start
                valley.reset_available(start)
                candidates = [(start, t, manhattan_2d(start, end))]
            else:
                print()
                return t, backtrack((pos,t), prev), visited

        for new_pos in valley.valid_steps(pos, t+1):
            if len(visited) < t+2:
                visited.append(set())
            if new_pos not in visited[t+1]:
                visited[t+1].add(new_pos)
                candidates.append((new_pos, t+1, manhattan_2d(new_pos, end)))
                prev[(new_pos, t+1)] = pos, t
    raise RuntimeError('No path found.')

def observe_valley(valley:Valley, show_steps: bool):
    run = True
    while run:
        run = not input()
        valley.step_field(show_steps)
        print(valley)

def main():
    valley = Valley.from_file("in.txt")
    print('P2:', valley_a_star(valley, True)[0])

if __name__ == "__main__":
    main()