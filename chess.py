class Position:
    def __init__(self, row, col):
        self.row = row
        self.col = col

    def match(self, list_pos):
        pass

    def __str__(self):
        return f'{self.row}, {self.col}'


class Piece:
    # chess = Chess()

    def __init__(self, color, board, position=None):
        self.color = color
        self.board = board
        self.has_moved = False
        self.position = position

    def possible_moves(self):
        pass

    def move(self, end_pos):
        # chess = Chess()
        for i in self.possible_moves():
            if end_pos.row == i.row and end_pos.col == i.col:
                return True
        return False

    def __str__(self):
        pass

    def possible_moves_loop(self, offsets, moves):  # PREVENTS DUPLICATED CODE FOR POSSIBLE MOVES
        # chess = Chess()
        for dr, dc in offsets:
            new_pos = Position(self.position.row + dr, self.position.col + dc)
            if self.board.is_inside_board(new_pos) and (
                    self.board.is_square_empty(new_pos) or self.board.is_enemy_piece(new_pos, self.color)):
                # if chess.check_move_and_is_check(self.position, new_pos, self.color, self.board):
                moves.append(new_pos)


class King(Piece):
    def __init__(self, color, board, position=None):
        super().__init__(color, board, position)
        self.piece_type = "king"

    def possible_moves(self):
        moves = []
        offsets = [(1, 0), (0, 1), (-1, 0), (0, -1),
                   (1, 1), (-1, 1), (1, -1), (-1, -1)]
        self.possible_moves_loop(offsets, moves)
        # Castling
        if not self.board.board[self.position.row][self.position.col].has_moved:
            # Check king_side castling
            if self.board.board[self.position.row][7] and not self.board.board[self.position.row][7].has_moved:
                if all(self.board.is_square_empty(Position(self.position.row, c)) for c in
                       range(self.position.col + 1, 7)):
                    moves.append(Position(self.position.row, self.position.col + 2))
            # Check queen_side castling
            if self.board.board[self.position.row][0] and not self.board.board[self.position.row][0].has_moved:
                if all(self.board.is_square_empty(Position(self.position.row, c)) for c in range(1, self.position.col)):
                    moves.append(Position(self.position.row, self.position.col - 2))
        return moves

    def castling(self):
        moves = {'left': None, 'right': None}
        if not self.board.board[self.position.row][self.position.col].has_moved:
            # Check king_side castling
            if self.board.board[self.position.row][7] and not self.board.board[self.position.row][7].has_moved:
                if all(self.board.is_square_empty(Position(self.position.row, c)) for c in
                       range(self.position.col + 1, 7)):
                    moves['right'] = Position(self.position.row, self.position.col + 2)
            # Check queen_side castling
            if self.board.board[self.position.row][0] and not self.board.board[self.position.row][0].has_moved:
                if all(self.board.is_square_empty(Position(self.position.row, c)) for c in range(1, self.position.col)):
                    moves['left'] = Position(self.position.row, self.position.col - 2)
        return moves

    def __str__(self):
        if self.color == "White":
            return "K"
        return "k"


class Bishop(Piece):

    def __init__(self, color, board, position=None):
        super().__init__(color, board, position)
        self.piece_type = "bishop"

    def possible_moves(self):
        moves = []
        offsets = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
        # chess = Chess()
        for number, ofs in enumerate(offsets):
            dr, dc = ofs[0], ofs[1]
            for i in range(6):
                new_pos = Position(
                    self.position.row + dr + i if number <= 1 else self.position.row + dr - i,
                    self.position.col + dc + i if (number == 0 or number == 2) else self.position.col + dc - i)
                if self.board.is_inside_board(new_pos) and (
                        self.board.is_square_empty(new_pos) or self.board.is_enemy_piece(new_pos, self.color)):
                    # if chess.check_move_and_is_check(self.position, new_pos, self.color, self.board):
                    moves.append(new_pos)
                if self.board.is_inside_board(new_pos) and not self.board.is_square_empty(new_pos):
                    break
        return moves

    def __str__(self):
        if self.color == "White":
            return "B"
        return "b"


