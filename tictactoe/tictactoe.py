"""
Tic Tac Toe Player
"""

import math

X = "X"
O = "O"
EMPTY = None

def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    if sum(row.count(X) for row in board) > sum(row.count(O) for row in board):
        return O
    else:
        return X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    possible_actions = set()
    
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == EMPTY:
                possible_actions.add((i, j))

    return possible_actions
    


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    # Create a deep copy of the board
    new_board = [row[:] for row in board]

    # Field is not allowed to be occupied already
    if board[action[0]][action[1]] != EMPTY:
        raise Exception("so nicht min jung!")
    # Field trying to occupy needs to be inside the limits
    if action[0] > len(board) or action[1] > len(board[0]):
        raise Exception("ich glaub es hackt!")
    # Field trying to occupy needs to be inside the limits
    if action[0] < 0 or action[1] < 0:
        raise Exception("das geht auch nicht!")
    else:
        new_board[action[0]][action[1]] = player(board)
        return new_board

def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # Do i need to check that the fields are not EMPTY?
    # Check rows and columns
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] != EMPTY:
            return board[i][0]
        if board[0][i] == board[1][i] == board[2][i] != EMPTY:
            return board[0][i]
    
    # Check diagonals
    if board[0][0] == board[1][1] == board[2][2] != EMPTY:
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != EMPTY:
        return board[0][2]
    
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) != None:
        return True
    
    for row in board:
        if EMPTY in row:
            return False
    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    else:
        return 0
    

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    # X tries to maximize score
    # O tries to minimize score
    if terminal(board):
        return None

    if player(board) == X:
        best_value = float('-inf')
        for action in actions(board):
            value = min_value(result(board, action))
            if value > best_value:
                best_value = value
                best_action = action
    else:
        best_value = float('inf')
        for action in actions(board):
            value = max_value(result(board, action))
            if value < best_value:
                best_value = value
                best_action = action
    
    return best_action
    

def max_value(board):
    if terminal(board):
        return utility(board)
    v = float('-inf')
    for action in actions(board):
        v = max(v, min_value(result(board,action)))
        
    return v

def min_value(board):
    if terminal(board):
        return utility(board)
    v = float('inf')
    for action in actions(board):
        v = min(v, max_value(result(board,action)))

    return v

