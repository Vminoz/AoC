from cave_class import CaveScan
import numpy as np

def p1_sol(file_name):
    sand_to_show = set(np.logspace(0,3,100).astype(int))
    sand_to_show.add(994)
    cave = CaveScan(file_name, (500,0), False, True, sand_to_show)
    done = False
    while not done:
        done = cave.drop()
    return cave.sand_count

def p2_sol(file_name):
    sand_to_show = set(np.logspace(0,4.5,100).astype(int))
    cave = CaveScan(file_name, (500,0), True, True, sand_to_show)
    i = 0
    done = False
    while not done:
        i+=1
        if i > 3000:
            break
        done = cave.drop()
        if not i % 100:
            print(i, end='\r')
    return cave.sand_count

def main():
    file_name = "input.txt"
    print('P1:', p1_sol(file_name))
    print('P2:', p2_sol(file_name))

if __name__ == "__main__":
    main()