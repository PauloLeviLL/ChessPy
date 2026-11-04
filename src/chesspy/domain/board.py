import chess


class ChessBoard:
    """Representa o tabuleiro e controla as regras básicas do xadrez."""

    def __init__(self) -> None:
        self._board = chess.Board()

    @property
    def board(self) -> chess.Board:
        """Retorna o estado atual do tabuleiro."""
        return self._board

    def get_fen(self) -> str:
        """Retorna a posição atual no formato FEN."""
        return self._board.fen()

    def get_turn(self) -> str:
        """Retorna a cor que deve jogar."""
        return "white" if self._board.turn == chess.WHITE else "black"

    def get_legal_moves(self) -> list[str]:
        """Retorna os movimentos legais em notação UCI."""
        return [move.uci() for move in self._board.legal_moves]

    def make_move(self, uci_move: str) -> bool:
        """Executa um movimento legal informado em UCI."""
        try:
            move = chess.Move.from_uci(uci_move)
        except ValueError:
            return False

        if move not in self._board.legal_moves:
            return False

        self._board.push(move)
        return True

    def undo_move(self) -> bool:
        """Desfaz o último movimento, se existir."""
        if not self._board.move_stack:
            return False

        self._board.pop()
        return True

    def reset(self) -> None:
        """Restaura o tabuleiro para a posição inicial."""
        self._board.reset()

    
    def test_castling():
        import chess

        board = ChessBoard()
        board.board.set_fen("r3k2r/8/8/8/8/8/8/R3K2R w KQkq - 0 1")

        assert board.make_move("e1g1")
        assert board.board.piece_at(chess.G1) == chess.Piece(chess.KING, chess.WHITE)
        assert board.board.piece_at(chess.F1) == chess.Piece(chess.ROOK, chess.WHITE)


    def test_en_passant():
        import chess

        board = ChessBoard()
        board.board.set_fen("8/8/8/3pP3/8/8/8/K6k w - d6 0 1")

        assert board.make_move("e5d6")
        assert board.board.piece_at(chess.D6) == chess.Piece(chess.PAWN, chess.WHITE)
        assert board.board.piece_at(chess.D5) is None


    def test_promotion():
        import chess

        board = ChessBoard()
        board.board.set_fen("7k/P7/8/8/8/8/8/7K w - - 0 1")

        assert board.make_move("a7a8q")
        assert board.board.piece_at(chess.A8) == chess.Piece(chess.QUEEN, chess.WHITE)