class Pawn(Piece):
    def __init__(self, color, board, position=None):
        super().__init__(color, board, position)
        # self.has_moved = 0
        self.move_count = 0
        self.first_move_2_blocks = False
        self.piece_type = "pawn"

    def possible_moves(self):
        moves = []
        direction = 1 if self.color == "White" else -1
        direction2 = 2 if self.color == "White" else -2

        # start_row = 1 if self.color == "White" else 6

        if self.color == "White":
            offsets = [(1, 1), (1, -1)]
            new_pos = Position(self.position.row + direction, self.position.col)
            if self.board.is_inside_board(new_pos) and self.board.is_square_empty(new_pos):
                moves.append(new_pos)
            if self.position.row == 1:
                new_pos = Position(self.position.row + direction2, self.position.col)
                if self.board.is_inside_board(new_pos) and self.board.is_square_empty(new_pos) and self.board.board[self.position.row +1][self.position.col] is None:
                    moves.append(new_pos)
            for dr, dc in offsets:
                new_pos1 = Position(self.position.row + dr, self.position.col + dc)
                if (
                        self.board.is_inside_board(new_pos1)
                        and (not self.board.is_square_empty(new_pos1))
                        and self.board.is_enemy_piece(new_pos1, self.color)
                ):
                    moves.append(new_pos1)
        else:
            offsets = [(-1, 1), (-1, -1)]
            new_pos = Position(self.position.row + direction, self.position.col)
            if self.board.is_inside_board(new_pos) and self.board.is_square_empty(new_pos):
                moves.append(new_pos)
            if self.position.row == 6:
                new_pos = Position(self.position.row + direction2, self.position.col)
                if self.board.is_inside_board(new_pos) and self.board.is_square_empty(new_pos) and self.board.board[self.position.row -1][self.position.col] is None:
                    moves.append(new_pos)
            for dr, dc in offsets:
                new_pos1 = Position(self.position.row + dr, self.position.col + dc)
                if (
                        self.board.is_inside_board(new_pos1)
                        and (not self.board.is_square_empty(new_pos1))
                        and self.board.is_enemy_piece(new_pos1, self.color)
                ):
                    moves.append(new_pos1)
        # TODO
        self.en_passant(moves)
        return moves

    def en_passant(self, moves):
        if (self.position.row == 4 and self.color == "White") or (self.position.row == 3 and self.color == "Black"):
            white_offsets = [(1, -1), (1, 1)]
            black_offsets = [(-1, 1), (-1, -1)]
            for dr, dc in eval(f"{self.color.lower()}_offsets"):
                enemy_pos = Position(self.position.row, self.position.col + dc)
                new_pos = Position(self.position.row + dr, self.position.col + dc)
                try:  # IF ENEMY PIECE IS NOT PAWN OR IS NONE
                    enemy = self.board.board[enemy_pos.row][enemy_pos.col]
                    if self.board.is_enemy_piece(enemy_pos, self.color):
                        if enemy.first_move_2_blocks and enemy.move_count == 1:
                            if self.board.is_inside_board(new_pos) and self.board.is_square_empty(
                                    new_pos) and not self.board.is_enemy_piece(new_pos, self.color):
                                moves.append(new_pos)
                        else:
                            pass
                except (AttributeError, NameError, IndexError):
                    continue
        return moves

    def __str__(self):
        if self.color == "White":
            return "P"
        return "p"


