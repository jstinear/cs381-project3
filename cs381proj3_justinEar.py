from __future__ import annotations

import itertools
import math
import time
from typing import Iterable, List, Sequence, Tuple, Union

BOARD_SIZE = 4
EMPTY = 0
VALID_VALUES = {0, 1, 2}


def _normalize_board(board: Sequence[Sequence[int]]) -> List[List[int]]:
    """Convert input into a 4x4 list-of-lists board."""
    if isinstance(board, (list, tuple)) and len(board) == 4 and all(
        isinstance(row, (list, tuple)) for row in board
    ):
        rows = [list(row) for row in board]
        if all(len(r) == 4 for r in rows):
            return rows

    if isinstance(board, (list, tuple)) and len(board) == 16:
        flat = [int(v) for v in board]
        return [flat[r * 4 : (r + 1) * 4] for r in range(4)]

    raise ValueError("Board must be a 4x4 matrix or a flat 16-element list.")


def _winner(board: Sequence[Sequence[int]], player: int) -> bool:
    """Return True if player has a winning set of four cells."""
    if player not in (1, 2):
        raise ValueError("player must be 1 or 2")

    cells = [
        (r, c)
        for r in range(BOARD_SIZE)
        for c in range(BOARD_SIZE)
        if board[r][c] == player
    ]
    if len(cells) < 4:
        return False

    for combo in itertools.combinations(cells, 4):
        rows = {r for r, _ in combo}
        cols = {c for _, c in combo}
        if len(rows) == 4 and len(cols) == 4:
            return True
    return False


def _winning_sets(board: Sequence[Sequence[int]], player: int) -> int:
    """Count the number of winning 4-cell sets for the given player."""
    cells = [
        (r, c)
        for r in range(BOARD_SIZE)
        for c in range(BOARD_SIZE)
        if board[r][c] == player
    ]
    total = 0
    for combo in itertools.combinations(cells, 4):
        rows = {r for r, _ in combo}
        cols = {c for _, c in combo}
        if len(rows) == 4 and len(cols) == 4:
            total += 1
    return total


def _legal_moves(board: Sequence[Sequence[int]]) -> List[Tuple[int, int]]:
    """Return a sorted list of empty positions as (row, col), 1-based indexes."""
    return [
        (r, c)
        for r in range(BOARD_SIZE)
        for c in range(BOARD_SIZE)
        if board[r][c] == EMPTY
    ]


def _apply_move(board: Sequence[Sequence[int]], move: Tuple[int, int], player: int) -> List[List[int]]:
    """Return a board with move applied for the given player."""
    row, col = move
    b = [list(r) for r in board]
    if not (0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE):
        raise ValueError("Move is outside the board.")
    if b[row][col] != EMPTY:
        raise ValueError("Move is not legal on an empty square.")
    b[row][col] = player
    return b


def _current_player(board: Sequence[Sequence[int]]) -> int:
    """Determine whose turn it is based on the move counts."""
    one_count = sum(cell == 1 for row in board for cell in row)
    two_count = sum(cell == 2 for row in board for cell in row)

    if one_count == two_count:
        return 1
    if one_count == two_count + 1:
        return 2
    raise ValueError("Board has an invalid move count sequence.")


def _terminal_result(board: Sequence[Sequence[int]]) -> int:
    """Return 1 if player 1 has won, -1 if player 2 has won, else 0."""
    if _winner(board, 1):
        return 1
    if _winner(board, 2):
        return -1
    return 0


def _utility_for_player(board: Sequence[Sequence[int]], root_player: int) -> int:
    """Convert an end-state result into the value for the root player."""
    result = _terminal_result(board)
    if result == 0:
        return 0
    if root_player == 1:
        return result
    return -result


