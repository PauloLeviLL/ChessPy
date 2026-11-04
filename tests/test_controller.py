from chesspy.controller.game_controller import GameController


def test_controller_initial_state():
    game = GameController()

    assert game.get_turn() == "white"
    assert len(game.get_legal_moves()) == 20


def test_controller_play():
    game = GameController()

    assert game.play("e2e4")
    assert game.get_turn() == "black"


def test_controller_undo():
    game = GameController()

    game.play("e2e4")

    assert game.undo()
    assert game.get_turn() == "white"


def test_controller_restart():
    game = GameController()

    game.play("e2e4")
    game.restart()

    assert game.get_turn() == "white"
    assert len(game.get_legal_moves()) == 20
