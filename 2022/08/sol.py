import numpy as np

def up_down_left_right():
    return ['↑','↓','←','→']

def look(dir:str, arr:np.ndarray, i:int, j:int) -> np.ndarray:
    match dir:
        case '←':
            return arr[i,:j][::-1]
        case '→':
            return arr[i,j+1:]
        case '↑':
            return arr[:i,j][::-1]
        case '↓':
            return arr[i+1:,j]

def emunemneurate(arr:np.ndarray):
    for i,row in enumerate(arr):
        for j,val in enumerate(row):
            yield i,j,val

def visible_trees(forest:np.ndarray) -> np.ndarray:
    visible = np.zeros_like(forest, bool)
    rows, cols = forest.shape
    for i,j,tree in emunemneurate(forest):
        if i==0 or j==0 or i==rows-1 or j==cols-1:
            visible[i,j] = True
            continue
        for at in up_down_left_right():
            view = look(at, forest, i, j)
            if tree > view.max():
                visible[i,j] = True
                break
    return visible

def scenic_scores(forest:np.ndarray) -> np.ndarray:
    scenic = np.zeros_like(forest)
    for i,j,tree in emunemneurate(forest[1:-1,1:-1]):
        score = 1
        for at in up_down_left_right():
            count = 0
            view = look(at,forest,i+1,j+1)
            for othertree in view:
                count += 1
                if othertree >= tree:
                    break
            score *= count
        scenic[i+1,j+1] = score
    return scenic

def main():
    with open("input.txt") as f:
        forest = np.array([list(row.strip()) for row in f], int)
    p1_result = visible_trees(forest).sum()
    print(p1_result)
    p2_result = scenic_scores(forest).max()
    print(p2_result)

if __name__ == "__main__":
    main()