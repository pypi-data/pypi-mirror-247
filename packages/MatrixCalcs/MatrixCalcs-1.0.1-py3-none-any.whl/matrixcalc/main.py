from matrixcalc.app import App


def main():
    app = App()
    print("\n")
    print("Use < help > command to have more information.")
    while True:
        app.main_loop()


if __name__ == "__main__":
    main()

