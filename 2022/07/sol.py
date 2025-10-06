from collections import deque
import json

def build_tree(filename:str) -> dict[str:int|dict]:
    root = {}
    path = deque([root])
    with open(filename) as f:
        groups = f.read().split('\n$ ')[1:]
    for g in groups:
        if g[:2]=='cd':
            change_dir(path, g[3:])
        elif g[:2]=='ls':
            look_see(path[-1], g.splitlines()[1:])
    size_dive(root)
    return root

def change_dir(path:deque, target:str):
    if target == '..':
        path.pop()
    elif target == '/':
        root = path[0]
        path.clear()
        path.append(root)
    else:
        cd = path[-1]
        path.append(cd[target])

def look_see(loc:dict[str:int|dict], rows:list[str]):
    for row in rows:
        if row[:3] == 'dir':
            dname = row[4:]
            loc[dname] = {}
        else:
            row_l = row.split()
            loc[row_l[1]] = int(row_l[0])

def size_dive(loc:dict[str:int|dict]) -> int:
    if 'SIZE' in loc:
        return loc['SIZE']
    tot_sz = 0
    for key, item in loc.items():
        if isinstance(item,dict):
            tot_sz += size_dive(item)
        elif isinstance(item, int):
            tot_sz += item
        else:
            raise TypeError(f'{key}:{item} is of unexpected type {type(item)}')
    loc['SIZE'] = tot_sz
    return tot_sz

def p1_sol(loc:dict[str:int|dict]) -> int:
    size_sum = loc['SIZE'] if loc['SIZE'] < 100_000 else 0
    for _, sub_d in dict_dicts(loc):
        size_sum += p1_sol(sub_d)
    return size_sum

def p2_sol(root:dict[str:int|dict], avail=int(7e7), need=int(3e7)) -> tuple[str,int]:
    in_use = root['SIZE']
    free_up = need - (avail - in_use)
    print(f"""P2: Available: {avail}
    In use:    {in_use}
    Needed:    {need}
    → Free up: {free_up}
    """)
    found = find_smaller('/', root, ('/', in_use), free_up)
    print(f'    Solution:  {found}')
    return found

def find_smaller(name:str, loc:dict[str:int|dict],
                 smallest:tuple[str:int], minimum:int) -> bool|tuple[str,int]:
    this_size = loc['SIZE']
    if this_size < minimum:
        return smallest
    if this_size < smallest[1]:
        smallest = (name, this_size)
    for sub_name, sub_d in dict_dicts(loc):
        smallest = find_smaller(sub_name, sub_d, smallest, minimum)
    return smallest

def dict_dicts(d:dict[dict]):
    for key, val in d.items():
        if isinstance(val,dict):
            yield key, val

def print_tree(tree:dict):
    print('#'*80)
    print(json.dumps(tree,indent=4))
    print('#'*80)

def main():
    root = build_tree("in.txt")
    print_tree(root)
    print(f'P1: {p1_sol(root)}')
    p2_sol(root)


if __name__ == "__main__":
    main()