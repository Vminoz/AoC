class IntIntervallist:
    def __init__(self) -> None:
        self._ilist = []

    def __in__(self, value) -> bool:
        return any(interval[0] <= value <= interval[1] for interval in self._ilist)

    def __str__(self) -> str:
        if self._ilist:
            return " | ".join(f"{s:_} ~ {e:_}" for s, e in self._ilist)
        else:
            return "[~]"

    def __getitem__(self, i) -> list[int]:
        return self._ilist[i]

    def __len__(self) -> int:
        return len(self._ilist)

    def merge(self, new_interv: list[int]) -> None:
        """Assumes intervals list is sorted"""
        if not self._ilist:
            self._ilist.append(new_interv)
            return
        for i, iv in enumerate(self._ilist):
            if new_interv[0] > iv[1]:  # above
                continue
            if new_interv[1] < iv[0]:  # below, assumes sorted
                self._ilist.insert(i, new_interv)
            else:
                iv[0] = min(iv[0], new_interv[0])
                iv[1] = max(iv[1], new_interv[1])
                if i + 1 < len(self._ilist) and iv[1] >= self._ilist[i + 1][0]:
                    break
            return
        else:
            self._ilist.append(new_interv)
            return

        # break-ed, spicy stuff
        self.merge(self._ilist.pop(i))

    def sum(self):
        return sum(1 + end - start for start, end in self._ilist)

    def split(self, value: int):
        for i, iv in enumerate(self._ilist):
            if value > iv[1]:
                continue  # check next
            if value < iv[0]:
                return  # passed
            if value == iv[0]:
                if value == iv[1]:  # interval is singular
                    self._ilist.pop(i)
                    return
                iv[0] += 1
                return
            if value == iv[1]:
                iv[1] -= 1
                return
            left = [iv[0], value - 1]
            iv[0] = value + 1
            self._ilist.insert(i, left)
            return

    def bind(self, lb, ub) -> None:
        new_ilist = []
        for iv in self._ilist:
            if iv[1] < lb:
                continue
            if iv[0] > ub:
                continue
            new_ilist.append([max(iv[0], lb), min(iv[1], ub)])
        self._ilist = new_ilist
