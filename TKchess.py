import tkinter as tk

class ChessGUI:
    def __init__(self, root, board):
        self.root = root
        self.root.title("Chess")

        self.board = board  # your current chess board
        self.buttons = {}
        self.selected = None
        self.turn = "white"

        self.create_board()
        self.display_pieces(self.board)

    def create_board(self):
        colors = ["#F0D9B5", "#B58863"]
        for row in range(8):
            for col in range(8):
                color = colors[(row + col) % 2]
                btn = tk.Button(self.root, bg=color, width=8, height=4,
                                command=lambda r=row, c=col: self.on_click(r, c))
                btn.grid(row=row, column=col)
                self.buttons[(row, col)] = btn

    def display_pieces(self, board):
        for row in range(8):
            for col in range(8):
                piece = board[row][col]
                self.buttons[(row, col)].config(text=piece)

    def can_capture(self, moving_piece, target_piece):
        if target_piece == " ":
            return True  # empty square is always allowed
        if moving_piece.isupper() and target_piece.islower():
            return True  # white can capture black piece
        if moving_piece.islower() and target_piece.isupper():
            return True  # black can capture white piece
        return False

    def is_valid_pawn_move(self, from_row, from_col, to_row, to_col, board=None, for_attack=False):
        if board is None:
            board = self.board
        moving_piece = board[from_row][from_col]
        direction = -1 if moving_piece.isupper() else 1
        start_row = 6 if moving_piece.isupper() else 1
        target_piece = board[to_row][to_col]

        if for_attack:
            return (to_row == from_row + direction) and (abs(to_col - from_col) == 1)
        else:
        # Normal 1-step forward
            if from_col == to_col and to_row == from_row + direction:
                if target_piece == " ":
                    return True

            # 2-step forward from starting position
            if from_col == to_col and from_row == start_row and to_row == from_row + 2 * direction:
                if self.board[from_row + direction][to_col] == " " and target_piece == " ":
                    return True

            # Diagonal capture
            if abs(from_col - to_col) == 1 and to_row == from_row + direction:
                if target_piece != " " and self.can_capture(moving_piece, target_piece):
                    return True
            return False

    def is_valid_knight_move(self, from_row, from_col, to_row, to_col, board=None, for_attack=False):
        if board is None:
            board = self.board
        moving_piece = board[from_row][from_col]
        target_piece = board[to_row][to_col]
        if (abs(to_row - from_row) == 2 and abs(to_col - from_col) == 1) or \
                (abs(to_row - from_row) == 1 and abs(to_col - from_col) == 2):
            target_piece = self.board[to_row][to_col]
            return self.can_capture(moving_piece, target_piece) or for_attack
        return False

    def is_valid_rook_move(self, from_row, from_col, to_row, to_col, board=None, for_attack=False):
        if board is None:
            board = self.board
        moving_piece = board[from_row][from_col]
        target_piece = board[to_row][to_col]

        if from_col == to_col:
            # Vertical move: iterate rows
            step = 1 if to_row > from_row else -1
            for row in range(from_row + step, to_row, step):
                if board[row][from_col] != " ":
                    return False
            return self.can_capture(moving_piece, target_piece)  # <--- Check capture after path clear

        elif from_row == to_row:
            # Horizontal move: iterate columns
            step = 1 if to_col > from_col else -1
            for col in range(from_col + step, to_col, step):
                if board[from_row][col] != " ":
                    return False
            return self.can_capture(moving_piece, target_piece) or for_attack  # <--- Check capture after path clear

        return False

    def is_valid_bishop_move(self, from_row, from_col, to_row, to_col, board=None, for_attack=False):
        if board is None:
            board = self.board
        moving_piece = board[from_row][from_col]
        target_piece = board[to_row][to_col]

        if abs(to_row - from_row) != abs(to_col - from_col):
            return False

        row_step = 1 if to_row > from_row else -1
        col_step = 1 if to_col > from_col else -1

        current_row = from_row + row_step
        current_col = from_col + col_step

        while current_row != to_row and current_col != to_col:
            if self.board[current_row][current_col] != " ":
                return False
            current_row += row_step
            current_col += col_step

        return self.can_capture(moving_piece, target_piece) or for_attack

    def is_valid_king_move(self, from_row, from_col, to_row, to_col, board=None, for_attack=False):
        if board is None:
            board = self.board
        moving_piece = board[from_row][from_col]
        target_piece = board[to_row][to_col]
        row_diff = abs(to_row - from_row)
        col_diff = abs(to_col - from_col)

        if max(row_diff, col_diff) == 1:
            return self.can_capture(moving_piece, target_piece) or for_attack
        return False

    def is_valid_move(self, from_row, from_col, to_row, to_col, board=None, for_attack=False):
        if board is None:
            board = self.board
        moving_piece = board[from_row][from_col]
        piece = moving_piece.lower()

        if piece == 'p':
            return self.is_valid_pawn_move(from_row, from_col, to_row, to_col, board, for_attack)

        elif piece == 'n':
            return self.is_valid_knight_move(from_row, from_col, to_row, to_col, board, for_attack)

        elif piece == 'r':
            return self.is_valid_rook_move(from_row, from_col, to_row, to_col, board, for_attack)

        elif piece == 'b':
            return self.is_valid_bishop_move(from_row, from_col, to_row, to_col, board, for_attack)

        elif piece == 'q':
            return (self.is_valid_bishop_move(from_row, from_col, to_row, to_col, board, for_attack) or
                    self.is_valid_rook_move(from_row, from_col, to_row, to_col, board, for_attack))

        elif piece == 'k':
            return self.is_valid_king_move(from_row, from_col, to_row, to_col, board, for_attack)

        return False

    def is_king_in_check(self, color, board, is_valid_move):
        king_symbol = 'k' if color == 'black' else 'K'
        king_pos = None

        # Locate the king
        for r in range(8):
            for c in range(8):
                if board[r][c] == king_symbol:
                    king_pos = (r, c)
                    break
            if king_pos:
                break

        if not king_pos:
            return False

        for r in range(8):
            for c in range(8):
                piece = board[r][c]
                if color == 'white' and piece.islower():
                    if is_valid_move(r, c, king_pos[0], king_pos[1], board, for_attack=True):
                        return True
                elif color == 'black' and piece.isupper():
                    if is_valid_move(r, c, king_pos[0], king_pos[1], board, for_attack=True):
                        return True
        return False


    def on_click(self, row, col):
        piece = self.board[row][col]

        #Turn
        is_white_piece = piece.isupper()
        is_black_piece = piece.islower()

        #Frist click: selected piece
        if not self.selected:
            if(self.turn == "white" and is_white_piece) or (self.turn == "black" and is_black_piece):
                self.selected = (row, col)
            return

        #Select click: move piece
        from_row, from_col = self.selected
        moving_piece = self.board[from_row][from_col]

        #Prevent capture own piece
        if(self.turn == "white" and piece.isupper()) or (self.turn == "black" and piece.islower()):
            self.selected = None
            return

        #Validation the move
        if not self.is_valid_move(from_row, from_col, row, col):
            print("invalid move!")
            self.selected = None
            return

        #Simulate move and check the king is in check
        temp_board = [list(r) for r in self.board]
        temp_board[row][col] = moving_piece
        temp_board[from_row][from_col] = " "

        def simulated_is_valid_move(from_row, from_col, to_row, to_col, board, for_attack=True):
            # Temporarily use the passed-in board instead of self.board
            original_board = self.board
            self.board = board
            result = self.is_valid_move(from_row, from_col, to_row, to_col, board, for_attack)
            self.board = original_board
            return result

        if self.is_king_in_check(self.turn, temp_board, simulated_is_valid_move):
            print("Illegal move: Your king would be in check!")
            self.selected = None
            return

        #Move piece
        self.board[row][col] = moving_piece
        self.board[from_row][from_col] = " "
        self.selected = None
        self.display_pieces(self.board)

        #Switch turn
        self.turn = "black" if self.turn == "white" else "white"


if __name__ == "__main__":
    # Use your existing create_board function or board state
    def create_board():
        return [
            ["r","n","b","q","k","b","n","r"],
            ["p","p","p","p","p","p","p","p"],
            [" "," "," "," "," "," "," "," "],
            [" "," "," "," "," "," "," "," "],
            [" "," "," "," "," "," "," "," "],
            [" "," "," "," "," "," "," "," "],
            ["P","P","P","P","P","P","P","P"],
            ["R","N","B","Q","K","B","N","R"]
        ]

    board = create_board()

    root = tk.Tk()
    gui = ChessGUI(root, board)
    root.mainloop()