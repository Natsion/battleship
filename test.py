# Global constants
BOARD_SIZE = 10  # Defines the size of the board (10x10)
LETTERS = "ABCDEFGHIJ"  # Letters to represent columns on the board
SHIP_SIZES = {  # Dictionary to define the ship sizes for different numbers of ships
    1: [1],  # 1 ship: 1x1
    2: [1, 2],  # 2 ships: 1x1, 1x2
    3: [1, 2, 3],  # 3 ships: 1x1, 1x2, 1x3
    4: [1, 2, 3, 4],  # 4 ships: 1x1, 1x2, 1x3, 1x4
    5: [1, 2, 3, 4, 5]  # 5 ships: 1x1, 1x2, 1x3, 1x4, 1x5
}


def print_board(board):
    """Prints the board with row and column labels."""
    print("  " + " ".join(LETTERS))  # Print the column letters
    for i in range(BOARD_SIZE):  # Loop through each row
        row = [str(cell) for cell in board[i]]  # Convert row cells to strings
        print(f"{i + 1:2} {' '.join(row)}")  # Print row index and its content


def create_empty_board():
    """Creates a 10x10 board filled with '~' to represent water."""
    return [['~'] * BOARD_SIZE for _ in range(BOARD_SIZE)]  # 2D list filled with '~'


def get_coordinates_input():
    """Prompts the player to enter valid coordinates."""
    while True:
        coordinates = input("Enter the coordinates (e.g., A5): ").strip().upper()  # Get input and format
        if len(coordinates) < 2:  # Check if input is too short
            print("Invalid input. Try again.")
            continue
        col = coordinates[0]  # Extract column part
        row = coordinates[1:]  # Extract row part
        if col in LETTERS and row.isdigit() and 1 <= int(row) <= 10:  # Validate coordinates
            return LETTERS.index(col), int(row) - 1  # Return column index and row index
        print("Invalid coordinates. Try again.")


def place_ship_on_board(board, size, ship_id):
    """Places a ship on the board after user inputs position and orientation."""
    while True:
        # Show the current state of the board
        print("\nCurrent board:")
        print_board(board)
        
        print(f"Placing ship of size {size}.")
        col, row = get_coordinates_input()  # Get coordinates for ship placement
        orientation = input("Enter orientation (H for Horizontal, V for Vertical): ").strip().upper()  # Get orientation

        if orientation == 'H':  # Place ship horizontally
            if col + size > BOARD_SIZE or any(board[row][col + i] != '~' for i in range(size)):  # Check if it fits
                print("Invalid placement. Try again.")
                continue
            for i in range(size):  # Place the ship on the board
                board[row][col + i] = ship_id
            break
        elif orientation == 'V':  # Place ship vertically
            if row + size > BOARD_SIZE or any(board[row + i][col] != '~' for i in range(size)):  # Check if it fits
                print("Invalid placement. Try again.")
                continue
            for i in range(size):  # Place the ship on the board
                board[row + i][col] = ship_id
            break
        else:
            print("Invalid orientation. Try again.")  # Invalid orientation error


def place_ships(board, ship_sizes):
    """Places all the ships on the board based on the number of ships."""
    for i, size in enumerate(ship_sizes):  # Loop over each ship size
        place_ship_on_board(board, size, f"S{i+1}")  # Call place_ship_on_board to place each ship


def check_hit_or_miss(board, row, col):
    """Checks if the shot is a hit or miss and updates the board."""
    if board[row][col].startswith("S"):  # Check if the shot hit a ship
        ship_id = board[row][col]
        board[row][col] = "X"  # Mark as hit
        return True, ship_id  # Return that it was a hit
    board[row][col] = "O"  # Mark as miss
    return False, None  # Return that it was a miss


def all_ships_sunk(ship_hits):
    """Checks if all ships are sunk by verifying hit counts."""
    return all(hit == 0 for hit in ship_hits.values())  # Return True if all ship hit counts are 0


def player_turn(opponent_board, opponent_ships, player_tracking_board):
    """Handles a player's turn to shoot at the opponent's board."""
    print("Your turn to shoot.")
    while True:
        col, row = get_coordinates_input()  # Get coordinates to shoot

        if player_tracking_board[row][col] != '~':  # Check if the location was already shot at
            print("You've already fired at this location. Try again.")
            continue

        hit, ship_id = check_hit_or_miss(opponent_board, row, col)  # Check if it's a hit or miss
        if hit:
            print("It's a hit!")
            opponent_ships[ship_id] -= 1  # Decrease the remaining hit count of the ship
            player_tracking_board[row][col] = "X"  # Mark the hit on the tracking board
            if opponent_ships[ship_id] == 0:  # Check if the ship is sunk
                print(f"You sunk the opponent's {ship_id}!")
        else:
            print("It's a miss.")
            player_tracking_board[row][col] = "O"  # Mark the miss on the tracking board
        break  # End the turn


def setup_game():
    """Sets up the game boards and ships for both players."""
    # Get the number of ships from the user
    while True:
        num_ships = input("Enter number of ships (1-5): ").strip()  # Ask how many ships
        if num_ships.isdigit() and 1 <= int(num_ships) <= 5:  # Validate input
            num_ships = int(num_ships)
            break
        print("Invalid number of ships. Please enter a value between 1 and 5.")

    # Set up player boards and ships
    player_board = create_empty_board()  # Create Player 1's board
    opponent_board = create_empty_board()  # Create Player 2's board

    print("Player 1, place your ships.")
    place_ships(player_board, SHIP_SIZES[num_ships])  # Player 1 places ships

    print("Player 2, place your ships.")
    place_ships(opponent_board, SHIP_SIZES[num_ships])  # Player 2 places ships

    # Initialize tracking boards (for firing results)
    player_tracking_board = create_empty_board()  # Player 1's tracking board
    opponent_tracking_board = create_empty_board()  # Player 2's tracking board

    # Create dictionaries to track ship hits
    player_ships = {f"S{i+1}": SHIP_SIZES[num_ships][i] for i in range(num_ships)}  # Player 1 ship hit count
    opponent_ships = {f"S{i+1}": SHIP_SIZES[num_ships][i] for i in range(num_ships)}  # Player 2 ship hit count

    return (player_board, opponent_board, player_tracking_board, opponent_tracking_board, player_ships, opponent_ships)


def main():
    """Main game loop that controls the flow of the game."""
    print("Welcome to Battleship!")
    
    (player_board, opponent_board, player_tracking_board, opponent_tracking_board, player_ships, opponent_ships) = setup_game()  # Set up the game

    # Game loop
    while True:
        # Player 1's turn
        print("\nPlayer 1's turn.")
        print("Your board:")
        print_board(player_board)  # Display Player 1's board
        print("\nYour tracking board:")
        print_board(player_tracking_board)  # Display Player 1's tracking board

        player_turn(opponent_board, opponent_ships, player_tracking_board)  # Player 1 takes a turn
        if all_ships_sunk(opponent_ships):  # Check if Player 1 wins
            print("Player 1 wins! You sank all the opponent's ships!")
            break

        # Player 2's turn
        print("\nPlayer 2's turn.")
        print("Your board:")
        print_board(opponent_board)  # Display Player 2's board
        print("\nYour tracking board:")
        print_board(opponent_tracking_board)  # Display Player 2's tracking board

        player_turn(player_board, player_ships, opponent_tracking_board)  # Player 2 takes a turn
        if all_ships_sunk(player_ships):  # Check if Player 2 wins
            print("Player 2 wins! You sank all the opponent's ships!")
            break


if __name__ == "__main__":
    main()  # Run the game if executed directly
