from typing import Iterator


class Packet:
    def __init__(self, contents: list[int]) -> None:
        self.contents = contents

    def __lt__(self, other) -> bool:
        return self.check_order(self.contents, other.contents) or False

    def __str__(self) -> str:
        return f"P{self.contents}"

    def __repr__(self) -> str:
        return f"Packet: {self.contents}"

    @staticmethod
    def _check_int_int(left, right, verb):
        if left < right:
            if verb:
                print("L smaller")
            return True
        if left > right:
            if verb:
                print("L larger")
            return False

    @classmethod
    def _check_list_list(cls, left, right, verb) -> bool | None:
        if not right:
            if not left:
                return
            if verb:
                print("R ran out (empty)")
            return False
        len_left, len_right = len(left), len(right)
        for i in range(len_left):
            if i == len_right:
                if verb:
                    print("R ran out")
                return False
            flag = cls.check_order(left[i], right[i], verb)
            if flag is not None:
                return flag
        return True

    @classmethod
    def check_order(cls, left, right, verb=False) -> bool | None:
        if verb:
            print(f"Comparing: {left} to {right}")
        if isinstance(left, int) and isinstance(right, int):
            return cls._check_int_int(left, right, verb)
        if isinstance(left, list) and isinstance(right, list):
            return cls._check_list_list(left, right, verb)
        if isinstance(left, int):
            return cls.check_order([left], right, verb)
        if isinstance(right, int):
            return cls.check_order(left, [right], verb)
        raise TypeError(f"Tried checking a {type(left)} against a {type(right)}")

    @classmethod
    def from_file(cls, file_name) -> list:
        packets = []
        with open(file_name) as f:
            for line in f:
                if line := line.rstrip():
                    packets.append(Packet(cls._read_list_nest(iter(line[1:-1]))))
        return packets

    @classmethod
    def _read_list_nest(cls, ln_iter: Iterator[str]) -> list[int]:
        pkt = []
        num = ""
        for ch in ln_iter:
            if ch == "[":
                pkt.append(cls._read_list_nest(ln_iter))
            if ch == "]":
                break
            if ch.isdigit():
                num += ch
            if ch == "," and len(num) > 0:
                pkt.append(int(num))
                num = ""
        if num:
            pkt.append(int(num))
        return pkt
