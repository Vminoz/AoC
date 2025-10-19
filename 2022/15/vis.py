from matplotlib import pyplot as plt
from sensor_class import parse_sensors


def main():
    sensors = parse_sensors("in.txt")
    coverage = set()
    deadzone = set()
    for s in sensors:
        print(s)
        coverage |= s.inside
        deadzone |= s.outside
    deadzone -= coverage
    plt.scatter(*zip(*coverage), marker="s")
    plt.scatter(*zip(*deadzone), marker="s", c="r")
    plt.axis("equal")
    plt.show()


if __name__ == "__main__":
    main()
