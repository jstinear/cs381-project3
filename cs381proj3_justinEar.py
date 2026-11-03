import ast
import time
import math
from itertools import combinations

BOARD_SIZE = 4
EMPTY = 0


def checkValid(board):
    """
    Returns True if the board is a valid game state or a completed game.
    Invalid examples:
      - counts of 1 and 2 differ by more than 1
      - both players have a winning set
      - board has impossible turn order
    """
    if len(board) != 4:
        return False
    for row in board:
        if len(row) != 4:
            return False
        for cell in row:
            if cell not in (0, 1, 2):
                return False

    p1 = sum(cell == 1 for row in board for cell in row)
    p2 = sum(cell == 2 for row in board for cell in row)

    if abs(p1 - p2) > 1:
        return False

    p1_win = has_win(board, 1)
    p2_win = has_win(board, 2)

    if p1_win and p2_win:
        return False

    # If player 1 wins, player 1 must have exactly one more move than player 2.
    if p1_win and p1 <= p2:
        return False

    # If player 2 wins, the move counts must be equal.
    if p2_win and p1 != p2:        
        return False

    return True


def has_win(board, player):
    "True if player has a 4-cell capture with all distinct rows and columns."
    positions = []
    for r in range(4):
        for c in range(4):
            if board[r][c] == player:
                positions.append((r, c))

    for combo in combinations(positions, 4):
        rows = {r for r, c in combo}
        cols = {c for r, c in combo}
        if len(rows) == 4 and len(cols) == 4:
            return True
    return False


def count_wins(board, player):
    "Number of distinct winning 4-cell sets for a player."
    positions = [(r, c) for r in range(4) for c in range(4) if board[r][c] == player]
    total = 0
    for combo in combinations(positions, 4):
        rows = {r for r, c in combo}
        cols = {c for r, c in combo}
        if len(rows) == 4 and len(cols) == 4:
            total += 1
    return total


def eval(board, p):
    "Return the number of winning sets for p minus the opponent's winning sets."
    if not checkValid(board):
        raise ValueError("Invalid board for eval()")
    if p not in (1, 2):
        raise ValueError("Player must be 1 or 2")

    opponent = 3 - p
    return count_wins(board, p) - count_wins(board, opponent)


def legal_moves(board):
    "Return empty positions as (row, column), using zero-based indexes."
    return [
        (r, c)
        for r in range(4)
        for c in range(4)
        if board[r][c] == EMPTY
    ]


def apply_move(board, move, player):
    "Return a new board with the move applied."
    r, c = move
    new_board = [row[:] for row in board]
    if new_board[r][c] != EMPTY:
        raise ValueError("Illegal move")
    new_board[r][c] = player
    return new_board


def current_player(board):
    "Determine whose turn it is based on the move counts."
    p1 = sum(cell == 1 for row in board for cell in row)
    p2 = sum(cell == 2 for row in board for cell in row)

    if p1 == p2:
        return 1
    if p1 == p2 + 1:
        return 2
    raise ValueError("Board has an impossible move count")


def terminal_value(board):
    "Return 1 if player 1 won, -1 if player 2 won, or 0 if no winner."
    if has_win(board, 1):
        return 1
    if has_win(board, 2):
        return -1
    return 0


def Minimax(board):
    """Return (value, nodes_expanded, elapsed_seconds)."""
    if not checkValid(board):
        raise ValueError("Invalid board")

    start = time.perf_counter()
    nodes = 0

    def solve(state, turn):
        nonlocal nodes
        nodes += 1  # Count each visited state, including the root.

        outcome = terminal_value(state)
        if outcome != 0:
            return outcome

        moves = legal_moves(state)
        if not moves:
            return 0

        if turn == 1:
            best = -2
            for move in moves:
                best = max(best, solve(apply_move(state, move, 1), 2))
            return best

        best = 2
        for move in moves:
            best = min(best, solve(apply_move(state, move, 2), 1))
        return best

    value = solve(board, current_player(board))
    elapsed = time.perf_counter() - start
    return value, nodes, elapsed


