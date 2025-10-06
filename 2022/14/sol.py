from cave_class import CaveScan

def p1_sol(file_name):
    cave = CaveScan(file_name, (500,0))
    with open('_start.txt', 'w', encoding='utf-8') as f:
        f.write(str(cave))
    done = False
    while not done:
        done = cave.drop()
    print()
    with open('_end.txt', 'w', encoding='utf-8') as f:
        f.write(str(cave))
    return cave.sand_count

def p2_sol(file_name):
    cave = CaveScan(file_name, (500,0), True)
    i = 0
    done = False
    while not done:
        done = cave.drop()
        if not i % 100:
            print(i, end='\r')
        i+=1
    with open('_ohno.txt', 'w', encoding='utf-8') as f:
        f.write(str(cave))
    return cave.sand_count()

def main():
    file_name = "input.txt"
    print('P1:', p1_sol(file_name))
    print('P2:', p2_sol(file_name))

if __name__ == "__main__":
    main()