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

<<<<<<< HEAD
    # If player 1 wins, player 1 must have exactly one more move than player 2
    if p1_win and p1 <= p2:
        return False

    # If player 2 wins, player 2 must not have more pieces than player 1
=======
    # If player 1 wins, player 1 must have exactly one more move than player 2.
    if p1_win and p1 <= p2:
        return False

    # If player 2 wins, the move counts must be equal.
>>>>>>> 4fed33cc0ee005a803867be0f57b2d0b602618ba
    if p2_win and p2 > p1:
        return False

    return True


def has_win(board, player):
<<<<<<< HEAD
    """True if player has a 4-cell capture with all distinct rows and cols."""
=======
    """True if player has a 4-cell capture with all distinct rows and columns."""
>>>>>>> 4fed33cc0ee005a803867be0f57b2d0b602618ba
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
<<<<<<< HEAD
    """
    Static evaluation:
      e(B, p) = number of ways player p can win - number of ways opponent can win
    """
=======
    """Return the number of winning sets for p minus the opponent's winning sets."""
>>>>>>> 4fed33cc0ee005a803867be0f57b2d0b602618ba
    if not checkValid(board):
        raise ValueError("Invalid board for eval()")
    if p not in (1, 2):
        raise ValueError("Player must be 1 or 2")

<<<<<<< HEAD
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
=======
    opponent = 3 - p
    return count_wins(board, p) - count_wins(board, opponent)


def legal_moves(board):
    """Return empty positions as (row, column), using zero-based indexes."""
    return [
        (r, c)
        for r in range(4)
        for c in range(4)
        if board[r][c] == EMPTY
    ]
>>>>>>> 4fed33cc0ee005a803867be0f57b2d0b602618ba


def apply_move(board, move, player):
    """Return a new board with the move applied."""
    r, c = move
    new_board = [row[:] for row in board]
<<<<<<< HEAD
    if new_board[r][c] != 0:
=======
    if new_board[r][c] != EMPTY:
>>>>>>> 4fed33cc0ee005a803867be0f57b2d0b602618ba
        raise ValueError("Illegal move")
    new_board[r][c] = player
    return new_board


def current_player(board):
<<<<<<< HEAD
    """Determine whose turn it should be based on the move counts."""
=======
    """Determine whose turn it is based on the move counts."""
>>>>>>> 4fed33cc0ee005a803867be0f57b2d0b602618ba
    p1 = sum(cell == 1 for row in board for cell in row)
    p2 = sum(cell == 2 for row in board for cell in row)

    if p1 == p2:
        return 1
    if p1 == p2 + 1:
        return 2
    raise ValueError("Board has an impossible move count")


def terminal_value(board):
<<<<<<< HEAD
    """
    Return 1 if player 1 has won, -1 if player 2 has won, 0 otherwise.
    """
=======
    """Return 1 if player 1 won, -1 if player 2 won, or 0 if no winner."""
>>>>>>> 4fed33cc0ee005a803867be0f57b2d0b602618ba
    if has_win(board, 1):
        return 1
    if has_win(board, 2):
        return -1
    return 0


def Minimax(board):
<<<<<<< HEAD
    """
    Return the value of the board:
      1 if player 1 can force a win
      0 if neither player can force a win
     -1 if player 2 can force a win

    This is the full minimax implementation for Option 1. It may take a long time for
    sparse boards because the game tree is large; that is expected.
    """
=======
    """Return 1 if player 1 can force a win, 0 for a draw, or -1 for player 2."""
>>>>>>> 4fed33cc0ee005a803867be0f57b2d0b602618ba
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
<<<<<<< HEAD
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

=======
                best = max(best, solve(apply_move(state, move, 1), 2))
            return best

        best = 2
        for move in moves:
            best = min(best, solve(apply_move(state, move, 2), 1))
        return best

>>>>>>> 4fed33cc0ee005a803867be0f57b2d0b602618ba
    return solve(board, current_player(board))


def MinimaxCutOff(board, k):
<<<<<<< HEAD
    """
    Minimax search to depth k.
    Returns: (value, best_move, nodes_expanded, elapsed_time)
    best_move is chosen with smaller row, smaller col tie-break.
    The returned value is for the root player.
    """
=======
    """Depth-limited minimax; return (value, best_move, nodes, elapsed_seconds)."""
>>>>>>> 4fed33cc0ee005a803867be0f57b2d0b602618ba
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
<<<<<<< HEAD
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
=======
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
    """Depth-limited alpha-beta search; return (value, move, nodes, elapsed_seconds)."""
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
>>>>>>> 4fed33cc0ee005a803867be0f57b2d0b602618ba

    return best_value, best_move, nodes, time.perf_counter() - start


<<<<<<< HEAD
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


=======
>>>>>>> 4fed33cc0ee005a803867be0f57b2d0b602618ba
def display_board(board):
    for row in board:
        print(" ".join(str(cell) for cell in row))
    print()


def prompt_move(board, player):
<<<<<<< HEAD
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
=======
    """Prompt for an empty square, with row and column numbered 1 through 4."""
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
    """Read a board as a nested list, 16 values on one line, or four rows."""
