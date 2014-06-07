from __future__ import print_function
import copy
__author__ = 'Madhunisha'



DEPTHLIMIT = 6

class TeamA:
    def __init__(self):
        self.board = [[' '] * 8 for i in range(8)]
        self.size = 8
        self.board[4][4] = 'W'
        self.board[3][4] = 'B'
        self.board[3][3] = 'W'
        self.board[4][3] = 'B'
        self.r = -1
        self.c = -1
        # a list of unit vectors (row, col)
        print (self.board)
        self.directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        # a list of legal moves for both the players
        #  for white sqaures possible moves
        set_for_white = self.get_possible_moves(3, 4, self.directions, 'W', 'B')
        set_for_white = set_for_white.union(self.get_possible_moves(4, 3, self.directions, 'W', 'B'))
        set_for_black = self.get_possible_moves(4, 4, self.directions, 'B', 'W')
        set_for_black = set_for_black.union(self.get_possible_moves(3, 3, self.directions, 'B', 'W'))
        self.players_possible_moves = [set_for_black, set_for_white] # black player's list first followed by white one's
        print ("possible white moves:"+str(self.players_possible_moves[1]))

    def get_possible_moves (self, row, col, directions, player, opp):
        print ("directions:"+str(directions)+"row:"+str(row)+"col:"+str(col))
        possible_moves = set()
        for i in directions:
            check_row = row + i[0]
            check_col = col + i[1]
            #print "row:"+str(check_row)+"col:"+str(check_col)
            if (self.board[check_row][check_col]==' '):
                if self.islegal(check_row, check_col, player, opp):
                    possible_moves.add((check_row, check_col))
		#print "possible moves:"+str(possible_moves)
		print (possible_moves)
        return possible_moves
        #prints the boards

    def PrintBoard(self):
        # Print column numbers
        print("  ",end="")
        for i in range(self.size):
            print(i+1,end=" ")
        print()
        # Build horizontal separator
        linestr = " " + ("+-" * self.size) + "+"

        # Print board
        for i in range(self.size):
            print(linestr)  # Separator
            print(i+1,end="|")				   # Row number
            for j in range(self.size):
                print(self.board[i][j],end="|")  # board[i][j] and pipe separator
            print()  # End line
        print(linestr)

        #checks every direction fromt the position which is input via "col" and "row", to see if there is an opponent piece
        #in one of the directions. If the input position is adjacent to an opponents piece, this function looks to see if there is a
        #a chain of opponent pieces in that direction, which ends with one of the players pieces.

    def islegal(self, row, col, player, opp):
        if (self.get_square(row, col) != " "):
            return False
        for Dir in self.directions:
            for i in range(self.size):
                if ((( row + i * Dir[0]) < self.size) and (( row + i * Dir[0]) >= 0 ) and (
                            ( col + i * Dir[1]) >= 0 ) and (( col + i * Dir[1]) < self.size )):
                    #does the adjacent square in direction dir belong to the opponent?
                    if self.get_square(row + i * Dir[0], col + i * Dir[1]) != opp and i == 1:  # no
                        #no pieces will be flipped in this direction, so skip it
                        break
                    #yes the adjacent piece belonged to the opponent, now lets see if there are a chain
                    #of opponent pieces
                    if self.get_square(row + i * Dir[0], col + i * Dir[1]) == " " and i != 0:
                        break

                    #with one of player's pieces at the other end
                    if self.get_square(row + i * Dir[0], col + i * Dir[1]) == player and i != 0 and i != 1:
                        #set a flag so we know that the move was legal
                        return True
        return False

            #returns true if the square was played, false if the move is not allowed

    def place_piece(self, row, col, player, opp):
        if(row == -1 and col == -1):
            return False
        if (self.get_square(row, col) != " "):
            return False

        if (player == opp):
            print("player and opponent cannot be the same")
            return False

        legal = False
        #for each direction, check to see if the move is legal by seeing if the adjacent square
        #in that direction is occuipied by the opponent. If it isnt check the next direction.
        #if it is, check to see if one of the players pieces is on the board beyond the oppponents piece,
        #if the chain of opponents pieces is flanked on both ends by the players pieces, flip
        #the opponents pieces
        for Dir in self.directions:
            #look across the length of the board to see if the neighboring squares are empty,
            #held by the player, or held by the opponent
            for i in range(self.size):
                if ((( row + i * Dir[0]) < self.size) and (( row + i * Dir[0]) >= 0 ) and (
                                ( col + i * Dir[1]) >= 0 ) and (( col + i * Dir[1]) < self.size )):
                        #does the adjacent square in direction dir belong to the opponent?
                        if self.get_square(row + i * Dir[0], col + i * Dir[1]) != opp and i == 1:  # no
                            #no pieces will be flipped in this direction, so skip it
                            break
                        #yes the adjacent piece belonged to the opponent, now lets see if there are a chain
                        #of opponent pieces
                        if self.get_square(row + i * Dir[0], col + i * Dir[1]) == " " and i != 0:
                            break

                        #with one of player's pieces at the other end
                        if self.get_square(row + i * Dir[0], col + i * Dir[1]) == player and i != 0 and i != 1:
                            #set a flag so we know that the move was legal
                            legal = True
                            self.flip_tiles(row, col, Dir, i, player)
                            break

        return legal

            #Places piece of opponent's color at (row,col) and then returns
            #  the best move, determined by the make_move(...) function

    def play_square(self, row, col, playerColor, oppColor):
    # Place a piece of the opponent's color at (row,col)
         if (row, col) != (-1, -1):
                self.place_piece(row, col, oppColor, playerColor)
                # Determine best move and and return value to Matchmaker
                self.r = -1
                self.c = -1
                # print("|||||||||||||||||||||||||||||||||||||||||||||")
                # self.PrintBoard()
                # print("|||||||||||||||||||||||||||||||||||||||||||||")
                self.MaxplyMaster(playerColor,oppColor,-1000,1000,0)
                self.place_piece(self.r, self.c,playerColor,oppColor)
                return (self.r,self.c)

            #sets all tiles along a given direction (Dir) from a given starting point (col and row) for a given distance
            # (dist) to be a given value ( player )

    def flip_tiles(self, row, col, Dir, dist, player):
        for i in range(dist):
            self.board[row + i * Dir[0]][col + i * Dir[1]] = player
        return True

            #returns the value of a square on the board

    def get_square(self, row, col):
            return self.board[row][col]

            #Search the game board for a legal move, and play the first one it finds

    def make_move(self, playerColor, oppColor):
            for row in range(self.size):
                for col in range(self.size):
                    if (self.islegal(row, col, playerColor, oppColor)):
                        for Dir in self.directions:
                            #look across the length of the board to see if the neighboring squares are empty,
                            #held by the player, or held by the opponent
                            for i in range(self.size):
                                if ((( row + i * Dir[0]) < self.size) and (( row + i * Dir[0]) >= 0 ) and (
                                            ( col + i * Dir[1]) >= 0 ) and (( col + i * Dir[1]) < self.size )):
                                    #does the adjacent square in direction dir belong to the opponent?
                                    if self.get_square(row + i * Dir[0], col + i * Dir[1]) != oppColor and i == 1:  # no
                                        #no pieces will be flipped in this direction, so skip it
                                        break
                                    #yes the adjacent piece belonged to the opponent, now lets see if there are a chain
                                    #of opponent pieces
                                    if self.get_square(row + i * Dir[0], col + i * Dir[1]) == " " and i != 0:
                                        break

                                    #with one of player's pieces at the other end
                                    if self.get_square(row + i * Dir[0],
                                                       col + i * Dir[1]) == playerColor and i != 0 and i != 1:
                                        #set a flag so we know that the move was legal
                                        legal = True
                                        self.flip_tiles(row, col, Dir, i, playerColor)
                                        break
                        return (row, col)
            return (-1, -1)

    def cornerCheck(self,row,col,directions,player,opp):
        score = 0
        #possibleMoves = self.get_possible_moves(row,col,directions,player,opp)
        playerPossibleMoves = self.FindMoves(player,opp)
        opponentPossibleMoves = self.FindMoves(opp,player)
        score = score + len(playerPossibleMoves)-len(opponentPossibleMoves)
        print ("from corner:")
        if (2,4) in playerPossibleMoves and (2,4)not in opponentPossibleMoves:
            score = score +10
        if (0,7) in playerPossibleMoves and (0,7)not in opponentPossibleMoves:
            score = score +10
        if (7,0) in playerPossibleMoves and (7,0)not in opponentPossibleMoves:
            score = score +10
        if (7,7) in playerPossibleMoves and (7,7)not in opponentPossibleMoves:
            score = score +10

        return score

    def evaluation(self,row,col,directions,player,opp):
        cornerScore = self.cornerCheck(row,col,directions,player,opp)



    def FindMoves(self, playerColor, oppColor):
        moves = []
        for row in range(self.size):
            for col in range(self.size):
                if (self.islegal(row, col, playerColor, oppColor)):
                    for Dir in self.directions:
                        #look across the length of the board to see if the neighboring squares are empty,
                        #held by the player, or held by the opponent
                        for i in range(self.size):
                            if ((( row + i * Dir[0]) < self.size) and (( row + i * Dir[0]) >= 0 ) and (
                                        ( col + i * Dir[1]) >= 0 ) and (( col + i * Dir[1]) < self.size )):
                                #does the adjacent square in direction dir belong to the opponent?
                                if self.get_square(row + i * Dir[0], col + i * Dir[1]) != oppColor and i == 1:  # no
                                    #no pieces will be flipped in this direction, so skip it
                                    break
                                #yes the adjacent piece belonged to the opponent, now lets see if there are a chain
                                #of opponent pieces
                                if self.get_square(row + i * Dir[0], col + i * Dir[1]) == " " and i != 0:
                                    break

                                #with one of player's pieces at the other end
                                if self.get_square(row + i * Dir[0],
                                                   col + i * Dir[1]) == playerColor and i != 0 and i != 1:
                                    #set a flag so we know that the move was legal
                                    legal = True
                                    #self.flip_tiles(row, col, Dir, i, playerColor)
                                    break
                    moves.append((row, col))
        if(moves):
            # print("p")
            # print(moves)
            return moves
        return [(-1, -1)]

    def evaluationfn(self,PlayerColor,oppColor):
        score = 0
        for i in range(8):
            for j in range(8):
                if(self.board[i][j] == PlayerColor):
                    score = score+0.01
                elif(self.board[i][j] == oppColor):
                    score = score - 0.01
        playerPossibleMoves = self.FindMoves(PlayerColor,oppColor)
        opponentPossibleMoves = self.FindMoves(oppColor,PlayerColor)
        score = score + len(playerPossibleMoves)-len(opponentPossibleMoves)
        if (0,0) in playerPossibleMoves and (0,0)not in opponentPossibleMoves:
            score = score +10
        if (0,7) in playerPossibleMoves and (0,7)not in opponentPossibleMoves:
            score = score +10
        if (7,0) in playerPossibleMoves and (7,0)not in opponentPossibleMoves:
            score = score +10
        if (7,7) in playerPossibleMoves and (7,7)not in opponentPossibleMoves:
            score = score +10

        return score








    def MaxplyMaster(self,playerColor,oppColor,alpha,beta,depth):
            moves = self.FindMoves(playerColor,oppColor)
            v = -1000
            for move in moves:
                board = copy.deepcopy(self.board)
                # board = self.board
                self.place_piece(move[0],move[1],playerColor,oppColor)
                v = self.minply(playerColor,oppColor,alpha,beta,depth+1)
                if(alpha < v):
                    self.r,self.c = move[0],move[1]
                    alpha = v
                # self.board = copy.deepcopy(board)
                self.board = board
                if(beta <= alpha):
                    return alpha
            return v


    def minply(self,playerColor,oppColor,alpha,beta,depth):
        if(depth >= DEPTHLIMIT):
            return self.evaluationfn(playerColor,oppColor)
        else:
            moves = self.FindMoves(oppColor,playerColor)
            v = 1000
            for move in moves:
                # board = self.board
                board = copy.deepcopy(self.board)
                self.place_piece(move[0],move[1],oppColor,playerColor)
                v = min(v,self.maxply(playerColor,oppColor,alpha,beta,depth+1))
                # self.board = copy.deepcopy(board)
                self.board = board
                beta = min(beta,v)
                if(beta <= alpha):
                    return beta

            return v

    def maxply(self,playerColor,oppColor,alpha,beta,depth):
        if(depth >= DEPTHLIMIT):
            return self.evaluationfn(playerColor,oppColor)
        else:
            moves = self.FindMoves(playerColor,oppColor)
            v = -1000
            for move in moves:
                board = copy.deepcopy(self.board)
                # board = self.board
                self.place_piece(move[0],move[1],playerColor,oppColor)
                v = max(v,self.minply(playerColor,oppColor,alpha,beta,depth+1))
                # self.board = copy.deepcopy(board)
                self.board = board
                alpha = max(alpha,v)
                if(alpha >= beta):
                    return alpha
            return v


#def main():
    #board = TeamA()
    #board.PrintBoard()
    #score = board.cornerCheck(3,4,board.directions,'W','B')
    #print(score);
def main():
    c = TeamA()
    flag = 'Y'
    opp='B'
    player ='W'
    while(flag == 'Y'):
        c.PrintBoard()

        r = input("Row-----")
        col = input("Col-----")
        c.play_square(r,col,player,opp)
        c.PrintBoard()
        flag = input("Do you want to continue")



