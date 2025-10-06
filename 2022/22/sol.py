import numpy as np

SYMBOL = {' ': 0, '.': 1, '#': 2}
FACING = ((0,1), (1,0), (0,-1), (-1,0)) # RDLU
DIAGON = ((1,1), (1,-1), (-1,-1), (-1,1))

def parse_notes(file_name) -> tuple[np.ndarray, list[tuple[int,int]]]:
    with open(file_name) as f:
        at_instructions = False
        for i, line in enumerate(f):
            if not i:
                map_arr = np.array([SYMBOL[ch] for ch in line[:-1]])
                r_len = map_arr.shape[0]
                continue
            line = line.rstrip()
            if not line: at_instructions = True
            elif not at_instructions:
                l_len = len(line)
                map_arr = np.vstack((map_arr,
                                     [SYMBOL[line[i]] if i<l_len else 0
                                      for i in range(r_len)]))
            else:
                instructions = []
                num = ''
                for ch in line:
                    if ch.isdigit():
                        num += ch
                    else:
                        instructions.extend((int(num), 1 - 2 * (ch == 'L')))
                        num = ''
                if num: instructions.append(int(num))
                return map_arr, instructions

def slide(pos:np.ndarray, direction:int, n:int,
          map_arr:np.ndarray, warp_dict:dict):
    dir_v = np.array(FACING[direction])
    new_direction = direction
    for _ in range(n):
        new_pos = pos + dir_v
        if out_of_bounds(new_pos, map_arr):
            if warp_dict:
                warp_pos, new_direction = warp_dict[(tuple(pos), direction)]
                dir_v = FACING[new_direction]
                new_pos = np.array(warp_pos)
            else: # Flat warp
                new_pos -= dir_v * valid_width(map_arr,
                                               1-direction%2,
                                               pos[direction%2])
            print('warped to',new_pos)
        if map_arr[tuple(new_pos)] == 2:
            print('Hit', new_pos)
            break
        pos = new_pos
        direction = new_direction
        print('went to',pos)
    return pos, direction

def valid_width(map_arr:np.ndarray, axis:int, pos:int) -> int:
    track = map_arr[:,pos] if axis == 0 else map_arr[pos,:]
    valid_indices = np.nonzero(track)[0]
    return valid_indices[-1] - valid_indices[0] + 1

def out_of_bounds(pos:np.ndarray, map_arr:np.ndarray) -> bool:
    return ((pos < 0).any() or (pos >= map_arr.shape).any()
                or not map_arr[tuple(pos)])

def is_armpit(position:tuple[int,int], map_arr:np.ndarray) -> bool|np.ndarray:
    if out_of_bounds(np.array(position), map_arr): return False
    for d in FACING:
        pos = position + np.array(d)
        if out_of_bounds(pos, map_arr): return False
    armpit_normal = None
    for d in DIAGON:
        pos = position + np.array(d)
        if out_of_bounds(pos, map_arr):
            if armpit_normal is None:
                armpit_normal = d
            else: return False # Can't have two armpit holes
    return False if armpit_normal is None else armpit_normal

def make_cube_warp(map_arr:np.ndarray):
    warp = {}
    for pos, v in np.ndenumerate(map_arr):
        if v and (armpit := is_armpit(pos, map_arr)):
            d_l = DIAGON.index(armpit)
            d_r = (d_l + 1) % 4
            n_l, n_r = d_r, d_l # initially directions are each other's outwards normal
            p_r = np.array(pos)
            print(f'Found armpit at {pos}, left d:{FACING[d_l]}, right d:{FACING[d_r]}')
            p_l = np.array(pos)
            while True: # Stop criterion: left and right edge path turn simultaneously
                angles = 0
                next_r = p_r + FACING[d_r]
                if out_of_bounds(next_r, map_arr):
                    print('r turn')
                    # Turn right instead
                    angles = 1
                    d_r = (d_r + 1) % 4
                    n_r = (n_r + 1) % 4
                    next_r = p_r
                else:
                    p_r = next_r

                next_l = p_l + FACING[d_l]
                if out_of_bounds(next_l, map_arr):
                    print('l turn')
                    # Turn left instead
                    angles += 1
                    if angles == 2: break
                    d_l = (d_l - 1) % 4
                    n_l = (n_l - 1) % 4
                else:
                    p_l = next_l
                print(next_l, next_r)

                warp[(tuple(p_r), n_r)] = (tuple(p_l), (n_l+2)%4)
                warp[(tuple(p_l), n_l)] = (tuple(p_r), (n_r+2)%4)

                # input()
    return warp

def draw_path(map_arr:np.ndarray, instructions:list, warp_dict:dict=None):
    position = np.array((0, np.argmax(map_arr[0,:] == 1))) # Argmax shorthand for "first True"
    direction = 0
    turning = True
    for inst in instructions:
        turning = not turning
        if turning:
            direction = (direction + inst) % 4
            print(f'At {position}, heading {direction}')
            continue
        # Not Turning → Move
        position, direction = slide(position, direction, inst, map_arr, warp_dict)
    print(position, direction)
    return ((position+1)*(1000,4)).sum() + direction

def main():
    map_arr, instructions = parse_notes("input.txt")
    print('P1:', draw_path(map_arr, instructions))
    cube_warp = make_cube_warp(map_arr)
    print(cube_warp)
    print('P2:', draw_path(map_arr, instructions, cube_warp))

if __name__ == "__main__":
    main()