def MinimaxCutOff(board, k):
    "Depth-limited minimax; return (value, best_move, nodes, elapsed_seconds)."
    if k < 0:
        raise ValueError("k must be non-negative")
    if not checkValid(board):
        raise ValueError("Invalid board")

    root_player = current_player(board)
    start = time.perf_counter()
    nodes = 0

    def search(state, depth, turn):
        nonlocal nodes
        nodes += 1

        outcome = terminal_value(state)
        if outcome != 0:
            return outcome if root_player == 1 else -outcome

        moves = legal_moves(state)
        if depth == 0 or not moves:
            return eval(state, root_player)

        if turn == root_player:
            best = -math.inf
            for move in moves:
                best = max(best, search(apply_move(state, move, turn), depth - 1, 3 - turn))
            return best

        best = math.inf
        for move in moves:
            best = min(best, search(apply_move(state, move, turn), depth - 1, 3 - turn))
        return best

    moves = sorted(legal_moves(board))
    if not moves:
        return 0, None, nodes, time.perf_counter() - start

    best_move = None
    best_value = -math.inf
    for move in moves:
        value = search(apply_move(board, move, root_player), k - 1, 3 - root_player)
        if value > best_value:
            best_value, best_move = value, move

    return best_value, best_move, nodes, time.perf_counter() - start


def MinimaxAlphaBetaCutOff(board, k):
    "Depth-limited alpha-beta search; return (value, move, nodes, elapsed_seconds)."
    if k < 0:
        raise ValueError("k must be non-negative")
    if not checkValid(board):
        raise ValueError("Invalid board")

    root_player = current_player(board)
    start = time.perf_counter()
    nodes = 0

    def search(state, depth, turn, alpha, beta):
        nonlocal nodes
        nodes += 1

        outcome = terminal_value(state)
        if outcome != 0:
            return outcome if root_player == 1 else -outcome

        moves = legal_moves(state)
        if depth == 0 or not moves:
            return eval(state, root_player)

        if turn == root_player:
            best = -math.inf
            for move in moves:
                best = max(best, search(
                    apply_move(state, move, turn), depth - 1, 3 - turn, alpha, beta
                ))
                alpha = max(alpha, best)
                if alpha >= beta:
                    break
            return best

        best = math.inf
        for move in moves:
            best = min(best, search(
                apply_move(state, move, turn), depth - 1, 3 - turn, alpha, beta
            ))
            beta = min(beta, best)
            if alpha >= beta:
                break
        return best

    moves = sorted(legal_moves(board))
    if not moves:
        return 0, None, nodes, time.perf_counter() - start

    best_move = None
    best_value = -math.inf
    alpha, beta = -math.inf, math.inf
    for move in moves:
        value = search(apply_move(board, move, root_player), k - 1, 3 - root_player, alpha, beta)
        if value > best_value:
            best_value, best_move = value, move
        alpha = max(alpha, best_value)

    return best_value, best_move, nodes, time.perf_counter() - start


def display_board(board):
    for row in board:
        print(" ".join(str(cell) for cell in row))
    print()


def prompt_move(board, player):
    "Prompt for an empty square, with row and column numbered 1 through 4."
    while True:
        try:
            parts = input(f"Player {player}: enter row col (1-4): ").split()
            if len(parts) != 2:
                raise ValueError
            r, c = int(parts[0]) - 1, int(parts[1]) - 1
            if 0 <= r < 4 and 0 <= c < 4 and board[r][c] == EMPTY:
                return r, c
        except ValueError:
            pass
        print("Invalid move. Enter row and column numbers between 1 and 4 for an empty square.")


def parse_board_input():
    "Read a board as a nested list, 16 values on one line, or four rows."
    txt = input("Enter the board: ").strip()

    if txt.startswith("["):
        try:
            board = ast.literal_eval(txt)
            if (isinstance(board, (list, tuple)) and len(board) == 4
                    and all(isinstance(row, (list, tuple)) and len(row) == 4 for row in board)):
                return [[int(value) for value in row] for row in board]
        except (ValueError, SyntaxError, TypeError):
            pass

    tokens = txt.replace(",", " ").split()
    if len(tokens) == 16:
        values = [int(token) for token in tokens]
        return [values[r * 4:(r + 1) * 4] for r in range(4)]

    if len(tokens) == 4:
        # The first line can be the first row in four-row input.
        rows = [[int(token) for token in tokens]]
        for _ in range(3):
            row_tokens = input().replace(",", " ").split()
            if len(row_tokens) != 4:
                raise ValueError("Each board row must contain exactly four values.")
            rows.append([int(token) for token in row_tokens])
        return rows

    raise ValueError("Enter a 4x4 nested list, 16 values on one line, or four rows of four values.")


def _get_valid_board():
    "Keep prompting until a valid board is entered."
    while True:
        board = parse_board_input()
        if checkValid(board):
            return board
        print("That board is invalid. Please enter a valid board.")


def _announce_result(board, human_player):
    "Display the finished board and report the winner or draw."
    display_board(board)
    if has_win(board, human_player):
        print("You win!")
    elif has_win(board, 3 - human_player):
        print("Computer wins!")
    else:
        print("The game is a draw.")


