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
    flatten = [item for row in board for item in row]
    if flatten.count(X) > flatten.count(O):
        return O
    else:
        return X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    return {(i,j) for i, row in enumerate(board)
            for j,item in enumerate(row) if item is None}


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    #for row in board:
    #    print(row)
    #print(action)
    
    if board[action[0]][action[1]] is not None:
        raise ValueError('Invalid action')
    import copy
    newboard = copy.deepcopy(board)
    newboard[action[0]][action[1]] = player(board)
    return newboard


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # check rows for winner
    for row in board:
        if all([item == row[0] for item in row]) and row[0]:
            return row[0]

    # check cols for winner
    for i in range(3):
        col = [row[i] for row in board]
        if all([item == col[0] for item in col]) and col[0]:
            return col[0]

    # check diagonals
    diagonal = [board[i][i] for i in range(3)]
    if all([item == diagonal[0] for item in diagonal]) and diagonal[0]:
        return diagonal[0]
    diagonal = [board[i][2-i] for i in range(3)]
    if all([item == diagonal[0] for item in diagonal]) and diagonal[0]:
        return diagonal[0]

    # There is no winner
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    return winner(board) or all([cell for row in board for cell in row])


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    # For me the most natural way to approach this problem would be
    # to extent this function to all boards, but this would contradict
    # some part of the instructions, so I didn't do that.
    valmap = {X: 1, O: -1, None: 0}
    return valmap[winner(board)]


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """

    # we will recursively iterate through the moves available.
    # for each move, 
    # we will keep track of the moves computed (and their utility)
    # using a dict whose keys are 0, -1, 1 and whose values are
    # lists of moves.  As soon as we find a move with utility 1
    # (for player X), we can return that move; this is  A*-pruning.

    
    
    # check for a terminal board
    if terminal(board):
        return None

    # 
    avail_moves = actions(board)
    moveutils = {1:[], 0:[], -1:[]}

    if player(board) == X:
        for move in avail_moves:

            # determin the utility of the current move
            # then add it to the dictionary
            moveutils[min_value(result(board, move))].append(move)

            # if a winning move has been fonud, take it
            if len(moveutils[1])>0:
                return moveutils[1][0]

            # otherwise, keep searching

        # no winning move is available
        # choose from among the best available moves
        bestutil = max([key for key, val in moveutils.items() if len(val)>0])
        return moveutils[bestutil][0]
    
    else: #player(board) == O
        for move in avail_moves:
            
            # determin the utility of the current move
            # then add it to the dictionary
            moveutils[max_value(result(board, move))].append(move)

            # if a winning move has been fonud, take it
            if len(moveutils[-1])>0:
                return moveutils[-1][0]

            # otherwise, keep searching

        # no winning move is available
        # choose from among the best available moves
        bestutil = min([key for key, val in moveutils.items() if len(val)>0])
        return moveutils[bestutil][0]
    
        
def max_value(board):
    # make a set to hold the utility values of subsequent boards
    # This is preferable to using math.inf because the utility
    # values have a known bound
    
    v = {-2}

    # if the board is terminal, return its utility
    if terminal(board):
        return utility(board)

    # otherwise, iterate through available moves
    # for each one, compute the utility (to min_player)
    # of result(board, move)
    # add this value to the set
    
    for move in actions(board):
        v.add(min_value(result(board, move)))

        # if ever a winning move has been found, we can halt
        if 1 in v:
            return 1
    return max(v)

def min_value(board):
    # make a set to hold the utility values of subsequent boards
    # This is preferable to using math.inf because the utility
    # values have a known bound

    v = {2}

    # if the board is terminal, return its utility    
    if terminal(board):
        return utility(board)

    # otherwise, iterate through available moves
    # for each one, compute the utility (to max_player)
    # of result(board, move)
    # add this value to the set
    
    for move in actions(board):
        v.add(max_value(result(board, move)))

        # if ever a winning move has been found, we can halt
        if -1 in v:
            return -1
    return min(v)
