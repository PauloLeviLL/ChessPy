from chesspy.view.window import GameWindow


def main() -> None:
    window = GameWindow()

    while window.running:
        window.handle_events()
        window.update()

    window.close()


if __name__ == "__main__":
    main()
