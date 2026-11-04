from chesspy.domain.board import ChessBoard


def test_initial_board():
    board = ChessBoard()

    assert board.get_turn() == "white"
    assert len(board.get_legal_moves()) == 20


def test_make_legal_move():
    board = ChessBoard()

    assert board.make_move("e2e4")
    assert board.get_turn() == "black"


def test_reject_illegal_move():
    board = ChessBoard()

    assert not board.make_move("e2e5")
    assert board.get_turn() == "white"


def test_undo_move():
    board = ChessBoard()

    board.make_move("e2e4")

    assert board.undo_move()
    assert board.get_turn() == "white"


def test_reset_board():
    board = ChessBoard()

    board.make_move("e2e4")
    board.reset()

    assert board.get_turn() == "white"
    assert len(board.get_legal_moves()) == 20
