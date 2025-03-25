from discord_bot import initialize_bot


def main():
    with open("../token.txt", "r") as f:
        token = f.readlines()[0]
    initialize_bot(token=token, prefix='~')


if __name__ == "__main__":
    main()