def checkValid(board: Sequence[Sequence[int]]) -> bool:
    """Return True if the board is a valid game state or completed game."""
    try:
        b = _normalize_board(board)
    except ValueError:
        return False

    if any(cell not in VALID_VALUES for row in b for cell in row):
        return False

    one_count = sum(cell == 1 for row in b for cell in row)
    two_count = sum(cell == 2 for row in b for cell in row)

    if abs(one_count - two_count) > 1:
        return False
    if not (one_count == two_count or one_count == two_count + 1):
        return False

    p1_win = _winner(b, 1)
    p2_win = _winner(b, 2)
    if p1_win and p2_win:
        return False
    if p1_win and one_count <= two_count:
        return False
    if p2_win and one_count != two_count:
        return False

    return True


def Minimax(board: Sequence[Sequence[int]]) -> int:
    """Return the game-theoretic value of a valid board: 1,0,-1."""
    b = _normalize_board(board)
    if not checkValid(b):
        raise ValueError("Invalid board.")

    current = _current_player(b)

    def solve(state: List[List[int]], turn: int) -> int:
        result = _terminal_result(state)
        if result != 0:
            return result
        if not _legal_moves(state):
            return 0

        if turn == 1:
            best = -2
            for move in _legal_moves(state):
                child = _apply_move(state, move, 1)
                best = max(best, solve(child, 2))
            return best

        best = 2
        for move in _legal_moves(state):
            child = _apply_move(state, move, 2)
            best = min(best, solve(child, 1))
        return best

    return solve(b, current)


def eval(board: Sequence[Sequence[int]], p: int) -> int:
    """Static evaluation for a board from the point of view of player p."""
    b = _normalize_board(board)
    if not checkValid(b):
        raise ValueError("Invalid board.")
    if p not in (1, 2):
        raise ValueError("p must be 1 or 2")

    opponent = 3 - p
    return _winning_sets(b, p) - _winning_sets(b, opponent)


def MinimaxCutOff(board: Sequence[Sequence[int]], k: int):
    """Depth-limited minimax search. Returns (value, best_move, nodes, elapsed_seconds)."""
    if k < 0:
        raise ValueError("k must be non-negative")

    b = _normalize_board(board)
    if not checkValid(b):
        raise ValueError("Invalid board.")

    root_player = _current_player(b)
    start = time.perf_counter()
    nodes = 0

    def search(state: List[List[int]], depth: int, turn: int) -> int:
        nonlocal nodes
        nodes += 1

        result = _terminal_result(state)
        if result != 0:
            return _utility_for_player(state, root_player)
        if depth == 0 or not _legal_moves(state):
            return eval(state, root_player)

        moves = _legal_moves(state)
        if turn == root_player:
            best = -math.inf
            for move in moves:
                child = _apply_move(state, move, turn)
                value = search(child, depth - 1, 3 - turn)
                best = max(best, value)
            return best

        best = math.inf
        for move in moves:
            child = _apply_move(state, move, turn)
            value = search(child, depth - 1, 3 - turn)
            best = min(best, value)
        return best

    moves = _legal_moves(b)
    if not moves:
        return 0, None, nodes, time.perf_counter() - start

    best_move = None
    best_value = -math.inf
    for move in sorted(moves):
        child = _apply_move(b, move, root_player)
        value = search(child, k - 1, 3 - root_player)
        if value > best_value:
            best_value = value
            best_move = move
        elif value == best_value:
            if move < best_move if best_move is not None else True:
                best_move = move

    result = (best_value, best_move, nodes, time.perf_counter() - start)
    return result


