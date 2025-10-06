from dataclasses import dataclass
import numpy as np
from collections import deque as DQ


@dataclass
class Valve:
    id:int
    name:str
    flow_rate:int
    tunnels:list

class Volcano:
    def __init__(self, file_name:str, start:str) -> None:
        self.start = start
        self.valves, self.v_list, self.jammed = self.parse(file_name, start)
        self.N = len(self.valves)
        self.cost = self._calc_cost()

    @staticmethod
    def parse(file_name:str, start:str) -> tuple[dict[str:Valve],list[str]]:
        valves = {}
        v_list = []
        jam_id = []
        with open(file_name) as f:
            for i,line in enumerate(f):
                line = line.split('; ')
                tunnels = line[1][22:].lstrip().rstrip().split(', ')
                valve = Valve(i, line[0][6:8], int(line[0][23:]), tunnels)
                valves[valve.name] = valve
                if not valve.flow_rate and valve.name != start:
                    jam_id.append(valve.id)
                v_list.append(valve.name)
        return valves, v_list, jam_id

    def _calc_cost(self) -> np.ndarray:
        cost = 1_000_00 * np.ones((self.N, self.N),int)
        # original adj
        for v in self.valves.values():
            for destination in v.tunnels:
                cost[v.id, self.valves[destination].id] = 1
        # fully connected (Floyd-Warshall)
        for i in range(self.N):
            for j in range(self.N):
                for k in range(self.N):
                    cost[j,k] = min(cost[j,k], cost[j][i] + cost[i][k])
        np.fill_diagonal(cost, 0)
        cost += 1 # one turn to open
        for n_rm, vj_id in enumerate(self.jammed):
            cost[:,vj_id] = 0
            cost[vj_id,:] = 0
            self.N -= 1
            self.valves.pop(self.v_list[vj_id-n_rm])
            self.v_list.pop(vj_id-n_rm)
            for v in self.valves.values():
                if v.id > vj_id-n_rm:
                    v.id -= 1
        self.start_id = self.valves[self.start].id
        print(cost)
        print(cost[np.nonzero(cost)].reshape((self.N, self.N)))
        for v in self.valves.values(): print(v)
        return cost[np.nonzero(cost)].reshape((self.N, self.N))

    def dyn_prod(self, t_max=30):
        """ Top Down DP with states holding
            (cumulative flow, current position, opened valves, time left)
            using memoization of cumulative flow
        """
        self.T = t_max
        closed_ids = frozenset(i for i in range(self.N) if i != self.start_id)
        self.memo = {}
        initial_state = (0, self.start_id, t_max, closed_ids)
        to_check = DQ([initial_state])
        while to_check:
            self.check_tunnels(to_check)
        return self.memo

    def check_tunnels(self, to_check):
        state = to_check.pop()
        cumu_flow, v_id, time_left, closed = state
        for other_v_id in closed:
            tl = time_left - self.cost[v_id, other_v_id]
            if tl < 0:
                continue
            fr = self.valves[self.v_list[other_v_id]].flow_rate
            cl = closed - {other_v_id}
            cf = cumu_flow + tl * fr
            memo_key = (other_v_id, tl, cl)
            if memo_key not in self.memo or cf > self.memo[memo_key]:
                self.memo[memo_key] = cf
                to_check.append((cf, other_v_id, tl, cl))

def main():
    volcano = Volcano("input.txt", 'AA')
    mem30 = volcano.dyn_prod(30)
    print('P1:', max(mem30.values()))

    mem26 = volcano.dyn_prod(26)
    print('P1(26):', max(mem26.values()))
    v_set = frozenset(i for i in range(volcano.N) if i !=volcano.start_id)
    setmem26 = {}
    print('Memo size:', len(mem26))
    for k, v in mem26.items():
        if k[2] not in setmem26 or v > setmem26[k[2]]:
            setmem26[k[2]] = v
    print('Memo size (sets only for key):', len(setmem26))
    curr_max = 0
    for remaining_valves_mc, cf in setmem26.items():
        for remaining_valves_ele, ele_cf in setmem26.items():
            ele_opened = v_set - remaining_valves_ele
            if not (ele_opened).issubset(remaining_valves_mc):
                continue # can't be closed by both
            if cf + ele_cf > curr_max:
                curr_max = cf + ele_cf
                print(f'New max: {curr_max}\n{remaining_valves_mc=}\n{remaining_valves_ele=}')
    print('\nP2:', curr_max)


if __name__ == "__main__":
    main()