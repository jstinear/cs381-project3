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

    # If player 1 wins, player 1 must have exactly one more move than player 2
    if p1_win and p1 <= p2:
        return False

    # If player 2 wins, player 2 must not have more pieces than player 1
    if p2_win and p2 > p1:
        return False

    return True


def has_win(board, player):
    """True if player has a 4-cell capture with all distinct rows and cols."""
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
    """Number of distinct winning 4-cell sets for a player."""
    positions = [(r, c) for r in range(4) for c in range(4) if board[r][c] == player]
    total = 0
    for combo in combinations(positions, 4):
        rows = {r for r, c in combo}
        cols = {c for r, c in combo}
        if len(rows) == 4 and len(cols) == 4:
            total += 1
    return total


def eval(board, p):
    """
    Static evaluation:
      e(B, p) = number of ways player p can win - number of ways opponent can win
    """
    if not checkValid(board):
        raise ValueError("Invalid board for eval()")
    if p not in (1, 2):
        raise ValueError("Player must be 1 or 2")

    opp = 3 - p
    return count_wins(board, p) - count_wins(board, opp)


def legal_moves(board):
    """Return all empty moves as (row, col) using zero-based indexing."""
    moves = []
    for r in range(4):
        for c in range(4):
            if board[r][c] == 0:
                moves.append((r, c))
    return moves


def apply_move(board, move, player):
    """Return a new board with the move applied."""
    r, c = move
    new_board = [row[:] for row in board]
    if new_board[r][c] != 0:
        raise ValueError("Illegal move")
    new_board[r][c] = player
    return new_board


def current_player(board):
    """Determine whose turn it should be based on the move counts."""
    p1 = sum(cell == 1 for row in board for cell in row)
    p2 = sum(cell == 2 for row in board for cell in row)

    if p1 == p2:
        return 1
    if p1 == p2 + 1:
        return 2
    raise ValueError("Board has an impossible move count")


def terminal_value(board):
    """
    Return 1 if player 1 has won, -1 if player 2 has won, 0 otherwise.
    """
    if has_win(board, 1):
        return 1
    if has_win(board, 2):
        return -1
    return 0


def Minimax(board):
    """
    Return the value of the board:
      1 if player 1 can force a win
      0 if neither player can force a win
     -1 if player 2 can force a win

    This is the full minimax implementation for Option 1. It may take a long time for
    sparse boards because the game tree is large; that is expected.
    """
    if not checkValid(board):
        raise ValueError("Invalid board")

    def solve(state, turn):
        outcome = terminal_value(state)
        if outcome != 0:
            return outcome

        moves = legal_moves(state)
        if not moves:
            return 0

        if turn == 1:
            best = -2
            for move in moves:
                child = apply_move(state, move, 1)
                val = solve(child, 2)
                if val > best:
                    best = val
            return best
        else:
            best = 2
            for move in moves:
                child = apply_move(state, move, 2)
                val = solve(child, 1)
                if val < best:
                    best = val
            return best

    return solve(board, current_player(board))


def MinimaxCutOff(board, k):
    """
    Minimax search to depth k.
    Returns: (value, best_move, nodes_expanded, elapsed_time)
    best_move is chosen with smaller row, smaller col tie-break.
    The returned value is for the root player.
    """
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
            if root_player == 1:
                return outcome
            return -outcome

        if depth == 0 or not legal_moves(state):
            return eval(state, root_player)

        moves = legal_moves(state)
        if turn == root_player:
            best = -math.inf
            for move in moves:
                child = apply_move(state, move, turn)
                val = search(child, depth - 1, 3 - turn)
                if val > best:
                    best = val
            return best
        else:
            best = math.inf
            for move in moves:
                child = apply_move(state, move, turn)
                val = search(child, depth - 1, 3 - turn)
                if val < best:
                    best = val
            return best

    best_move = None
    best_value = -math.inf

    for move in sorted(legal_moves(board)):
        child = apply_move(board, move, root_player)
        value = search(child, k - 1, 3 - root_player)

        if value > best_value:
            best_value = value
            best_move = move
        elif value == best_value and (best_move is None or move < best_move):
            best_move = move

    elapsed = time.perf_counter() - start
    return best_value, best_move, nodes, elapsed


def MinimaxAlphaBetaCutOff(board, k):
    """
    Minimax with alpha-beta pruning to depth k.
    Returns: (value, best_move, nodes_expanded, elapsed_time)
    The returned value is for the root player.
    """
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
            if root_player == 1:
                return outcome
            return -outcome

        if depth == 0 or not legal_moves(state):
            return eval(state, root_player)

        moves = legal_moves(state)

        if turn == root_player:
            best = -math.inf
            for move in moves:
                child = apply_move(state, move, turn)
                val = search(child, depth - 1, 3 - turn, alpha, beta)
                if val > best:
                    best = val
                if best > alpha:
                    alpha = best
                if alpha >= beta:
                    break
            return best
        else:
            best = math.inf
            for move in moves:
                child = apply_move(state, move, turn)
                val = search(child, depth - 1, 3 - turn, alpha, beta)
                if val < best:
                    best = val
                if best < beta:
                    beta = best
                if alpha >= beta:
                    break
            return best

    best_move = None
    best_value = -math.inf
    alpha = -math.inf
    beta = math.inf

    for move in sorted(legal_moves(board)):
        child = apply_move(board, move, root_player)
        value = search(child, k - 1, 3 - root_player, alpha, beta)

        if value > best_value:
            best_value = value
            best_move = move
            if best_value > alpha:
                alpha = best_value
        elif value == best_value and (best_move is None or move < best_move):
            best_move = move

    elapsed = time.perf_counter() - start
    return best_value, best_move, nodes, elapsed


