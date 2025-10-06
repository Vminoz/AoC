def check_pair(line:str) -> int:
    l1,u1,l2,u2 = [int(i) for i in line.replace('-',',').split(',')]
    if l2<l1 or (l1==l2 and u2>u1): # Swap to make 1st
        l1,u1,l2,u2 = l2,u2,l1,u1
    if l1<=l2 and u2<=u1:
        return 1
    return 2 if l2<=u1 else 0

def main():
    pair1_sum = 0
    pair2_sum = 0
    with open("input.txt",'r') as f:
        for line in f:
            check_code = check_pair(line.rstrip('\n'))
            pair1_sum += (check_code==1)
            pair2_sum += (check_code>0)
    print(pair1_sum, pair2_sum)

if __name__ == "__main__":
    main()