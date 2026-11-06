import pygame
import chess


class GameWindow:
    """Gerencia a janela principal e desenha o tabuleiro."""

    WIDTH = 800
    HEIGHT = 800
    TITLE = "ChessPy"
    SPRITE_SIZE = (100, 100)

    LIGHT_SQUARE = (194, 214, 215)
    DARK_SQUARE = (78, 93, 127)

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
        self.black_sprites = self.load_sprites()
        self.white_sprites = self.load_sprites("white")
        self.running = True

    
    def load_sprites(self, color: str = "black") -> dict:
        sprite_path = f"assets/sprites/{color}/"

        sprites = {
            chess.KING: "Rei.png",
            chess.QUEEN: "Rainha.png",
            chess.ROOK: "Torre.png",
            chess.BISHOP: "Bispo.png",
            chess.KNIGHT: "Cavalo.png",
            chess.PAWN: "Peao.png",
        }

        loaded_sprites = {}

        for piece_type, filename in sprites.items():
            image = pygame.image.load(
                sprite_path + filename
            ).convert_alpha()

            image = pygame.transform.scale(
                image,
                self.SPRITE_SIZE,
            )

            loaded_sprites[piece_type] = image

        return loaded_sprites


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

            if piece.color == chess.BLACK:
                image = self.black_sprites[piece.piece_type]
            else:
                image = self.white_sprites[piece.piece_type]

            rect = image.get_rect(
                center=(
                    col * square_size + square_size // 2,
                    row * square_size + square_size // 2,
                )
            )

            self.screen.blit(image, rect)


    def update(self) -> None:
        self.draw_board()
        self.draw_pieces()
        pygame.display.flip()
        self.clock.tick(60)

    def close(self) -> None:
        pygame.quit()