def MinimaxAlphaBetaCutOff(board: Sequence[Sequence[int]], k: int):
    """Depth-limited alpha-beta minimax search. Returns (value, best_move, nodes, elapsed_seconds)."""
    if k < 0:
        raise ValueError("k must be non-negative")

    b = _normalize_board(board)
    if not checkValid(b):
        raise ValueError("Invalid board.")

    root_player = _current_player(b)
    start = time.perf_counter()
    nodes = 0

    def search(state: List[List[int]], depth: int, turn: int, alpha: int, beta: int) -> int:
        nonlocal nodes
        nodes += 1

        result = _terminal_result(state)
        if result != 0:
            return _utility_for_player(state, root_player)
        if depth == 0 or not _legal_moves(state):
            return eval(state, root_player)

        moves = _legal_moves(state)
        if turn == root_player:
            best = -math.inf
            for move in moves:
                child = _apply_move(state, move, turn)
                value = search(child, depth - 1, 3 - turn, alpha, beta)
                if value > best:
                    best = value
                if best > alpha:
                    alpha = best
                if beta <= alpha:
                    break
            return best

        best = math.inf
        for move in moves:
            child = _apply_move(state, move, turn)
            value = search(child, depth - 1, 3 - turn, alpha, beta)
            if value < best:
                best = value
            if best < beta:
                beta = best
            if beta <= alpha:
                break
        return best

    moves = _legal_moves(b)
    if not moves:
        return 0, None, nodes, time.perf_counter() - start

    best_move = None
    best_value = -math.inf
    alpha = -math.inf
    beta = math.inf
    for move in sorted(moves):
        child = _apply_move(b, move, root_player)
        value = search(child, k - 1, 3 - root_player, alpha, beta)
        if value > best_value:
            best_value = value
            best_move = move
            alpha = max(alpha, best_value)
        elif value == best_value and (best_move is None or move < best_move):
            best_move = move

    elapsed = time.perf_counter() - start
    return best_value, best_move, nodes, elapsed


def _display_board(board: Sequence[Sequence[int]]) -> None:
    """Print the board in a human-friendly format."""
    b = _normalize_board(board)
    print()
    for row in b:
        print(" ".join(str(cell) for cell in row))
    print()


def _parse_board_input(prompt: str = "Enter the board as 4 rows of 4 numbers separated by spaces:") -> List[List[int]]:
    """Read a board from the user. Accepts 4 lines or one line with 16 numbers."""
    print(prompt)
    lines = []
    for _ in range(4):
        raw = input().strip()
        if not raw:
            raise ValueError("Board input cannot be empty.")
        parts = raw.split()
        if len(parts) == 4:
            values = [int(p) for p in parts]
            lines.append(values)
        elif len(parts) == 16:
            flat = [int(p) for p in parts]
            lines = [flat[r * 4 : (r + 1) * 4] for r in range(4)]
            break
        else:
            raise ValueError("Each row must contain exactly 4 numbers.")
    return lines


def _prompt_move(board: Sequence[Sequence[int]], marker: int) -> Tuple[int, int]:
    """Prompt the user for a move on a 1-based (row, col) system."""
    while True:
        try:
            text = input(f"Player {marker}: enter move as row col (1-4 each): ")
            parts = text.split()
            if len(parts) != 2:
                raise ValueError
            row = int(parts[0]) - 1
            col = int(parts[1]) - 1
            if not (0 <= row < 4 and 0 <= col < 4):
                raise ValueError
            if board[row][col] != 0:
                raise ValueError
            return (row, col)
        except Exception:
            print("Invalid move. Please enter two integers between 1 and 4 for row and column.")


def _play_human_vs_computer() -> None:
    """Human vs computer mode."""
    board = [[0 for _ in range(4)] for _ in range(4)]
    answer = input("Do you want to play first? (y/n): ").strip().lower()
    human_first = answer in {"y", "yes", "1"}
    human_marker = 1 if human_first else 2
    computer_marker = 3 - human_marker
    depth = int(input("Choose the cutoff depth for the computer: "))

    turn = 1
    while True:
        _display_board(board)
        if turn == human_marker:
            row, col = _prompt_move(board, human_marker)
            board[row][col] = human_marker
        else:
            print("Computer is thinking...")
            value, move, nodes, elapsed = MinimaxAlphaBetaCutOff(board, depth)
            if move is None:
                break
            row, col = move
            board[row][col] = computer_marker
            print(f"Computer chooses row {row + 1}, col {col + 1}.")

        if _winner(board, 1):
            _display_board(board)
            if human_marker == 1:
                print("You win!")
            else:
                print("Computer wins!")
            break
        if _winner(board, 2):
            _display_board(board)
            if human_marker == 2:
                print("You win!")
            else:
                print("Computer wins!")
            break
        if not _legal_moves(board):
            _display_board(board)
            print("The board is full. It is a draw.")
            break

        turn = 3 - turn


