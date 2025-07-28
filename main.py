
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
#Lowercase = Black, Uppercase = White

def print_board(board):
    print("  a b c d e f g h")
    for i, row in enumerate(board):
        print(8 - i, " ".join(row), 8 - i)
    print("  a b c d e f g h\n")

def parse_move(move):
    files = {'a':0, 'b':1, 'c':2, 'd':3, 'e':4, 'f':5, 'g':6, 'h':7}
    try:
        start, end = move.split()
        start_row = 8 - int(start[1])
        start_col = files[start[0]]
        end_row = 8 - int(end[1])
        end_col = files[end[0]]
        return (start_row, start_col), (end_row, end_col)
    except:
        return None, None

def make_move(board, start, end):
    piece = board[start[0]][start[1]]
    board[end[0]][end[1]] = piece
    board[start[0]][start[1]] = " "

def is_valid_pawn_move(start, end, board, turn):
    direction = -1 if turn == "White" else 1
    start_row, start_col = start
    end_row, end_col = end
    piece = board[start_row][start_col]
    target = board[end_row][end_col]

    #move 1 step forward
    if start_col == end_col and end_row == start_row + direction and target == " ":
        return True

    #move 2 step for starting position
    if((turn == "White" and start_row == 6) or (turn == "Black" and start_row == 1)) and \
        start_col == end_col and end_row == start_row + 2 * direction and\
        target == " " and board[start_row + direction][start_col] == " ":
        return True

    #Capture
    if abs(end_col - start_col) == 1 and end_row == start_row + direction:
        if(turn == "White" and target.islower()) or (turn == "Black" and target.isupper()):
            print("captured")
            return True

    return False

def is_valid_knight_move(start, end, board, turn):
    start_row, start_col = start
    end_row, end_col = end
    piece = board[start_row][start_col]
    target = board[end_row][end_col]

    # check the knight correct color
    if turn == "White" and piece != "N":
        return False
    if turn == "Black" and piece != "n":
        return False
    #Cal the difference in rows and columns
    row_diff = abs(end_row - start_row)
    col_diff = abs(end_col - start_col)

    #knight move in L shape so 2 1
    if (row_diff, col_diff) not in [(2,1), (1,2)]:
        return False

    #Make sure it not cature it own piece
    if target != " ":
        if turn == "White" and target.isupper():
            return False
        if turn == "Black" and target.islower():
            return False

    return True

def is_valid_Rook_move(start, end, board, turn):
    start_row, start_col = start
    end_row, end_col = end
    piece = board[start_row][start_col]
    target = board[end_row][end_col]

    # Move straight line
    if start_row != end_row and start_col != end_col:
        return False
    #Check path is clear
    ##Move Horizontally
    if start_row == end_row:
        step = 1 if end_col> start_col else -1
        for col in range(start_col + step, end_col, step):
            if board[start_row][col] != " ":
                return False
    ##Move Vertically
    else:
        step = 1 if end_row > start_row else -1
        for row in range(start_row + step, end_row, step):
            if board[row][start_col] != " ":
                return False

    #Cannot capture own piece
    if target != " " and target.isupper() == piece.isupper():
        return False

    return True

def is_valid_Bishop_move(start, end, board, turn):
    start_row, start_col = start
    end_row, end_col = end
    piece = board[start_row][start_col]
    target = board[end_row][end_col]

    # Check it's a diagonal move
    row_diff = abs(end_row - start_row)
    col_diff = abs(end_col - start_col)
    if row_diff != col_diff:
        return False
    # Determine direction
    row_step = 1 if end_row > start_row else -1
    col_step = 1 if end_col > start_col else -1

    #Check if path is clear
    r, c = start_row + row_step, start_col + col_step
    while r != end_row and c != end_col:
        if board[r][c] != " ":
            return False
        r += row_step
        c += col_step
    # Cant capture own piece
    if target != " " and target.isupper() == piece.isupper():
        return False
    return True

def is_valid_Queen_move(start, end, board, turn):
    # Queen moves like rook or bishop
    if is_valid_Rook_move(start, end, board, turn) or is_valid_Bishop_move(start, end, board, turn):
        return True
    return False

def is_valid_King_move(start, end, board, turn):
    start_row, start_col = start
    end_row, end_col = end
    piece = board[start_row][start_col]
    target = board[end_row][end_col]

    # Check that the move is only one square in any direction
    row_diff = abs(end_row - start_row)
    col_diff = abs(end_col - start_col)

    if max(row_diff, col_diff) != 1:
        return False

    # Cannot capture own piece
    if target != " " and target.isupper() == piece.isupper():
        return False

    return True

def main():
    board = create_board()
    turn = "White"

    while True:
        print_board(board)
        move = input(f"{turn}'s move (e.g. e2 e4): ").strip()
        start, end = parse_move(move)

        if not start or not end:
            print("Invalid input! Try again.")
            continue

        start_piece = board[start[0]][start[1]]
        end_piece = board[end[0]][end[1]]

        # Skip if empty start
        if start_piece == " ":
            print("There's no piece there!")
            continue

        # Enforce turn-based movement
        if turn == "White" and start_piece.islower():
            print("That's Black's piece!")
            continue
        if turn == "Black" and start_piece.isupper():
            print("That's White's piece!")
            continue

        # Prevent capturing your own piece
        if (start_piece.isupper() and end_piece.isupper()) or \
           (start_piece.islower() and end_piece.islower()):
            print("You can't capture your own piece!")
            continue

        if start_piece.upper() == "P":
            if not is_valid_pawn_move(start, end, board, turn):
                print("Invalid pawn move!")
                continue

        if start_piece.upper() == "N":
            if not is_valid_knight_move(start, end, board, turn):
                print("Invalid knight move!")
                continue

        if start_piece.upper() == "R":
            if not is_valid_Rook_move(start, end, board, turn):
                print("Invalid Rook move!")
                continue

        if start_piece.upper() == "B":
            if not is_valid_Bishop_move(start, end, board, turn):
                print("Invalid Bishop move!")
                continue

        if start_piece.upper() == "Q":
            if not is_valid_Queen_move(start, end, board, turn):
                print("Invalid Queen move!")
                continue

        if start_piece.upper() == "K":
            if not is_valid_King_move(start, end, board, turn):
                print("Invalid king move!")
                continue

        # Valid move, apply it
        make_move(board, start, end)

        # Switch turns
        turn = "Black" if turn == "White" else "White"




if __name__ == "__main__":
    main()