def main():
    line = input()
    for i in range(14-1, len(line)):
        chars = line[i-(14-1):i+1]
        if len(set(chars)) == 14:
            print(i + 1)  # counting from 1
            return

if __name__ == "__main__":
    main()
