import pygame
import chess


class GameWindow:
    """Gerencia a janela, o tabuleiro e a movimentação das peças."""

    WIDTH = 800
    HEIGHT = 800
    TITLE = "ChessPy"
    SPRITE_SIZE = (90, 90)
    FPS = 60

    LIGHT_SQUARE = (194, 214, 215)
    DARK_SQUARE = (78, 93, 127)

    SELECTED_COLOR = (255, 215, 0)
    MOVE_COLOR = (60, 190, 100)
    CAPTURE_COLOR = (220, 75, 75)

    ANIMATION_DURATION = 160

    def __init__(self) -> None:
        pygame.init()

        self.screen = pygame.display.set_mode(
            (self.WIDTH, self.HEIGHT)
        )
        pygame.display.set_caption(self.TITLE)

        self.clock = pygame.time.Clock()
        self.board = chess.Board()

        # Fontes
        self.font = pygame.font.SysFont(
            "Arial",
            48,
            bold=True,
        )

        self.coordinate_font = pygame.font.SysFont(
            "Arial",
            16,
            bold=True,
        )

        self.checkmate_font = pygame.font.SysFont(
            "Arial",
            30,
            bold=True,
        )

        # Sprites
        self.black_sprites = self.load_sprites()
        self.white_sprites = self.load_sprites("white")

        self.running = True

        # Seleção e movimentação
        self.selected_square = None
        self.dragging = False
        self.drag_position = None
        self.drag_start_position = None

        # Animação
        self.animation = None

        # Último movimento
        self.last_move = None

        # Estado da partida
        self.game_over = False

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

    def get_square_from_position(self, position):
        """Converte a posição do mouse em uma casa do xadrez."""

        mouse_x, mouse_y = position
        square_size = self.WIDTH // 8

        col = mouse_x // square_size
        row = mouse_y // square_size

        if not (0 <= col < 8 and 0 <= row < 8):
            return None

        return chess.square(col, 7 - row)

    def get_square_center(self, square):
        """Retorna o centro visual de uma casa."""

        square_size = self.WIDTH // 8

        col = chess.square_file(square)
        row = 7 - chess.square_rank(square)

        return (
            col * square_size + square_size // 2,
            row * square_size + square_size // 2,
        )

    def get_legal_destinations(self, square: int) -> list[int]:
        """Retorna os destinos legais de uma peça."""

        return [
            move.to_square
            for move in self.board.legal_moves
            if move.from_square == square
        ]

    def get_sprite(self, piece):
        """Retorna o sprite correspondente à peça."""

        if piece.color == chess.WHITE:
            return self.white_sprites[piece.piece_type]

        return self.black_sprites[piece.piece_type]

    def start_animation(self, move, moving_piece):
        """Inicia a animação de um movimento válido."""

        start_position = self.get_square_center(
            move.from_square
        )

        end_position = self.get_square_center(
            move.to_square
        )

        self.animation = {
            "image": self.get_sprite(moving_piece),
            "start": start_position,
            "end": end_position,
            "target_square": move.to_square,
            "start_time": pygame.time.get_ticks(),
            "duration": self.ANIMATION_DURATION,
        }

    def make_move(
        self,
        from_square: int,
        to_square: int,
        animate: bool = True,
    ) -> bool:
        """Executa um movimento se ele for legal."""

        # Impede movimentos após o fim da partida.
        if self.game_over:
            return False

        moving_piece = self.board.piece_at(from_square)

        if moving_piece is None:
            return False

        move = chess.Move(from_square, to_square)

        # Trata a promoção do peão para Rainha.
        if (
            moving_piece.piece_type == chess.PAWN
            and chess.square_rank(to_square) in (0, 7)
        ):
            move = chess.Move(
                from_square,
                to_square,
                promotion=chess.QUEEN,
            )

        if move not in self.board.legal_moves:
            return False

        self.last_move = move

        # Inicia a animação antes de atualizar o estado do tabuleiro.
        if animate:
            self.start_animation(move, moving_piece)

        self.board.push(move)

        # Verifica se o movimento terminou a partida.
        if self.board.is_checkmate():
            self.game_over = True

        self.selected_square = None
        self.dragging = False
        self.drag_position = None
        self.drag_start_position = None

        return True

    def handle_mouse_down(self, event):
        """Processa o início de um clique ou arraste."""

        if self.game_over or self.animation is not None:
            return

        square = self.get_square_from_position(event.pos)

        if square is None:
            return

        piece = self.board.piece_at(square)

        if self.selected_square is not None:
            if square in self.get_legal_destinations(
                self.selected_square
            ):
                self.make_move(self.selected_square, square)
                return

        if piece is not None and piece.color == self.board.turn:
            self.selected_square = square
            self.dragging = True
            self.drag_position = event.pos
            self.drag_start_position = square

        else:
            self.selected_square = None
            self.dragging = False
            self.drag_position = None
            self.drag_start_position = None

    def handle_mouse_motion(self, event):
        """Atualiza a posição da peça durante o arraste."""

        if self.game_over:
            return

        if self.dragging:
            self.drag_position = event.pos

    def handle_mouse_up(self, event):
        """Finaliza o arraste e valida o destino."""

        if self.game_over or not self.dragging:
            return

        destination = self.get_square_from_position(event.pos)
        origin = self.drag_start_position

        self.dragging = False

        if destination is not None and destination != origin:
            if self.make_move(origin, destination, animate=False):
                return

        self.drag_position = None
        self.selected_square = origin if destination == origin else None

    def handle_events(self) -> None:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                self.running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.handle_mouse_down(event)

            elif event.type == pygame.MOUSEMOTION:
                self.handle_mouse_motion(event)

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.handle_mouse_up(event)

    def get_king_in_check(self):
        """Retorna a casa do rei que está em xeque."""

        if not self.board.is_check():
            return None

        king_color = self.board.turn

        return self.board.king(king_color)

    def get_checkmate_kings(self):
        """Retorna as casas dos reis vencedor e derrotado."""

        if not self.board.is_checkmate():
            return None

        losing_king = self.board.king(self.board.turn)
        winning_king = self.board.king(not self.board.turn)

        return winning_king, losing_king

    def draw_board(self) -> None:
        square_size = self.WIDTH // 8

        destinations = []

        if self.selected_square is not None and not self.game_over:
            destinations = self.get_legal_destinations(
                self.selected_square
            )

        king_in_check = self.get_king_in_check()
        checkmate_kings = self.get_checkmate_kings()

        # Casas do último movimento
        last_move_squares = []

        if self.last_move is not None:
            last_move_squares = [
                self.last_move.from_square,
                self.last_move.to_square,
            ]

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

                current_square = chess.square(col, 7 - row)

                # Destaque do último movimento
                if current_square in last_move_squares:
                    highlight = pygame.Surface(
                        (square_size, square_size),
                        pygame.SRCALPHA,
                    )
                    highlight.fill((255, 220, 80, 85))

                    self.screen.blit(
                        highlight,
                        (col * square_size, row * square_size),
                    )

                # Destaque vermelho do xeque
                if current_square == king_in_check:
                    check_highlight = pygame.Surface(
                        (square_size, square_size),
                        pygame.SRCALPHA,
                    )
                    check_highlight.fill((220, 40, 40, 130))

                    self.screen.blit(
                        check_highlight,
                        (col * square_size, row * square_size),
                    )

                # Destaque verde do rei vencedor no xeque-mate
                if checkmate_kings is not None:
                    winning_king, losing_king = checkmate_kings

                    if current_square == winning_king:
                        checkmate_highlight = pygame.Surface(
                            (square_size, square_size),
                            pygame.SRCALPHA,
                        )
                        checkmate_highlight.fill((40, 190, 80, 150))

                        self.screen.blit(
                            checkmate_highlight,
                            (col * square_size, row * square_size),
                        )

                # Destaque da peça selecionada
                if self.selected_square is not None and not self.game_over:
                    selected_col = chess.square_file(
                        self.selected_square
                    )
                    selected_row = 7 - chess.square_rank(
                        self.selected_square
                    )

                    if row == selected_row and col == selected_col:
                        pygame.draw.rect(
                            self.screen,
                            self.SELECTED_COLOR,
                            (
                                col * square_size,
                                row * square_size,
                                square_size,
                                square_size,
                            ),
                            4,
                        )

        # Desenha os destinos legais
        for destination in destinations:
            center = self.get_square_center(destination)

            target_piece = self.board.piece_at(destination)

            dest_col = chess.square_file(destination)
            dest_row = 7 - chess.square_rank(destination)

            square_color = (
                self.LIGHT_SQUARE
                if (dest_row + dest_col) % 2 == 0
                else self.DARK_SQUARE
            )

            # Escurece a cor original da casa
            darker_color = tuple(
                max(0, channel - 45)
                for channel in square_color
            )

            if target_piece is None:
                pygame.draw.circle(
                    self.screen,
                    darker_color,
                    center,
                    13,
                )
            else:
                pygame.draw.circle(
                    self.screen,
                    darker_color,
                    center,
                    36,
                    5,
                )

    def draw_coordinates(self) -> None:
        square_size = self.WIDTH // 8

        for row in range(8):
            for col in range(8):

                square_color = (
                    self.LIGHT_SQUARE
                    if (row + col) % 2 == 0
                    else self.DARK_SQUARE
                )

                text_color = (
                    self.DARK_SQUARE
                    if square_color == self.LIGHT_SQUARE
                    else self.LIGHT_SQUARE
                )

                # Letras: a até h
                if row == 7:
                    letter = chr(ord("a") + col)

                    text = self.coordinate_font.render(
                        letter,
                        True,
                        text_color,
                    )

                    self.screen.blit(
                        text,
                        (
                            col * square_size + 5,
                            (row + 1) * square_size - 22,
                        ),
                    )

                # Números: 8 até 1
                if col == 0:
                    number = str(8 - row)

                    text = self.coordinate_font.render(
                        number,
                        True,
                        text_color,
                    )

                    self.screen.blit(
                        text,
                        (
                            5,
                            row * square_size + 5,
                        ),
                    )

    def draw_pieces(self) -> None:
        for square in chess.SQUARES:

            piece = self.board.piece_at(square)

            if piece is None:
                continue

            # Não desenha a peça na posição original
            # enquanto ela estiver sendo arrastada.
            if self.dragging and square == self.selected_square:
                continue

            # Não desenha a peça na posição final
            # durante sua animação.
            if (
                self.animation is not None
                and square == self.animation_square()
            ):
                continue

            image = self.get_sprite(piece)

            center_x, center_y = self.get_square_center(square)

            # Ajuste vertical do peão.
            if piece.piece_type == chess.PAWN:
                center_y += 6

            rect = image.get_rect(
                center=(center_x, center_y)
            )

            self.screen.blit(image, rect)

    def animation_square(self):
        """Retorna a casa de destino da animação."""

        if self.animation is None:
            return None

        return self.animation.get("target_square")

    def draw_dragged_piece(self):
        """Desenha a peça acompanhando o mouse."""

        if not self.dragging or self.selected_square is None:
            return

        piece = self.board.piece_at(self.selected_square)

        if piece is None:
            return

        image = self.get_sprite(piece)

        image = pygame.transform.scale(
            image,
            (115, 115),
        )

        # Pequeno deslocamento para dar sensação de suspensão.
        position = (
            self.drag_position[0],
            self.drag_position[1] - 12,
        )

        rect = image.get_rect(center=position)

        self.screen.blit(image, rect)

    def draw_animation(self):
        """Desenha o movimento de forma suave."""

        if self.animation is None:
            return

        current_time = pygame.time.get_ticks()

        elapsed = (
            current_time - self.animation["start_time"]
        )

        progress = min(
            elapsed / self.animation["duration"],
            1.0,
        )

        # Suavização da animação.
        smooth_progress = (
            progress * progress * (3 - 2 * progress)
        )

        start_x, start_y = self.animation["start"]
        end_x, end_y = self.animation["end"]

        current_x = start_x + (
            end_x - start_x
        ) * smooth_progress

        current_y = start_y + (
            end_y - start_y
        ) * smooth_progress

        image = self.animation["image"]

        rect = image.get_rect(
            center=(int(current_x), int(current_y))
        )

        self.screen.blit(image, rect)

        if progress >= 1.0:
            self.animation = None

    def draw_checkmate_marker(self):
        """Desenha o símbolo # sobre o rei derrotado."""

        checkmate_kings = self.get_checkmate_kings()

        if checkmate_kings is None:
            return

        winning_king, losing_king = checkmate_kings

        center_x, center_y = self.get_square_center(losing_king)

        # Posiciona o símbolo próximo ao canto superior direito do rei.
        marker_position = (
            center_x + 22,
            center_y - 22,
        )

        marker_shadow = self.checkmate_font.render(
            "#",
            True,
            (20, 20, 20),
        )

        marker = self.checkmate_font.render(
            "#",
            True,
            (255, 255, 255),
        )

        shadow_rect = marker_shadow.get_rect(
            center=(
                marker_position[0] + 2,
                marker_position[1] + 2,
            )
        )

        marker_rect = marker.get_rect(
            center=marker_position
        )

        self.screen.blit(marker_shadow, shadow_rect)
        self.screen.blit(marker, marker_rect)

    def update(self) -> None:
        self.draw_board()
        self.draw_pieces()
        self.draw_dragged_piece()
        self.draw_animation()
        self.draw_coordinates()
        self.draw_checkmate_marker()

        pygame.display.flip()

        self.clock.tick(self.FPS)

    def close(self) -> None:
        pygame.quit()