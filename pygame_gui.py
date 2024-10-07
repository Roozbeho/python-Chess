import tkinter as tk
from PIL import ImageTk, Image
from tkinter import messagebox

import pygame
import pygame.mixer

from chess import *


class PygameGUI:
    def __init__(self):
        pygame.init()
        self.WIDTH = 950
        self.HEIGHT = 530
        self.FPS = 60
        self.window = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Chess Game")
        self.chess = Chess()
        self.current_player = "White"
        self.import_pieces_images()
        self.turn_font = pygame.font.Font('freesansbold.ttf', 25)
        self.move_font = pygame.font.Font('freesansbold.ttf', 12)
        self.letters_font = pygame.font.Font('freesansbold.ttf', 18)
        self.player_choices = []
        self.selected_square = tuple()
        self.player_clicks = []

    def draw_board(self):
        # LIGHT BROWN = #F0D9B5
        # DARK BROWN = #B58863
        for i in range(32):  # BOARD ENDS AT X: 537 Y: 530
            column = i % 4
            row = i // 4
            if row % 2 == 0:
                pygame.draw.rect(self.window, '#B58863', [405 - (column * 125), 30 + row * 62.5, 63.375, 63.375])
            else:
                pygame.draw.rect(self.window, '#B58863', [467 - (column * 125), 30 + row * 62.5, 63.375, 63.375])
        letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
        numbers = ['1', '2', '3', '4', '5', '6', '7', '8']
        for i in range(8):
            pygame.draw.rect(self.window, 'Black', [30 + (i * 62.5), 0, 63.375, 30])
            self.window.blit(self.letters_font.render(letters[i], True, 'White'), (55 + (i * 62.5), 5))
            pygame.draw.rect(self.window, 'Black', [0, 30 + (i * 62.5), 30, 63.375])
            self.window.blit(self.letters_font.render(numbers[i], True, 'White'), (10, 55 + (i * 62.5)))
        pygame.draw.rect(self.window, 'Black', [0, 0, 30, 30])

        # CAPTURED PIECES
        for i in range(8):
            pygame.draw.rect(self.window, 'dark gray', [550, 30 + (i * 28), 26, 26], 1)
            pygame.draw.rect(self.window, 'dark gray', [550, 500 - (i * 28), 26, 26], 1)
            pygame.draw.rect(self.window, 'dark gray', [580, 30 + (i * 28), 26, 26], 1)
            pygame.draw.rect(self.window, 'dark gray', [580, 500 - (i * 28), 26, 26], 1)

        # BG - UTILS
        # pygame.draw.rect(self.window, '#424549', [537, 0, 420,530])
        # USER TURN
        turn = f"{self.current_player}'s Turn"
        self.window.blit(self.turn_font.render(turn, True, 'black'), (700, 20))

        # MOVES
        pygame.draw.rect(self.window, 'dark gray', [650, 100, 120, 300], 1)
        self.window.blit(self.move_font.render('White Moves', True, 'black'), (670, 80))
        pygame.draw.rect(self.window, 'dark gray', [780, 100, 120, 300], 1)
        self.window.blit(self.move_font.render('Black Moves', True, 'black'), (800, 80))
        white_moves = self.chess.chess_set.Board.moves['White']
        black_moves = self.chess.chess_set.Board.moves['Black']
        for counter in range(len(white_moves)):
            move = white_moves[counter]
            self.window.blit(self.move_font.render(move, True, 'Black'), (660, 110 + 25 * counter))
        for counter in range(len(black_moves)):
            move = black_moves[counter]
            self.window.blit(self.move_font.render(move, True, 'Black'), (790, 110 + 25 * counter))

        # SURRENDER
        pygame.draw.rect(self.window, 'dark gray', [670, 440, 80, 30], 3)
        self.window.blit(self.move_font.render('Surrender', True, 'black'), (680, 450))

        # DRAW
        pygame.draw.rect(self.window, 'dark gray', [800, 440, 80, 30], 3)
        self.window.blit(self.move_font.render('Draw', True, 'black'), (825, 450))

    def import_pieces_images(self):
        for row in self.chess.chess_set.Board.board:
            for piece in row:
                if piece:
                    image = 'images/svg-img/' + piece.color + '_' + piece.piece_type + '.svg'
                    piece.image = pygame.image.load(image)
                    piece.image = pygame.transform.scale(piece.image, (43, 43))
                    piece.captured_image = pygame.transform.scale(piece.image, (26, 26))

    def show_capture_pices(self):
        captured = self.chess.chess_set.Board.captured_pieces_gui
        for count, i in enumerate(captured['White']):
            if count < 8:
                self.window.blit(i.captured_image, (550, 30 + (count * 28)))
            else:
                self.window.blit(i.captured_image, (580, 30 + ((count - 8) * 28)))
        for count, i in enumerate(captured['Black']):
            if count < 8:
                self.window.blit(i.captured_image, (550, 500 - (count * 28)))
            else:
                self.window.blit(i.captured_image, (580, 500 - ((count - 8) * 28)))

    def draw_pieces(self):
        for row in self.chess.chess_set.Board.board:
            for piece in row:
                if piece:
                    self.window.blit(piece.image, (piece.position.col * 63.375 + 36, piece.position.row * 63.375 + 37))

    def moves_input(self):
        if 28 <= location[0] <= 530 and 28 <= location[1] <= 530:
            row = int((location[1] - 28) // 63.375)
            col = int((location[0] - 28) // 63.375)
            piece = self.chess.chess_set.Board.board[row][col]
            if piece and piece.color == self.current_player:
                if self.selected_square == (row, col):
                    self.selected_square = tuple()
                    self.player_clicks = []
                else:
                    self.selected_square = (row, col)
                    PygameGUI.play_sound(pygame.mixer.Sound('sounds/premove.mp3'))
                    self.player_clicks.append(Position(row, col))
            elif self.selected_square:
                self.player_clicks.append(Position(row, col))
            if len(self.player_clicks) == 2:
                if not self.chess.check_move_and_is_check(self.player_clicks[0], self.player_clicks[1],
                                                          self.current_player,
                                                          self.chess.chess_set.Board):
                    if self.chess.is_check(self.current_player, self.chess.chess_set.Board):
                        if not self.chess.all_posibble_move(self.current_player, self.chess.chess_set.Board):
                            if self.chess.is_checkmate(self.current_player, self.chess.chess_set.Board):
                                self.current_player = ("Black" if self.current_player == "White" else "White")
                                PygameGUI.play_sound(pygame.mixer.Sound("sounds/game-end.mp3"))
                                messagebox.showinfo('CHECKMATE', f'{self.current_player} HAS WON THE GAME')
                                exit()
                                print('is_checkmate')
                    else:
                        PygameGUI.play_sound(pygame.mixer.Sound("sounds/illegal.mp3"))

                elif self.chess.chess_set.Board.move_piece(self.player_clicks[0], self.player_clicks[1]):
                    self.chess.chess_set.captured_piece()
                    PygameGUI.play_sound(pygame.mixer.Sound("sounds/move-self.mp3"))
                    self.chess.chess_set.Board.moves_logger(self.player_clicks[0], self.player_clicks[1],
                                                            self.current_player)
                    
                    piece = self.chess.chess_set.Board.board[self.player_clicks[1].row][self.player_clicks[1].col]
                    if isinstance(piece, Pawn) and (piece.position.row == 7 or piece.position.row == 0):
                        # CALLS THE PAWN PROMOTION WINDOW
                        self.choose_piece_to_exchange(piece.position.row, piece.position.col)
                    self.current_player = "Black" if self.current_player == "White" else "White"
                    if self.chess.is_check(self.current_player, self.chess.chess_set.Board):
                        if not self.chess.all_posibble_move(
                                self.current_player, self.chess.chess_set.Board):
                            if self.chess.is_checkmate(
                                    self.current_player, self.chess.chess_set.Board):
                                self.current_player = ("Black" if self.current_player == "White" else "White")
                                PygameGUI.play_sound(pygame.mixer.Sound("sounds/game-end.mp3"))
                                messagebox.showinfo('CHECKMATE', f'{self.current_player} HAS WON THE GAME')
                                exit()
                                print('is_checkmate')
                        else:
                            PygameGUI.play_sound(pygame.mixer.Sound("sounds/move-check.mp3"))
                            messagebox.showinfo('CHECK', f'{self.current_player}IS CHECK')
                            print('is_check')

                    elif self.chess.is_draw():
                        print('Draw')
                        messagebox.showerror('DRAW', 'GAME HAS NO WINNER, DRAW !!!')
                        exit()
                else:
                    PygameGUI.play_sound(pygame.mixer.Sound('sounds/illegal.mp3'))
                self.player_clicks = []
                self.selected_square = tuple()

    @staticmethod
    def play_sound(sound):
        pygame.mixer.Sound.play(sound)
        pygame.mixer.music.stop()

    def show_possible_moves(self):
        if self.selected_square:
            piece = self.chess.chess_set.Board.board[self.selected_square[0]][self.selected_square[1]]
            if piece:
                piece_possible_moves = piece.possible_moves()
                if isinstance(piece, King):
                    self.chess.chess_set.Board.validate_castling(Position(piece.position.row, 6), piece.color,
                                                                 piece_possible_moves)
                    self.chess.chess_set.Board.validate_castling(Position(piece.position.row, 2), piece.color,
                                                                 piece_possible_moves)
                for move in piece_possible_moves:
                    if self.chess.check_move_and_is_check(piece.position, move, self.current_player,
                                                          self.chess.chess_set.Board):
                        if self.chess.chess_set.Board.board[move.row][move.col]:
                            pygame.draw.rect(self.window, '#D03136',
                                             [30 + move.col * 62.5, 30 + move.row * 62.5, 63.375, 63.375])
                        else:
                            pygame.draw.rect(self.window, '#DFC272',
                                             [30 + move.col * 62.5, 30 + move.row * 62.5, 63.375, 63.375])
                        pygame.draw.rect(self.window, '#96EB85',
                                         [30 + piece.position.col * 62.5, 30 + piece.position.row * 62.5, 63.375,
                                          63.375])

    def draw_borders(self):

        # DRAW BORDER
        pygame.draw.line(self.window, 'black', (530, 0), (530, 530))
        for i in range(8):
            # DRAW BORDERS
            pygame.draw.line(self.window, 'black', (0, 30 + i * 62.5), (530, 30 + i * 62.5))
            pygame.draw.line(self.window, 'black', (30 + i * 62.5, 0), (30 + i * 62.5, 530))

    def surrender(self):
        if 670 <= location[0] <= 748 and 440 <= location[1] <= 468:
            self.current_player = 'Black' if self.current_player == 'White' else 'White'
            print(f'{self.current_player} has won!')
            messagebox.showinfo('WIN!', f'{self.current_player.upper()} HAS WON THE GAME')
            pygame.quit()

    def request_draw(self):
        # NEEDS POP UP FOR ACCEPTING
        if 801 <= location[0] <= 877 and 443 <= location[1] <= 465:
            msg = messagebox.askquestion('DRAW REQUEST', f'{self.current_player.upper()} HAS OFFERED TO DRAW, ARE AGREE?')
            if msg == 'yes':
                pygame.quit()
            self.current_player = 'Black' if self.current_player == 'White' else 'White'

    def choose_piece_to_exchange(self, row, col):
        piece_list = {0: ('q', 'Queen'), 1: ('n', 'Knight'), 2: ('b', 'Bishop'), 3: ('r', 'Rook')}
        self.piece_list_page = tk.Tk()
        self.piece_list_page.resizable(False, False)
        self.load_pawn_promotion_images()
        self.piece_list_page.geometry('340x80+600+300')
        self.frame = tk.Frame(self.piece_list_page)
        self.frame.grid(row=0, column=0)
        self.piece_list_page.title("Exchange Piece")
        _Buttons = [None, None, None, None]
        for i in range(len(_Buttons)):
            button = tk.Button(self.frame, image=eval(f'self.{self.current_player.lower()}_{piece_list[i][1].lower()}'))
            button.bind('<Button>', self.place_new_piece(row, col, piece_list[i][1], self.piece_list_page))
            button.grid(row=3, column=i + 2)
            _Buttons[i] = button
        self.piece_list_page.mainloop()

    def place_new_piece(self, row, col, user_choose, piece_list_page):
        def inner(event):
            end_pos = Position(row, col)
            # USER ADDED BECEAUSE OF BUG
            user = 'Black' if self.current_player == 'White' else 'White'
            chosen_piece = eval(f"{user_choose}('{self.current_player}', self.chess.chess_set.Board)")
            chosen_piece.image = pygame.image.load(f"images/svg-img/{chosen_piece.color}_{chosen_piece.piece_type}.svg")
            chosen_piece.image = pygame.transform.scale(chosen_piece.image, (43, 43))
            chosen_piece.captured_image = pygame.transform.scale(chosen_piece.image, (26, 26))
            self.chess.chess_set.Board.pawn_exchange(user, end_pos, chosen_piece)
            piece_list_page.destroy()
        return inner

    def load_pawn_promotion_images(self):
        self.black_rook = ImageTk.PhotoImage(Image.open("images/png-img/br_light.png").resize((80, 80)))
        self.white_rook = ImageTk.PhotoImage(Image.open("images/png-img/wr_light.png").resize((80, 80)))
        self.black_bishop =  ImageTk.PhotoImage(Image.open("images/png-img/bb_light.png").resize((80, 80)))
        self.white_bishop =ImageTk.PhotoImage(Image.open("images/png-img/wb_light.png").resize((80, 80)))
        self.black_knight =ImageTk.PhotoImage(Image.open("images/png-img/bn_light.png").resize((80, 80)))
        self.white_knight =ImageTk.PhotoImage(Image.open("images/png-img/wn_light.png").resize((80, 80)))
        self.black_queen =ImageTk.PhotoImage(Image.open("images/png-img/bq_light.png").resize((80, 80)))
        self.white_queen = ImageTk.PhotoImage(Image.open("images/png-img/wq_light.png").resize((80, 80)))


if __name__ == "__main__":
    GUI = PygameGUI()
    status = True
    clock = pygame.time.Clock()
    while status:
        GUI.window.fill('#F0D9B5')
        GUI.draw_board()
        GUI.show_possible_moves()
        GUI.draw_pieces()
        GUI.draw_borders()
        clock.tick(GUI.FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                status = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                location = pygame.mouse.get_pos()
                GUI.moves_input()
                GUI.request_draw()
                GUI.surrender()
        GUI.show_capture_pices()
        pygame.display.flip()
    pygame.quit()
