def update_top(top, k, new_val):
    for i in range(k):
        if new_val > top[i]:
            top.insert(i, new_val)
            top.pop()
            return top
    return top

def main():
    current_sum = 0
    k = 3
    top = [0 for _ in range(k)]
    with open("input.txt",'r') as f:
        for line in f:
            if line != "\n": # Not blank line
                current_sum += int(line)
                continue
            top = update_top(top, k, current_sum)
            current_sum = 0
    #last sum
    top = update_top(top, k, current_sum)
    print(f'Final top {k}:{top}, sum:{sum(top)}')

if __name__ == "__main__":
    main()