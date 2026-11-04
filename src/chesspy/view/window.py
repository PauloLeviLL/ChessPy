import pygame
import chess


class GameWindow:
    """Gerencia a janela principal e desenha o tabuleiro."""

    WIDTH = 800
    HEIGHT = 800
    TITLE = "ChessPy"

    LIGHT_SQUARE = (240, 217, 181)
    DARK_SQUARE = (181, 136, 99)

    PIECE_SYMBOLS = {
        chess.PAWN: "P",
        chess.KNIGHT: "N",
        chess.BISHOP: "B",
        chess.ROOK: "R",
        chess.QUEEN: "Q",
        chess.KING: "K",
    }

    def __init__(self) -> None:
        pygame.init()

        self.screen = pygame.display.set_mode(
            (self.WIDTH, self.HEIGHT)
        )
        pygame.display.set_caption(self.TITLE)

        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 48, bold=True)
        self.board = chess.Board()
        self.running = True

    def handle_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def draw_board(self) -> None:
        square_size = self.WIDTH // 8

        for row in range(8):
            for col in range(8):
                color = (
                    self.LIGHT_SQUARE
                    if (row + col) % 2 == 0
                    else self.DARK_SQUARE
                )

                pygame.draw.rect(
                    self.screen,
                    color,
                    (
                        col * square_size,
                        row * square_size,
                        square_size,
                        square_size,
                    ),
                )

    def draw_pieces(self) -> None:
        square_size = self.WIDTH // 8

        for square in chess.SQUARES:
            piece = self.board.piece_at(square)

            if piece is None:
                continue

            col = chess.square_file(square)
            row = 7 - chess.square_rank(square)

            symbol = self.PIECE_SYMBOLS[piece.piece_type]

            color = (
                (255, 255, 255)
                if piece.color == chess.WHITE
                else (30, 30, 30)
            )

            text = self.font.render(symbol, True, color)

            rect = text.get_rect(
                center=(
                    col * square_size + square_size // 2,
                    row * square_size + square_size // 2,
                )
            )

            self.screen.blit(text, rect)

    def update(self) -> None:
        self.draw_board()
        self.draw_pieces()
        pygame.display.flip()
        self.clock.tick(60)

    def close(self) -> None:
        pygame.quit()
