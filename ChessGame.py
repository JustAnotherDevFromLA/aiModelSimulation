import chess
import chess.engine

def print_board(board):
    """Prints the chess board in a readable format."""
    print("  a b c d e f g h")
    print(" +-----------------+")
    for rank in range(8, 0, -1):
        row = f"{rank}|"
        for file in range(8):
            piece = board.piece_at(chess.square(file, rank - 1))
            row += " " + (piece.symbol() if piece else ".")
        row += " |"
        print(row)
    print(" +-----------------+")
    print("  a b c d e f g h")

def get_move(board):
    """Prompts the user to input a move and validates it."""
    while True:
        move_input = input("Enter your move (e.g., e2e4): ").strip()
        if move_input.lower() == "quit":
            return None
        try:
            move = chess.Move.from_uci(move_input)
            if move in board.legal_moves:
                return move
            else:
                print("Illegal move. Try again.")
        except ValueError:
            print("Invalid move format. Use UCI notation (e.g., e2e4).")

def play_game():
    """Main function to play the chess game."""
    board = chess.Board()
    engine = chess.engine.SimpleEngine.popen_uci("C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Python 3.10\stockfish-windows-x86-64-avx2\stockfish\stockfish-windows-x86-64-avx2")  # Ensure Stockfish is installed

    print("Welcome to Python Chess!")
    print("Enter moves in UCI notation (e.g., e2e4). Type 'quit' to exit.")

    while not board.is_game_over():
        print_board(board)
        print(f"\nTurn: {'White' if board.turn == chess.WHITE else 'Black'}")

        if board.turn == chess.WHITE:
            # Human player's turn
            move = get_move(board)
            if move is None:
                print("Game ended by user.")
                break
            board.push(move)
        else:
            # Computer's turn (using Stockfish)
            result = engine.play(board, chess.engine.Limit(time=2.0))
            board.push(result.move)
            print(f"Computer plays: {result.move.uci()}")

    print_board(board)
    if board.is_checkmate():
        winner = "Black" if board.turn == chess.WHITE else "White"
        print(f"Checkmate! {winner} wins!")
    elif board.is_stalemate():
        print("Stalemate! It's a draw.")
    elif board.is_insufficient_material():
        print("Draw due to insufficient material.")
    elif board.is_seventyfive_moves():
        print("Draw by 75-move rule.")
    elif board.is_fivefold_repetition():
        print("Draw by fivefold repetition.")
    else:
        print("Game over.")

    engine.quit()

if __name__ == "__main__":
    play_game()