class Rook(Piece):
    def __init__(self, color, board, position=None):
        super().__init__(color, board, position)
        self.piece_type = "rook"

    def possible_moves(self):
        moves = []
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        # chess = Chess()
        for number, ofs in enumerate(directions):
            dr, dc = ofs[0], ofs[1]
            for i in range(7):
                if number <= 1:
                    new_pos = Position(self.position.row + dr + i if number == 0 else self.position.row + dr - i,
                                       self.position.col)
                    if self.board.is_inside_board(new_pos) and (
                            self.board.is_square_empty(new_pos) or self.board.is_enemy_piece(new_pos, self.color)):
                        # if chess.check_move_and_is_check(self.position, new_pos, self.color, self.board):
                        moves.append(new_pos)
                else:
                    new_pos = Position(self.position.row,
                                       self.position.col + dc + i if number == 2 else self.position.col + dc - i)
                    if self.board.is_inside_board(new_pos) and (
                            self.board.is_square_empty(new_pos) or self.board.is_enemy_piece(new_pos, self.color)):
                        # if chess.check_move_and_is_check(self.position, new_pos, self.color, self.board):
                        moves.append(new_pos)
                if self.board.is_inside_board(new_pos) and (not self.board.is_square_empty(new_pos)):
                    break
        return moves

    def __str__(self):
        if self.color == "White":
            return "R"
        return "r"


class Knight(Piece):
    def __init__(self, color, board, position=None):
        super().__init__(color, board, position)
        self.piece_type = "knight"

    def possible_moves(self):
        moves = []
        offsets = [(1, 2), (2, 1), (1, -2), (2, -1), (-1, 2), (-2, 1), (-1, -2), (-2, -1)]
        self.possible_moves_loop(offsets, moves)
        # return super().possible_moves(moves)
        return moves

    def __str__(self):
        if self.color == "White":
            return "N"
        return "n"


class Queen(Piece):
    def __init__(self, color, board, position=None):
        super().__init__(color, board, position)
        self.piece_type = "queen"

    def possible_moves(self):
        moves = []
        offsets = [(1, -1), (1, 0), (1, 1), (-1, -1), (-1, -0), (-1, 1), (0, -1), (0, 1)]
        # chess = Chess()
        for dr, dc in offsets:
            new_pos = Position(self.position.row + dr, self.position.col + dc)
            while True:
                if self.board.is_inside_board(new_pos) and (
                        self.board.is_square_empty(new_pos) or self.board.is_enemy_piece(new_pos, self.color)):
                    # if chess.check_move_and_is_check(self.position, new_pos, self.color, self.board):
                    moves.append(new_pos)
                if (not self.board.is_inside_board(new_pos)) or self.board.is_enemy_piece(new_pos, self.color) or (
                not self.board.is_square_empty(new_pos)):
                    break
                new_pos = Position(new_pos.row + dr, new_pos.col + dc)
        return moves

    def __str__(self):
        if self.color == "White":
            return "Q"
        return "q"