def display_board(board):
    for row in board:
        print(" ".join(str(cell) for cell in row))
    print()


def prompt_move(board, player):
    while True:
        try:
            text = input(f"Player {player}: enter row col (1-4): ").strip()
            parts = text.split()
            if len(parts) != 2:
                raise ValueError
            r = int(parts[0]) - 1
            c = int(parts[1]) - 1
            if 0 <= r < 4 and 0 <= c < 4 and board[r][c] == 0:
                return (r, c)
            raise ValueError
        except Exception:
            print("Invalid move. Enter row and column numbers between 1 and 4 on an empty square.")


def parse_board_input():
    """
    Accepts either:
      - 16 numbers in a single line (e.g. 1 0 0 0 2 0 0 0 ...)
      - 4 rows of 4 numbers
      - a Python-style nested list like:
        [[1,0,0,0],[2,0,0,0],[0,2,1,0],[0,0,0,0]]
    """
    raw = input("Enter the board: ").strip()

    if raw.startswith("["):
        try:
            board = ast.literal_eval(raw)
            if isinstance(board, list) and len(board) == 4:
                if all(isinstance(row, (list, tuple)) and len(row) == 4 for row in board):
                    return [[int(x) for x in row] for row in board]
        except Exception:
            pass

    # Allow one-line 16-number input
    flat_tokens = raw.replace(",", " ").split()
    if len(flat_tokens) == 16:
        try:
            vals = [int(x) for x in flat_tokens]
            return [vals[r * 4 : (r + 1) * 4] for r in range(4)]
        except ValueError:
            pass

    rows = []
    for _ in range(4):
        row = input().strip()
        if not row:
            raise ValueError("Board input cannot be empty.")
        parts = row.replace(",", " ").split()
        if len(parts) != 4:
            raise ValueError("Each row must contain exactly 4 numbers.")
        rows.append([int(x) for x in parts])

    return rows


def play_human_vs_computer():
    board = [[0 for _ in range(4)] for _ in range(4)]

    ans = input("Do you want to play first? (y/n): ").strip().lower()
    human_first = ans in ("y", "yes")

    human_player = 1 if human_first else 2
    computer_player = 3 - human_player

    k = int(input("Choose cutoff depth for the computer: "))

    turn = 1
    while True:
        display_board(board)

        if turn == human_player:
            r, c = prompt_move(board, human_player)
            board[r][c] = human_player
        else:
            print("Computer thinking...")
            value, move, nodes, elapsed = MinimaxAlphaBetaCutOff(board, k)
            if move is None:
                print("No legal moves remain.")
                break
            r, c = move
            board[r][c] = computer_player
            print(f"Computer plays at row {r+1}, col {c+1}")

        if has_win(board, 1) or has_win(board, 2):
            display_board(board)
            if has_win(board, human_player):
                print("You win!")
            else:
                print("Computer wins!")
            break

        if not legal_moves(board):
            display_board(board)
            print("Draw game.")
            break

        turn = 3 - turn


def main():
    while True:
        print("\nCS381 Project 3")
        print("0. Play against the computer")
        print("1. Evaluate a board using Minimax")
        print("2. Evaluate using MinimaxAlphaBetaCutOff")
        print("3. Compare MinimaxCutOff and MinimaxAlphaBetaCutOff")
        print("4. Exit")

        choice = input("Choose an option: ").strip()

        try:
            if choice == "0":
                play_human_vs_computer()

            elif choice == "1":
                board = parse_board_input()
                print("Minimax value:", Minimax(board))

            elif choice == "2":
                board = parse_board_input()
                k = int(input("Enter cutoff depth k: "))
                value, move, nodes, elapsed = MinimaxAlphaBetaCutOff(board, k)
                print("Value:", value)
                print("Best move:", move)
                print("Nodes expanded:", nodes)
                print("CPU time:", elapsed)

            elif choice == "3":
                board = parse_board_input()
                k = int(input("Enter cutoff depth k: "))
                value1, move1, nodes1, elapsed1 = MinimaxCutOff(board, k)
                value2, move2, nodes2, elapsed2 = MinimaxAlphaBetaCutOff(board, k)
                print("MinimaxCutOff:", value1, move1, nodes1, elapsed1)
                print("MinimaxAlphaBetaCutOff:", value2, move2, nodes2, elapsed2)

            elif choice == "4":
                print("Exiting.")
                break

            else:
                print("Invalid option.")

        except Exception as e:
            print("Error:", e)


if __name__ == "__main__":
    main()