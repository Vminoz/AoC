import re
import numpy as np
from collections import deque as DQ

def parse_bps(file_name):
    re_num = re.compile(r'\d+')
    blueprints = []
    with open(file_name) as f:
        blueprints.extend(tuple(int(n)
                                for n in re_num.findall(line))
                          for line in f)
    return blueprints

def make_cost_func(blueprint:tuple[int,...]):
    """ Returns dict of costs as given by a blueprint
        1: buy ore_rob
        2: buy clay_rob
        3: buy obs_rob
        4: buy geo_rob
    Args:
        blueprint (tuple[int,...]): Six integers
    """
    ore_ore, ore_clay, ore_obs, clay_obs, ore_geo, obs_geo = blueprint
    ore = ore_ore, ore_clay, ore_obs, ore_geo
    return {
        0: np.array((ore[0], 0, 0)),
        1: np.array((ore[1], 0, 0)),
        2: np.array((ore[2], clay_obs, 0)),
        3: np.array((ore[3], 0, obs_geo)),
        4: np.array((max(ore), clay_obs, obs_geo))
    }

def dp_mining(cost_func:dict, t_max:int=24) -> bool:
    """
    Args:
        cost_func:
            A dict with keys in int[0,3] that outputs the cost
            vector (ore, clay, obs) for constructing any robot.

    Problem:
        State (key is state without geodes):
            (geodes, time, bank, robots) :=
                (bank_geodes, time_left
                (bank_ore, bank_clay, bank_obs),
                (robs_ore, robs_clay, robs_obs, robs_geo))
        Value: bank_geo (when constructing a geo_rob)

    Optimization:
        Always buy geo if possible, will give one less memoization dimension
        Don't buy bots we don't need, eg if bots[0] = max_cost[0], don't buy 0
        Give up (prune) if building geo robots or beating current won't be
            possible triangularly from now (best case)
        !TODO Save up for specific bot. Statespace++, Branching--

    """
    triangular = [t*(t+1)//2 for t in range(t_max)]
    geode_cost = cost_func[3]
    max_cost = cost_func[4]

    max_geo = 0
    times = set()
    memo = {}
    init_state = (0, t_max, (0,0,0), (1,0,0))
    state_queue = DQ([init_state])
    while state_queue:
        geodes, time_left, bank, bots = state_queue.popleft()
        max_geo = max(geodes, max_geo)

        if time_left not in times:
            times.add(time_left)
            print(f't {time_left:>2} QS: {len(state_queue)}')

        tl = time_left - 1

        if geodes + triangular[tl] <= max_geo:
            continue # building a geo bot every minute won't beat max

        forecast = np.array(bots)*tl + bank
        if (geode_cost - forecast).sum() > triangular[tl]:
            continue # Won't afford more geode bots

        next_bank = np.array(bank) + bots
        if (bank >= geode_cost).all(): # can buy geode robot
            geodes += tl # add future instantly
            next_state = (geodes, tl, tuple(next_bank-geode_cost), bots)
            check_state(memo, state_queue, next_state)
            continue

        # Add do-nothing state
        check_state(memo, state_queue,
                    (geodes, tl, tuple(next_bank), bots))

        for resource in range(3):
            if bots[resource] == max_cost[resource]:
                continue # don't overbuy
            cost = cost_func[resource]
            if (bank < cost).any():
                continue # can't buy
            next_bots = np.array(bots)
            next_bots[resource] += 1
            next_state = (geodes, tl, tuple(next_bank-cost), tuple(next_bots))
            check_state(memo, state_queue, next_state)
    return max_geo

def check_state(memo:dict, state_queue:DQ, next_state:tuple):
    geodes, time_left, bank, bots = next_state
    memo_key = (time_left, bank, bots)
    if memo_key not in memo or memo[memo_key] < geodes:
        memo[memo_key] = geodes
        if next_state[1] > 0:
            state_queue.append(next_state)

def main():
    bps = parse_bps('input.txt')

    p1 = 0
    for bp in bps:
        print(bp)
        cost_func = make_cost_func(bp[1:])
        best = dp_mining(cost_func)
        print('Max Geodes:', best)
        p1 += best * bp[0]
    print('P1:', p1)

    p2 = 1
    for bp in bps[:3]:
        print(bp)
        cost_func = make_cost_func(bp[1:])
        best = dp_mining(cost_func, 32)
        print(best)
        p2 *= best
    print('P2:', p2)

if __name__ == "__main__":
    main()