>>>>>>> 4fed33cc0ee005a803867be0f57b2d0b602618ba
    raw = input("Enter the board: ").strip()

    if raw.startswith("["):
        try:
            board = ast.literal_eval(raw)
<<<<<<< HEAD
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
=======
            if (isinstance(board, (list, tuple)) and len(board) == 4
                    and all(isinstance(row, (list, tuple)) and len(row) == 4 for row in board)):
                return [[int(value) for value in row] for row in board]
        except (ValueError, SyntaxError, TypeError):
            pass

    tokens = raw.replace(",", " ").split()
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
    """Keep prompting until a valid board is entered."""
    while True:
        board = parse_board_input()
        if checkValid(board):
            return board
        print("That board is invalid. Please enter a valid board.")


def _announce_result(board, human_player):
    """Display the finished board and report the winner or draw."""
    display_board(board)
    if has_win(board, human_player):
        print("You win!")
    elif has_win(board, 3 - human_player):
        print("Computer wins!")
    else:
        print("The game is a draw.")


def play_human_vs_computer():
    """Option 0: play from an empty board, choosing whether the human starts."""
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
>>>>>>> 4fed33cc0ee005a803867be0f57b2d0b602618ba

    turn = 1
    while True:
        display_board(board)
<<<<<<< HEAD

=======
>>>>>>> 4fed33cc0ee005a803867be0f57b2d0b602618ba
        if turn == human_player:
            r, c = prompt_move(board, human_player)
            board[r][c] = human_player
        else:
            print("Computer thinking...")
<<<<<<< HEAD
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
=======
            _, move, _, _ = MinimaxAlphaBetaCutOff(board, depth)
            if move is None:
                break
            r, c = move
            board[r][c] = computer_player
            print(f"Computer plays at row {r + 1}, column {c + 1}.")
>>>>>>> 4fed33cc0ee005a803867be0f57b2d0b602618ba

        if has_win(board, 1) or has_win(board, 2) or not legal_moves(board):
            _announce_result(board, human_player)
            return
        turn = 3 - turn


<<<<<<< HEAD
=======
def play_from_entered_board():
    """Option 4: continue a valid entered position against the computer."""
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


>>>>>>> 4fed33cc0ee005a803867be0f57b2d0b602618ba
def main():
    while True:
        print("\nCS381 Project 3")
        print("0. Play against the computer from an empty board")
        print("1. Evaluate a board using Minimax")
        print("2. Evaluate using MinimaxAlphaBetaCutOff")
        print("3. Compare MinimaxCutOff and MinimaxAlphaBetaCutOff")
<<<<<<< HEAD
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
=======
        print("4. Play against the computer from a valid board")
        print("5. Exit")

        choice = input("Choose an option: ").strip()

        try:
            if choice == "0":
                play_human_vs_computer()
            elif choice == "1":
                board = parse_board_input()
                print("Minimax value:", Minimax(board))
            elif choice == "2":
                board = parse_board_input()
                depth = int(input("Enter cutoff depth k: "))
                value, move, nodes, elapsed = MinimaxAlphaBetaCutOff(board, depth)
>>>>>>> 4fed33cc0ee005a803867be0f57b2d0b602618ba
                print("Value:", value)
                print("Best move:", move)
                print("Nodes expanded:", nodes)
                print("CPU time:", elapsed)
<<<<<<< HEAD

            elif choice == "3":
                board = parse_board_input()
                k = int(input("Enter cutoff depth k: "))
                value1, move1, nodes1, elapsed1 = MinimaxCutOff(board, k)
                value2, move2, nodes2, elapsed2 = MinimaxAlphaBetaCutOff(board, k)
                print("MinimaxCutOff:", value1, move1, nodes1, elapsed1)
                print("MinimaxAlphaBetaCutOff:", value2, move2, nodes2, elapsed2)

            elif choice == "4":
=======
            elif choice == "3":
                board = parse_board_input()
                depth = int(input("Enter cutoff depth k: "))
                value1, move1, nodes1, elapsed1 = MinimaxCutOff(board, depth)
                value2, move2, nodes2, elapsed2 = MinimaxAlphaBetaCutOff(board, depth)
                print("MinimaxCutOff:", value1, move1, nodes1, elapsed1)
                print("MinimaxAlphaBetaCutOff:", value2, move2, nodes2, elapsed2)
            elif choice == "4":
                play_from_entered_board()
            elif choice == "5":
>>>>>>> 4fed33cc0ee005a803867be0f57b2d0b602618ba
                print("Exiting.")
                break

            else:
<<<<<<< HEAD
                print("Invalid option.")

        except Exception as e:
            print("Error:", e)


if __name__ == "__main__":
    main()
=======
                print("Invalid option. Choose a number from 0 to 5.")
        except (ValueError, TypeError) as error:
            print("Error:", error)


if __name__ == "__main__":
    main()
>>>>>>> 4fed33cc0ee005a803867be0f57b2d0b602618ba