def _play_user_vs_computer() -> None:
    """Human chooses the board and marker, while the computer plays the other side."""
    board = _parse_board_input()
    if not checkValid(board):
        raise ValueError("The entered board is invalid.")

    choice = input("Choose your marker: 1 or 2: ").strip()
    while choice not in {"1", "2"}:
        choice = input("Invalid choice. Choose 1 or 2: ").strip()
    human_marker = int(choice)
    computer_marker = 3 - human_marker
    depth = int(input("Choose the cutoff depth for the computer: "))

    turn = _current_player(board)
    while True:
        _display_board(board)
        if turn == human_marker:
            row, col = _prompt_move(board, human_marker)
            board[row][col] = human_marker
        else:
            print("Computer is thinking...")
            value, move, nodes, elapsed = MinimaxAlphaBetaCutOff(board, depth)
            if move is None:
                print("No move available.")
                break
            row, col = move
            board[row][col] = computer_marker
            print(f"Computer chooses row {row + 1}, col {col + 1}.")

        if _winner(board, 1):
            _display_board(board)
            if human_marker == 1:
                print("You win!")
            else:
                print("Computer wins!")
            break
        if _winner(board, 2):
            _display_board(board)
            if human_marker == 2:
                print("You win!")
            else:
                print("Computer wins!")
            break
        if not _legal_moves(board):
            _display_board(board)
            print("The board is full. It is a draw.")
            break

        turn = 3 - turn


def main() -> None:
    """Interactive menu-driven main program."""
    while True:
        print("\nCS381 Project 3")
        print("0. Play against the computer")
        print("1. Evaluate a board using Minimax")
        print("2. Evaluate a board using MinimaxAlphaBeta with cutoff")
        print("3. Compare MinimaxCutOff and MinimaxAlphaBetaCutOff")
        print("4. Human vs computer game with chosen marker")
        print("5. Exit")

        choice = input("Select an option: ").strip()
        try:
            if choice == "0":
                _play_human_vs_computer()
            elif choice == "1":
                board = _parse_board_input()
                print(f"Minimax value: {Minimax(board)}")
            elif choice == "2":
                board = _parse_board_input()
                depth = int(input("Enter cutoff depth k: "))
                value, move, nodes, elapsed = MinimaxAlphaBetaCutOff(board, depth)
                print(f"Value: {value}")
                print(f"Best move: {move}")
                print(f"Nodes expanded: {nodes}")
                print(f"CPU time: {elapsed:.6f} seconds")
            elif choice == "3":
                board = _parse_board_input()
                depth = int(input("Enter cutoff depth k: "))
                val1, move1, nodes1, elapsed1 = MinimaxCutOff(board, depth)
                val2, move2, nodes2, elapsed2 = MinimaxAlphaBetaCutOff(board, depth)
                print(f"MinimaxCutOff: value={val1}, best_move={move1}, nodes={nodes1}, time={elapsed1:.6f}s")
                print(f"AlphaBetaCutOff: value={val2}, best_move={move2}, nodes={nodes2}, time={elapsed2:.6f}s")
            elif choice == "4":
                _play_user_vs_computer()
            elif choice == "5":
                print("Goodbye!")
                break
            else:
                print("Invalid option. Please enter a number from 0 to 5.")
        except Exception as exc:
            print(f"Error: {exc}")


if __name__ == "__main__":
    main()

__all__ = [
    "BOARD_SIZE",
    "checkValid",
    "Minimax",
    "eval",
    "MinimaxCutOff",
    "MinimaxAlphaBetaCutOff",
    "main",
]


# End of file
""""""