class Board:
    def __init__(self):
        self.board = [[None for _ in range(8)] for _ in range(8)]  # Initialize the board
        self.moves = {'White': [], 'Black': []}
        self.latest_moves = []
        self.captured_pieces_gui = {'White': [], 'Black': []}
        self.fifty_moves_counter = 0

    def place_piece(self, piece, position):
        if piece is not None:
            piece.position = position
        self.board[position.row][position.col] = piece

    def remove_piece(self, position):
        self.board[position.row][position.col] = None

    def pawns_moves_adder(self):
        for i in self.board[3:5]:
            for j in i:
                if isinstance(j, Pawn):
                    j.move_count += 1

    def first_move_2_blocks_check(self, start_pos, end_pos):
        if abs(end_pos.row - start_pos.row) == 2:
            self.board[start_pos.row][start_pos.col].first_move_2_blocks = True

    def is_en_passant(self, start_pos, end_pos, color):
        if abs(end_pos.row - start_pos.row) == 1 and abs(end_pos.col - start_pos.col) == 1:
            try:
                enemy_white = self.board[end_pos.row - 1][end_pos.col]
                enemy_black = self.board[end_pos.row + 1][end_pos.col]
                if eval(f"enemy_{color}".lower()).first_move_2_blocks and eval(
                        f"enemy_{color}".lower()).move_count == 1:
                    self.captured_pieces_used_in_GUI(eval(f"enemy_{color}".lower()).position)
                    self.remove_piece(eval(f"enemy_{color}".lower()).position)  # REMOVES ENEMY PIECE
                    return eval(f"enemy_{color}".lower()).position
            except (AttributeError, TypeError, IndexError):
                return False

    def validate_castling(self, end_pos, current_player, king_possible_moves):
        # FOURTH CONDITION WHICH WHOULD HAPPEN TO CASTLING
        for i in self.board:
            for piece in i:
                if piece and piece.color!=current_player:
                    if end_pos.col==6:
                        if (
                            (piece.move(Position(end_pos.row, end_pos.col-1))
                            or piece.move(end_pos))):
                            for count, moves in enumerate(king_possible_moves):
                                if moves.row==end_pos.row and moves.col==end_pos.col:
                                    king_possible_moves.pop(count)
                            return False
                    else:
                        if (
                            (piece.move(Position(end_pos.row, end_pos.col+1))
                            or piece.move(Position(end_pos.row, end_pos.col-1))
                            or piece.move(end_pos))):
                            for count, moves in enumerate(king_possible_moves):
                                if moves.row==end_pos.row and moves.col==end_pos.col:
                                    king_possible_moves.pop(count)
                            return False
        return True

    def check_and_make_move_castling(self, start_pos, end_pos, piece):
        # CHECK THAT KING IS CHECK OR NOT
        for i in self.board:
            for enemy_piece in i:
                if enemy_piece and enemy_piece.color!=piece.color and enemy_piece.move(start_pos):
                    return False
        # CASLING
        if any(i != None and (i.row, i.col) == (end_pos.row, end_pos.col) for i in piece.castling().values()):
            if self.validate_castling(end_pos, piece.color, piece.possible_moves):
                king_moves = piece.castling()
                if king_moves['right'] != None and (king_moves['right'].row, king_moves['right'].col) == (end_pos.row, end_pos.col):
                    right_rook = self.board[start_pos.row][7]
                    self.remove_piece(Position(start_pos.row, 7))
                    self.place_piece(right_rook, Position(start_pos.row, 5))
                    right_rook.has_moved = True
                elif king_moves['left'] != None and (king_moves['left'].row, king_moves['left'].col) == (end_pos.row, end_pos.col):
                    left_rook = self.board[start_pos.row][0]
                    self.remove_piece(Position(start_pos.row, 0))
                    self.place_piece(left_rook, Position(start_pos.row, 3))
                    left_rook.has_moved = True
                # return True
            # return False
                    #     self.chess.chess_set.Board.validate_castling(Position(piece.position.row, 6), piece.color, piece_possible_moves)
                    # self.chess.chess_set.Board.validate_castling(Position(piece.position.row, 2), piece.color, piece_possible_moves)
    def captured_pieces_used_in_GUI(self, position):
        piece = self.board[position.row][position.col]
        if piece!=None:
            if piece.color == 'White':
                if piece not in self.captured_pieces_gui['White']:
                    self.captured_pieces_gui['White'].append(piece)
            else:
                if piece not in self.captured_pieces_gui['Black']:
                    self.captured_pieces_gui['Black'].append(piece)


    def move_piece(self, start_pos, end_pos):
        piece = self.board[start_pos.row][start_pos.col]
        if piece:
            if piece.move(end_pos):
                if isinstance(piece, Pawn):
                    self.first_move_2_blocks_check(start_pos, end_pos)
                    self.is_en_passant(start_pos, end_pos, piece.color)
                    self.fifty_moves_counter = 0
                if isinstance(piece, King):
                    self.check_and_make_move_castling(start_pos, end_pos, piece)
                check_board_before_move = sum(j is None for i in self.board for j in i)
                self.captured_pieces_used_in_GUI(end_pos)
                self.remove_piece(start_pos)
                self.place_piece(piece, end_pos)
                check_board_after_move = sum(j is None for i in self.board for j in i)
                if check_board_before_move != check_board_after_move or (isinstance(piece, Pawn)):
                    self.fifty_moves_counter = 0
                else:
                    self.fifty_moves_counter += 1
                    # print('fifty moves', self.fifty_moves_counter)
                piece.has_moved = True
                self.pawns_moves_adder()

                return True
            else:
                print('you cant move your piece to end_pos')
                return False
        else:
            print("No piece at the starting position.")
            return False

    def pawn_exchange(self, current_player, position, chosen_piece):
        self.remove_piece(position)
        self.remove_piece(position)
        self.place_piece(chosen_piece, position)

    def is_square_empty(self, position):
        return self.board[position.row][position.col] is None

    # (self.board[position.row][position.col].__str__()!='k' and self.board[position.row][position.col].__str__()!='K')
    def is_enemy_piece(self, position, color):
        if not self.is_square_empty(position):
            if (
                    self.board[position.row][position.col].color != color
            ):
                return True
        return False

    def moves_logger(self, start_pos, end_pos, current_player):
        start_pos = self.to_algebraic(start_pos)
        end_pos = self.to_algebraic(end_pos)
        self.moves[current_player].append(f"{start_pos} --> {end_pos}")
        self.latest_moves.append([start_pos, end_pos])

    @staticmethod
    def to_algebraic(position: Position):
        row = position.row
        col = chr(position.col + ord('a'))
        return col + str(row+1)

    @staticmethod
    def is_inside_board(position):
        return 0 <= position.row <= 7 and 0 <= position.col <= 7

    def print_board(self):
        print(" | a b c d e f g h")
        print("------------------")
        for i, row in enumerate(self.board):
            row_str = str(i) + "| "
            for piece in row:
                if piece:
                    row_str += f"{piece} "
                else:
                    row_str += ". "
            print(row_str)


