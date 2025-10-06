from sensor_class import parse_sensors, Sensor
from intintervals_class import IntIntervallist

def scan_y(sensors:set[Sensor], y_coord:int, verb=False, bounds=None):
    intervals = IntIntervallist()
    beacons = set()
    for sensor in sensors:
        if verb: print('looking at sensor',sensor)
        if interv := sensor.get_x_interval(y_coord):
            if verb: print(f'Merge {interv} into\n{intervals}')
            intervals.merge(interv)
            if verb: print('→',intervals)
        if sensor.by == y_coord:
            beacons.add(sensor.by)
    if bounds is not None:
        intervals.bind(*bounds)
        if verb: print(f'Bound intervals:\n{intervals}')
    else:
        for b in beacons:
            if verb: print('Splitting at', b, 'due to beacon.')
            intervals.split(b)
    return intervals

def dead_cell(sensors:set[Sensor], lb=0, ub=4_000_000, verb = False) -> tuple[int,int]:
    for y in range(lb, ub+1):
        scan = scan_y(sensors, y, False, (lb, ub))
        if verb and not y % 100000: print(f'{y=} → {scan}', end = '\r')
        if scan[0] != [lb, ub]:
            if verb: print(f'Found something interesting! {y=} → {scan}')
            if scan[0][0] == lb+1:
                return lb, y
            if scan[0][1] == ub-1:
                return ub, y
            if len(scan) == 2 and scan[0][1] +2 == scan[1][0]:
                return scan[0][1]+1, y
            raise ValueError(f'position not unique, got {scan}')
    raise ValueError(f'no free position found within [{lb},{ub}]')

def main():
    INPUTS = {'s': ('in.txt', 10, 20),
              'h': ('input.txt', 2_000_000, 4_000_000)}
    MODE = 'h'

    sensors = parse_sensors(INPUTS[MODE][0])
    p1_sol = scan_y(sensors, INPUTS[MODE][1], True)
    print('P1:', p1_sol.sum(),end='\n'+'#'*120+'\n')

    missing_beacon = dead_cell(sensors, 0, INPUTS[MODE][2], verb=True)
    print('P2:', missing_beacon[0]*4_000_000 + missing_beacon[1])


if __name__ == "__main__":
    main()