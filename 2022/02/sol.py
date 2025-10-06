HAND = {'A': 1, 'B': 2, 'C': 3}
N_GEST = 3

def bound_add(val, other_val=1, bound:int=N_GEST):
    return (val-1 + other_val) % bound + 1

def strat(gesture, outcome):
    match outcome:
        case 'X': return bound_add(gesture, -1)
        case 'Y': return gesture
        case 'Z': return bound_add(gesture)

def fun_strat(gesture, outcome):
    return bound_add(gesture, (outcome=='Z')-(outcome=='X'))

def generate_scoring():
    """ Return a dict with tuple keys that holds scores for any round outcome
        Keys : (gesture_number, gesture_number)
        Values : key[1] + win_score
        gesture_numbers:
            1: Rock
            2: Paper
            3: Scissors
        win_score:
            0: Lose
            3: Draw
            6: Win key[1]==key[0]+1'
    """
    return {(i, j): j + 6 * (j == bound_add(i)) + 3 * (j == i)
            for i in HAND.values() for j in HAND.values()}

def main():
    scoring = generate_scoring()
    score = 0
    with open("input.txt",'r') as f:
        for line in f:
            rival = HAND[line[0]]
            score += scoring[(rival, strat(rival,line[2]))]
    print(score)

if __name__ == "__main__":
    main()