class ChessSet:
    def __init__(self):
        self.Board = Board()
        self.setup_board()
        self.piece_count = {'k': 1, 'q': 1, 'b': 2, 'n': 2, 'r': 2, 'p': 8, 'K': 1, 'Q': 1, 'B': 2, 'N': 2, 'R': 2,
                            'P': 8}

    def setup_board(self):
        # Place white pieces

        for i in range(2):
            self.Board.place_piece(Rook("White", self.Board), Position(0, i) if i == 0 else Position(0, i + 6))
            self.Board.place_piece(Knight("White", self.Board), Position(0, i + 1) if i == 0 else Position(0, i + 5))
            self.Board.place_piece(Bishop("White", self.Board), Position(0, i + 2) if i == 0 else Position(0, i + 4))
        self.Board.place_piece(Queen("White", self.Board), Position(0, 3))
        self.Board.place_piece(King("White", self.Board), Position(0, 4))
        for i in range(8):
            self.Board.place_piece(Pawn("White", self.Board), Position(1, i))

        # Place black pieces
        for i in range(2):
            self.Board.place_piece(Rook("Black", self.Board), Position(7, i) if i == 0 else Position(7, i + 6))
            self.Board.place_piece(Knight("Black", self.Board), Position(7, i + 1) if i == 0 else Position(7, i + 5))
            self.Board.place_piece(Bishop("Black", self.Board), Position(7, i + 2) if i == 0 else Position(7, i + 4))
        self.Board.place_piece(Queen("Black", self.Board), Position(7, 3))
        self.Board.place_piece(King("Black", self.Board), Position(7, 4))
        for i in range(8):
            self.Board.place_piece(Pawn("Black", self.Board), Position(6, i))

    def print_board(self):
        self.Board.print_board()

    def captured_piece(self):
        pieces = {'k': 0, 'q': 0, 'b': 0, 'n': 0, 'r': 0, 'p': 0, 'K': 0, 'Q': 0, 'B': 0, 'N': 0, 'R': 0, 'P': 0}
        out_put = []
        for i in self.Board.board:
            for j in i:
                if j.__str__() in pieces.keys():
                    pieces[j.__str__()] += 1
                    # self.piece_count[j.__str__()] -= 1
        for key, value in pieces.items():
            num = key != 'None'
            self.piece_count = pieces