def play_human_vs_computer():
    "Option 0: play from an empty board, choosing whether the human starts."
    board = [[EMPTY for _ in range(4)] for _ in range(4)]
    answer = input("Do you want to play first? (y/n): ").strip().lower()
    human_player = 1 if answer in ("y", "yes") else 2
    computer_player = 3 - human_player

    while True:
        try:
            depth = int(input("Choose cutoff depth for the computer (positive integer): "))
            if depth > 0:
                break
        except ValueError:
            pass
        print("Please enter a positive integer depth.")

    turn = 1
    while True:
        display_board(board)
        if turn == human_player:
            r, c = prompt_move(board, human_player)
            board[r][c] = human_player
        else:
            print("Computer thinking...")
            _, move, _, _ = MinimaxAlphaBetaCutOff(board, depth)
            if move is None:
                break
            r, c = move
            board[r][c] = computer_player
            print(f"Computer plays at row {r + 1}, column {c + 1}.")

        if has_win(board, 1) or has_win(board, 2) or not legal_moves(board):
            _announce_result(board, human_player)
            return
        turn = 3 - turn


def play_from_entered_board():
    "Option 4: continue a valid entered position against the computer."
    board = _get_valid_board()

    while True:
        try:
            human_player = int(input("Choose your player (1 or 2): ").strip())
            if human_player in (1, 2):
                break
        except ValueError:
            pass
        print("Please enter 1 or 2.")
    computer_player = 3 - human_player

    while True:
        try:
            depth = int(input("Choose cutoff depth for the computer (positive integer): "))
            if depth > 0:
                break
        except ValueError:
            pass
        print("Please enter a positive integer depth.")

    # If the supplied valid board is already finished, report it without making a move.
    if has_win(board, 1) or has_win(board, 2) or not legal_moves(board):
        _announce_result(board, human_player)
        return

    turn = current_player(board)
    while True:
        display_board(board)
        if turn == human_player:
            r, c = prompt_move(board, human_player)
            board[r][c] = human_player
        else:
            print("Computer thinking...")
            _, move, _, _ = MinimaxAlphaBetaCutOff(board, depth)
            if move is None:
                _announce_result(board, human_player)
                return
            r, c = move
            board[r][c] = computer_player
            print(f"Computer plays at row {r + 1}, column {c + 1}.")

        if has_win(board, 1) or has_win(board, 2) or not legal_moves(board):
            _announce_result(board, human_player)
            return
        turn = 3 - turn


def main():
    while True:
        print("\nCS381 Project 3")
        print("0. Play against the computer from an empty board")
        print("1. Evaluate a board using Minimax")
        print("2. Evaluate using MinimaxAlphaBetaCutOff")
        print("3. Compare MinimaxCutOff and MinimaxAlphaBetaCutOff")
        print("4. Play against the computer from a valid board")
        print("5. Exit")

        choice = input("Choose an option: ").strip()

        try:
            if choice == "0":
                play_human_vs_computer()

            elif choice == "1":
                board = parse_board_input()
                value, nodes, elapsed = Minimax(board)
                print("Minimax value:", value)
                print("Nodes expanded:", nodes)
                print("CPU time:", elapsed)

            elif choice == "2":
                board = parse_board_input()
                depth = int(input("Enter cutoff depth k: "))
                value, move, nodes, elapsed = MinimaxAlphaBetaCutOff(board, depth)
                print("Value:", value)
                print("Best move:", move)
                print("Nodes expanded:", nodes)
                print("CPU time:", elapsed)

            elif choice == "3":
                board = parse_board_input()
                depth = int(input("Enter cutoff depth k: "))
                value1, move1, nodes1, elapsed1 = MinimaxCutOff(board, depth)
                value2, move2, nodes2, elapsed2 = MinimaxAlphaBetaCutOff(board, depth)

                print("MinimaxCutOff:")
                print("Value:", value1)
                print("Best move:", move1)
                print("Nodes expanded:", nodes1)
                print("CPU time:", elapsed1)

                print("MinimaxAlphaBetaCutOff:")
                print("Value:", value2)
                print("Best move:", move2)
                print("Nodes expanded:", nodes2)
                print("CPU time:", elapsed2)

            elif choice == "4":
                play_from_entered_board()

            elif choice == "5":
                print("Exiting.")
                break
            else:
                print("Invalid option. Choose a number from 0 to 5.")
        except (ValueError, TypeError) as error:
            print("Error:", error)


if __name__ == "__main__":
    main()
