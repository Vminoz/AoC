def main():
    BUFFER_SIZE = 14
    with open("input.txt", "r") as f:
        series = f.read()
        for i, _ in enumerate(series):
            if len(set(series[i : i + BUFFER_SIZE])) == BUFFER_SIZE:
                print(f"Marker:[{series[i : i + BUFFER_SIZE]}] at {i + BUFFER_SIZE}")
                return


if __name__ == "__main__":
    main()