class Chess:
    def __init__(self):
        self.chess_set = ChessSet()

    # To check user choose their own piece
    def check_user_choose_valid_piece(self, start_pos, color):
        if color == 'White':
            if self.chess_set.Board.board[start_pos.row][start_pos.col].__str__().isupper():
                return True
            return False
        else:
            if self.chess_set.Board.board[start_pos.row][start_pos.col].__str__().islower():
                return True
            return False

    # To Find King Position
    def find_king_position(self, current_player):
        for count_row, i in enumerate(self.chess_set.Board.board):
            for count_col, j in enumerate(i):
                if current_player == "White":
                    if j.__str__() == "K":
                        king_position1 = Position(count_row, count_col)
                        return king_position1
                else:
                    if j.__str__() == "k":
                        king_position1 = Position(count_row, count_col)
                        return king_position1

    def all_posibble_move(self, current_player, board):
        piece_list = {
            "q": "Queen",
            "n": "Knight",
            "b": "Bishop",
            "r": "Rook",
            "k": "King",
            "p": "Pawn",
        }
        for row, i in enumerate(board.board):
            for col, j in enumerate(i):
                # color = 'White' if j.__str__().isupper() else 'Black'
                pos = Position(row, col)
                if j is not None and j.color == current_player:
                    piece = eval(f"{piece_list[j.__str__().lower()]}(current_player, board, j.position)")
                    for h in piece.possible_moves():
                        if self.check_move_and_is_check(Position(row, col), h, current_player, board):
                            return True

        return False

    def check_move_and_is_check(self, start_pos, end_pos, current_player, board):
        start_piece = board.board[start_pos.row][start_pos.col]
        captured_place_piece = board.board[end_pos.row][end_pos.col]
        board.remove_piece(start_pos)
        board.remove_piece(end_pos)
        board.place_piece(start_piece, end_pos)
        if captured_place_piece is not None:
            if self.is_check(current_player, board):
                board.remove_piece(start_pos), board.remove_piece(end_pos)
                board.place_piece(captured_place_piece, end_pos), board.place_piece(start_piece, start_pos)
                return False
            board.remove_piece(start_pos), board.remove_piece(end_pos)
            board.place_piece(captured_place_piece, end_pos), board.place_piece(start_piece, start_pos)
            return True
        else:
            if self.is_check(current_player, board):
                board.remove_piece(start_pos), board.remove_piece(end_pos)
                board.place_piece(start_piece, start_pos)
                return False
            board.remove_piece(start_pos), board.remove_piece(end_pos)
            board.place_piece(start_piece, start_pos)
            return True

    def is_check(self, current_player, board):
        # TODO - find current_player's king on the board, check if the king is in check
        king_position = self.find_king_position(current_player)
        enemy = "Black" if current_player == "White" else "White"
        if not king_position:
            return True

        for i in range(8):
            for j in range(8):
                piece = board.board[i][j]
                if piece.__str__() != "p" and piece.__str__() != "P":
                    if piece != None and piece.color == enemy:

                        if piece.move(king_position):
                            return True
                else:
                    if piece != None and piece.color == enemy:
                        white_offsets = [(1, -1), (1, 1)]
                        black_offsets = [(-1, 1), (-1, -1)]
                        for dr, dc in eval(f"{enemy.lower()}_offsets"):
                            new_pos1 = Position(i + dr, j + dc)

                            if (board.is_inside_board(new_pos1)
                                and (not board.is_square_empty(new_pos1))
                                and board.is_enemy_piece(new_pos1, piece.color)):

                                if (king_position.row == new_pos1.row
                                    and king_position.col == new_pos1.col):
                                    return True

        return False
        pass

    def is_checkmate(self, current_player, board):
        # For simplicity, we consider losing the king as checkmate
        enemy = "Black" if current_player == "White" else "White"
        king_position = self.find_king_position(current_player)
        king_piece = board.board[king_position.row][king_position.col]
        offsets = [(1, 0), (0, 1), (-1, 0), (0, -1), (1, 1), (-1, 1), (1, -1), (-1, -1)]
        for dr, dc in offsets:
            new_pose = Position(king_position.row + dr, king_position.col + dc)
            if board.is_inside_board(new_pose):
                if board.is_square_empty(new_pose):
                    if self.check_move_and_is_check(king_position, new_pose, current_player, board):
                        return False
                else:
                    if board.is_enemy_piece(new_pose, current_player):
                        if self.check_move_and_is_check(king_position, new_pose, current_player, board):
                            return False
        return True
        pass

    def is_draw(self):
        return self.draw_check_pieces() or self.draw_stalemate() or self.fifty_moves_rule() or self.same_condition() or self.pat('White') or self.pat('Black')

    def draw_stalemate(self):
        # TODO CAN BE IMPLEMENTED VIA CHECKMATE FUNCTIONS
        pass

    def draw_check_pieces(self):
        print('4')
        '''
            1. Each player has 1 King only - Finished
            2. 1 king + Bishop / Knight vs King  - Finished
            3. 2 Knights + King vs King - Finished
            4. King + Bishop / Knight vs King + Bishop / Knight - Finished (should be checked)

        '''
        pieces = self.chess_set.piece_count
        for i in pieces.keys():
            if pieces[i] != 0 and (i not in ['K', 'k', 'N', 'n', 'B', 'b']):
                break
        else:
            if ((pieces['n'] <= 2 and pieces['N'] == 0) or (pieces['n'] == 0 and pieces['N'] <= 2)) and (
                    pieces['B'] == 0 and pieces['b'] == 0):
                return True
            elif ((pieces['b'] == 1 and pieces['B'] == 0) or (pieces['b'] == 0 and pieces['B'] == 1)) and (
                    pieces['n'] == 0 and pieces['N'] == 0):
                return True
            elif ((pieces['n'] == 1 and pieces['N'] == 1) and (pieces['b'] == 0 and pieces['B'] == 0)) or (
                    (pieces['b'] == 1 and pieces['B'] == 1) and (pieces['n'] == 0 and pieces['N'] == 0)):
                return True
            elif pieces['N'] == 0 and pieces['n'] == 0 and pieces['b'] == 0 and pieces['B'] == 0:
                return True
            elif (pieces['N'] == 1 and pieces['n'] == 0) and (pieces['b'] == 1 and pieces['B'] == 0):
                return True
            elif (pieces['N'] == 0 and pieces['n'] == 1) and (pieces['b'] == 0 and pieces['B'] == 1):
                return True
            else:
                return False

    def fifty_moves_rule(self):
        print('50')
        if self.chess_set.Board.fifty_moves_counter == 50:
            return True

    def same_condition(self):
        print('same')
        if len(self.chess_set.Board.moves['White']) >= 5 and len(self.chess_set.Board.moves['Black']) >= 5:
            return (self.chess_set.Board.moves['White'][-1] == self.chess_set.Board.moves['White'][-3] == self.chess_set.Board.moves['White'][-5]) and (
                        self.chess_set.Board.moves['Black'][-1] == self.chess_set.Board.moves['Black'][-3] == self.chess_set.Board.moves['Black'][-5])
   
    def pat(self, current_player):
        print('pat')
        for i in self.chess_set.Board.board:
            for piece in i:
                if piece and piece.color!=current_player and len(piece.possible_moves())>0:
                    for end_pos in piece.possible_moves():
                        if self.check_move_and_is_check(piece.position, end_pos, 'White' if current_player=='Black' else 'Black', self.chess_set.Board):
                            return False
        return True
                

    @staticmethod
    def from_algebraic(algebraic_notation):
        col = ord(algebraic_notation[0]) - ord('a')
        row = int(algebraic_notation[1])
        return Position(row, col)
