def is_game_over(state):
    # Check rows, columns and diagonals for a win
    for i in range(3):
        if state[i][0] == state[i][1] == state[i][2] != 0:  # Rows
            return True
        if state[0][i] == state[1][i] == state[2][i] != 0:  # Columns
            return True
    if state[0][0] == state[1][1] == state[2][2] != 0:  # Main diagonal
        return True
    if state[0][2] == state[1][1] == state[2][0] != 0:  # Second diagonal
        return True

    # Check if there are no more moves left
    if any(0 in row for row in state):
        return False

    # It's a draw
    return True

def evaluate(state):
    # Check rows, columns and diagonals for a win
    for i in range(3):
        if state[i][0] == state[i][1] == state[i][2] != 0:  # Rows
            return 1 if state[i][0] == 1 else -1
        if state[0][i] == state[1][i] == state[2][i] != 0:  # Columns
            return 1 if state[0][i] == 1 else -1
    if state[0][0] == state[1][1] == state[2][2] != 0:  # Main diagonal
        return 1 if state[0][0] == 1 else -1
    if state[0][2] == state[1][1] == state[2][0] != 0:  # Second diagonal
        return 1 if state[0][2] == 1 else -1

    # It's a draw
    return 0

def get_children(state, player):
    children = []
    for i in range(3):
        for j in range(3):
            if state[i][j] == 0:
                new_state = [row.copy() for row in state]
                new_state[i][j] = player
                children.append(new_state)
    return children

def minimax(state, depth, maximizing_player):
    if depth == 0 or is_game_over(state):
        return evaluate(state)

    if maximizing_player:
        max_eval = float('-inf')
        for child in get_children(state, 1):
            eval = minimax(child, depth - 1, False)
            max_eval = max(max_eval, eval)
        return max_eval
    else:
        min_eval = float('inf')
        for child in get_children(state, 2):
            eval = minimax(child, depth - 1, True)
            min_eval = min(min_eval, eval)
        return min_eval
# Initial empty board
state = [
    [0, 0, 0],
    [0, 1, 0],
    [0, 0, 0]
]

# Call minimax function
best_score = minimax(state, 9, True)
print("The best achievable score is: ", best_score)