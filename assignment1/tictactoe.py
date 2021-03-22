# Brian Koh
# a1782291
# Artificial Intelligence Assignment 1
# usage : $ python tictactoe.py [state] [path]

import math
import sys
import string

#player1 is maximizer
#player2 is minimizer
player1 = 'x'
player2 = 'o'

# checks if board is playable
def CheckBoard(b): 
    # nested for loop to check for empty squares
    for i in range(3):
        for j in range(3):
            if (b[i][j] == "-"):
                return True
    return False

# checks the board, checking for victories between player1 and player2 
def EvaluateBoard(b):

    # check for rows 
    # checking for victory between 'x' and 'o'
    # needs 3 in a row to consider a victory
    for row in range(3):
        if ( (b[row][0] == b[row][1]) and (b[row][1] == b[row][2]) ):  
            if b[row][0] == player1: 
                return 1 
            elif b[row][0] == player2:  
                return -1
    
    # check for columns
    for col in range(3):
        if ( (b[0][col] == b[1][col]) and (b[1][col] == b[2][col]) ):
            if b[0][col] == player1: 
                return 1
            elif b[0][col] == player2:  
                return -1

    # check for diagonals left to right
    if ( (b[0][0] == b[1][1]) and (b[1][1] == b[2][2]) ):
        if b[2][2] == player1:
            return 1
        elif b[2][2] == player2:
            return -1

    # check for diagonals right to left
    if ( (b[0][2] == b[1][1]) and (b[1][1] == b[2][0]) ):  
        if ( b[2][0] == player1 ):
            return 1 
        elif ( b[2][0] == player2 ):
            return -1

    # else if none satisfied 
    return 0

# calculates the next best move 
# assume that player1 / minimizer starts first
def minimax(b, depth, isMax):

    score = EvaluateBoard(b)

    # player1 wins
    if (score == 1): 
        return score
    # # #x + " " + str(best) + '\n')player2 wins
    if (score == -1):
        return score
    # tie
    if (CheckBoard(b) == False):
        return 0
    
    # if game is not done then call minimax function 
    # if player 1's move
    if (isMax) :     
        best = -1000
        # Traverse all cells 
        for i in range(3) :
            for j in range(3) :
                # Check if cell is empty 
                if (b[i][j] == '-') :
                    # Make the move for 'x'
                    b[i][j] = player1
                    # Call minimax recursively and choose the maximum value 
                    best = max( best, minimax(b, depth+1, not isMax) )
                    # Undo the move 
                    b[i][j] = '-'
        return best
    
    # If this minimizer's move 
    elif (not isMax) :
        best = 1000
        # Traverse all cells 
        for i in range(3) :
            for j in range(3) :
                # Check if cell is empty 
                if (b[i][j] == '-') :
                    # Make the move for 'o'
                    b[i][j] = player2
                    # Call minimax recursively and choose the minimum value 
                    best = min(best, minimax(b, depth+1, not isMax))
                    print "best " + str(best)
                    # Undo the move 
                    b[i][j] = '-'
        return best


# This will return the best possible next move for the player and its state
def findBestMove(b):
    bestVal = -1000
    bestMove = (-1, -1)
    # Traverse all cells, evaluate minimax function for 
    # all empty cells. And return the cell with optimal value. 
    for i in range(3) :
        for j in range(3) :
            # Check if cell is empty 
            if (b[i][j] == '-') :
                # Make the move 
                b[i][j] = player1
                # compute evaluation function for this move. 
                currVal = minimax(b, 0, False)
                # print currVal
                # Undo the move 
                b[i][j] = '-'
                # If the value of the current move is 
                # more than the best value, then update best 
                if (currVal > bestVal) :
                    bestMove = (i, j)
                    bestVal = currVal
    
    return bestMove , bestVal


# main function
if __name__ == "__main__":

    # if sys.argv[1] is None or sys.argv[2] is None:
    #    print "usage : $ python2 tictactoe.py [state] [output] "

    # reset file
    file = open(sys.argv[2], "w")
    file.write("")
    file.close()

    # capture string input
    board = sys.argv[1]

    # append string into 2d array
    a = []

    for x in board:
        a.append(x)

    b = [[],[],[]]

    list_count = 0

    for y in a:
        if list_count <= 5 and list_count >= 3:
            b[1].append(y)
        elif list_count <= 8 and list_count >= 6:
            b[2].append(y)
        elif list_count <= 2 and list_count >= 0:
            b[0].append(y)
        list_count += 1

    # print(b)
    bestMove = findBestMove(b)
    print bestMove[0]

    # check amount of x's and o's on the board 
    O_count = 0
    X_count = 0

    for i in range(3):
        for j in range(3):
            if b[i][j] == 'o':
                O_count += 1
            elif b[i][j] == 'x':
                X_count += 1

    # update board with best move
    new_board = b

    if O_count > X_count:
        new_board[bestMove[0][0]][bestMove[0][1]] = 'x'
    elif X_count > O_count:
        new_board[bestMove[0][0]][bestMove[0][1]] = 'o'
    else:
        new_board[bestMove[0][0]][bestMove[0][1]] = 'x'
    
    # print new_board

    # convert list to string
    new_str = ""

    for i in range(3):
        for j in range(3):
            new_str += new_board[i][j]

    print new_str

    # print the best move
    # then write all the possible states in the textfile.

    Status = EvaluateBoard(b)
    
    # write to file 
    file = open(sys.argv[2], "w")

    file.write(new_str + " " + str(Status) + '\n')

    file.close()