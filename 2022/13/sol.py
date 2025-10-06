from packet_class import Packet

def sum_correct_pairs(packets, verbose=False) -> int:
    right_order = 0
    list_iter = iter(packets)
    p1:Packet
    for i, p1 in enumerate(list_iter, start=1):
        p2:Packet = next(list_iter)
        flag = Packet.check_order(p1.contents,p2.contents,verbose)
        if verbose: print(f'→ pkt {i} is {flag}\n')
        if flag:
            right_order += i
    return right_order

def get_decoder_key(packets, dividers) -> int:
    list.sort(packets)
    decoder_key = 1
    for i,p in enumerate(packets, start=1):
        if p in dividers:
            decoder_key *= i
    return decoder_key

def main():
    packets = Packet.from_file("input.txt")

    p1_sol = sum_correct_pairs(packets, True)
    print('P1:', p1_sol)

    dividers = (Packet([[2]]), Packet([[6]]))
    packets.extend(dividers)
    p2_sol = get_decoder_key(packets, dividers)
    print('P2:', p2_sol)

if __name__ == "__main__":
    main()