from __future__ import print_function
import copy
import time
__author__ = 'Madhunisha'



class NewMonk:
    def __init__(self):
        self.board = [[' '] * 8 for i in range(8)]
        self.size = 8
        self.board[4][4] = 'W'
        self.board[3][4] = 'B'
        self.board[3][3] = 'W'
        self.board[4][3] = 'B'
        self.r = -1
        self.c = -1
        self.valMatrix = [[' '] * 8 for i in range(8)]
        self.valMatrix[0][0] = 20
        self.valMatrix[0][1] = self.valMatrix[1][0] = -3
        self.valMatrix[1][1] = -7
        self.valMatrix[2][0] = self.valMatrix[0][2] = 11
        self.valMatrix[0][3] = self.valMatrix[3][0] = 8
        self.valMatrix[2][1] = self.valMatrix[1][2] = -4
        self.valMatrix[2][2] = self.valMatrix[2][3] = self.valMatrix[3][2] = 2
        self.valMatrix[3][3] = -3
        self.valMatrix[3][1] = self.valMatrix[1][3] = 1
        self.corners = [(0,0),(0,7),(7,0),(7,7)]
        self.cornerdiag = [(1,1),(1,6),(6,1),(6,6),(1,0),(0,1),(0,6),(1,7),(6,0),(7,1),(7,6),(6,7)]
        for x in range(0,4):
            for i, j in zip(range(0,4), range(7, 3,-1)):
                self.valMatrix[x][j] = self.valMatrix[x][i]
        for x in range(0,8):
            for i, j in zip(range(0,4), range(7, 3,-1)):
                self.valMatrix[j][x] = self.valMatrix[i][x]
        # a list of unit vectors (row, col)
        print (self.board)
        self.directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        #  a list of legal moves for both the players
        #  for white sqaures possible moves
        self.possible_moves = set (((2,2), (2,3), (2,4), (2,5), (3,2), (3,5), (4,2), (4,5), (5,2), (5,3), (5,4), (5,5)))
        self.start_time = 0
        self.wait_time = 13
        self.depthlimit = 0
        self.timeout = 0

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



    def get_possible_moves (self, row, col):
        possible_moves = set()
        for i in self.directions:
            check_row = row + i[0]
            check_col = col + i[1]
            if (0 <= check_row < self.size and 0 <= check_col < self.size and self.board[check_row][check_col]==' '):
                possible_moves.add((check_row, check_col))

        return possible_moves



    def update_possible_moves(self, row, col):
        self.possible_moves.remove((row, col))
        new_moves = self.get_possible_moves(row, col)
        self.possible_moves = self.possible_moves.union(new_moves)
        return new_moves



    def backtrack_and_update_possible_moves(self, row, col, new_moves):
        # backtrack and add the move removed
        self.possible_moves.add((row,col))
        # fetch the moves which are valid and which should not be removed during backtracking
        valid_moves = self.find_valid_moves(new_moves)
        # subtract  the valid moves from the new_moves so they won't be removed from possible_moves set
        new_moves -= valid_moves
        # remove the moves which were added based on the move removed previously
        self.possible_moves -= new_moves



    # checks if the move you are going to remove in backtracking is a valid move due to some neighbouring square or not, if yes it shouldn't be removed. Means if that move is surrounded by some disc then its a neighbouring sqaure of that disc so its a valid move
    def find_valid_moves(self, moves):
        valid_moves = set()
        for move in moves:
            for direction in self.directions:
                check_row = move[0] + direction[0]
                check_col = move[1] + direction[1]
                if (0 <= check_row < self.size and 0 <= check_col < self.size and self.board[check_row][check_col]!=' '):
                    valid_moves.add(move)
                    break
        return valid_moves



    def FindMoves(self, playerColor, oppColor):
        moves = []
        for move in self.possible_moves:
                if (self.islegal(move[0], move[1], playerColor, oppColor)):
                    moves.append((move[0], move[1]))
        if(moves):
            return moves
        return [(-1, -1)]


    # returns moves ordered in descending order of their values
    def order_moves(self, playerColor,oppColor,alpha,beta,depth):
        moves = self.FindMoves(playerColor,oppColor)
        # save the current depthlimit
        depth_limit = self.depthlimit
        # temporarily set it to 2
        self.depthlimit = 2
        ordered_moves = []
        respective_ordered_vals = []
        for move in moves:
            board = copy.deepcopy(self.board)
            board_changed = 0
            if self.place_piece(move[0],move[1],playerColor,oppColor):
                board_changed = 1
                new_moves = self.update_possible_moves(move[0],move[1])
            v = self.minply(playerColor,oppColor,alpha,beta,depth+1)
            self.board = board
            if board_changed == 1:
                board_changed = 0
                self.backtrack_and_update_possible_moves(move[0],move[1], new_moves)
            index = 0
            for val in respective_ordered_vals:
                if val < v:
                    break
                index += 1
            respective_ordered_vals.insert(index, v)
            ordered_moves.insert(index, move)
        # Reset depthlimit for full fledged search
        self.depthlimit = depth_limit
        #print ("Moves:"+ str(ordered_moves))
        #print ("Values:"+ str(respective_ordered_vals))
        return ordered_moves



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
            print("player and opponent cannot be the same.........................................................................")
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



    #  Places piece of opponent's color at (row,col) and then returns
    #  the best move, determined by the make_move(...) function

    def play_square(self, row, col, playerColor, oppColor):
        # Place a piece of the opponent's color at (row,col)
        self.start_time = time.time()
        if (row, col) != (-1, -1):
            if self.place_piece(row, col, oppColor, playerColor):
                # obtain new possible moves surronding the last square played and add them, also delete the last square played
                self.update_possible_moves(row, col)
        # Determine best move and return value to Matchmaker
        self.r = -1
        self.c = -1
        last_r = -1
        last_c = -1
        self.depthlimit = 1
        self.timeout = 0
	moves = self.order_moves(playerColor,oppColor,-1000,1000,0)
        while self.depthlimit < 65:
            val = self.MaxplyMaster(playerColor,oppColor,-1000,1000,0, moves)
            if self.timeout == 1:
                break;
            # save the last stable move obtained after completely exploring till the previous depthlimit
            last_r = self.r
            last_c = self.c
	    self.depthlimit += 1

        self.r = last_r
        self.c = last_c
        if self.place_piece(self.r, self.c,playerColor,oppColor):
            self.update_possible_moves(self.r, self.c)
	return (self.r,self.c)



    # sets all tiles along a given direction (Dir) from a given starting point (col and row) for a given distance
    # (dist) to be a given value ( player )
    def flip_tiles(self, row, col, Dir, dist, player):
        for i in range(dist):
            self.board[row + i * Dir[0]][col + i * Dir[1]] = player
        return True

            #returns the value of a square on the board

    def get_square(self, row, col):
            return self.board[row][col]

            #Search the game board for a legal move, and play the first one it finds

    def evaluationfn(self,PlayerColor,oppColor):
        score = 0
        playerCorner = 0
        oppCorner = 0
        playerClose = 0
        oppClose = 0
        playdisc= 0
        oppdisc = 0
        #count the number of the discs that belong to the player and the number of discs that belong to the opponent
        for i in range(8):
            for j in range(8):
                if(self.board[i][j] == PlayerColor):
                    playdisc = playdisc+1
                elif(self.board[i][j] == oppColor):
                    oppdisc = oppdisc + 1

        for player in self.corners:
            if self.board[player[0]][player[1]] != ' ':
                if self.board[player[0]][player[1]] == PlayerColor:
                    playerCorner = playerCorner+1
                else:
                    oppCorner = oppCorner+1
            else:
                for play1 in self.cornerdiag:
                    if self.board[play1[0]][play1[1]]== PlayerColor:
                        playerClose = playerClose + 1
                    else:
                        oppClose = oppClose+1
        playerPossibleMoves = self.FindMoves(PlayerColor,oppColor)
        opponentPossibleMoves = self.FindMoves(oppColor,PlayerColor)
        playmob = 100 * (len(playerPossibleMoves)/(len(playerPossibleMoves) + len(opponentPossibleMoves))) + (10 * (playdisc/(playdisc+oppdisc)) )
        oppmob = -100 * (len(opponentPossibleMoves)/(len(playerPossibleMoves) + len(opponentPossibleMoves))) - (10 * (oppdisc/(playdisc+oppdisc)) )
        #for x in playerPossibleMoves:
        #      score = score + self.valMatrix[x[0]][x[1]]
        #for x in opponentPossibleMoves:
        #      score = score - self.valMatrix[x[0]][x[1]]
        corScore = 25 * playerCorner - 25 * oppCorner

        closeScore = -12.5 * playerClose + 12.5 * oppClose
        score = corScore+closeScore+playmob+oppmob
	#print ("score:"+str(score))
        return score



    def MaxplyMaster(self,playerColor,oppColor,alpha,beta,depth, moves):
        v = -1000
        board_changed = 0
	#print (moves)
        for move in moves:
            board = copy.deepcopy(self.board)
            if self.place_piece(move[0],move[1],playerColor,oppColor):
                board_changed = 1
                new_moves = self.update_possible_moves(move[0], move[1])
            v = self.minply(playerColor,oppColor,alpha,beta,depth+1)
            self.board = board
            if board_changed == 1:
                board_changed = 0
                self.backtrack_and_update_possible_moves(move[0],move[1],new_moves)
            if (self.timeout == 1):
                break
            if (alpha < v):
                self.r,self.c = move[0],move[1]
                alpha = v
        return v


    def minply(self,playerColor,oppColor,alpha,beta,depth):
        if ((time.time() - self.start_time) > self.wait_time):
            self.timeout = 1
            return -1
        if(depth >= self.depthlimit):
            return self.evaluationfn(playerColor,oppColor)
        else:
            moves = self.FindMoves(oppColor,playerColor)
            v = 1000
            board_changed = 0
            for move in moves:
                board = copy.deepcopy(self.board)
                if self.place_piece(move[0],move[1], oppColor, playerColor):
                    board_changed = 1
                    new_moves = self.update_possible_moves(move[0], move[1])
                v = min(v,self.maxply(playerColor,oppColor,alpha,beta,depth+1))
                self.board = board
                # backtrack and add the move removed
                if board_changed == 1:
                    board_changed = 0
                    self.backtrack_and_update_possible_moves(move[0],move[1],new_moves)
                if self.timeout == 1:
                    break
                beta = min(beta,v)
                if(beta <= alpha):
                    return beta

            return v

    def maxply(self,playerColor,oppColor,alpha,beta,depth):
        if ((time.time() - self.start_time) > self.wait_time):
            self.timeout = 1
            return -1
        if(depth >= self.depthlimit):
            return self.evaluationfn(playerColor,oppColor)
        else:
            moves = self.FindMoves(playerColor,oppColor)
            v = -1000
            board_changed = 0
            for move in moves:
                board = copy.deepcopy(self.board)
                if self.place_piece(move[0],move[1],playerColor,oppColor):
                    board_changed = 1
                    new_moves = self.update_possible_moves(move[0], move[1])

                v = max(v,self.minply(playerColor,oppColor,alpha,beta,depth+1))
                self.board = board
                if board_changed == 1:
                    board_changed = 0
                    self.backtrack_and_update_possible_moves(move[0],move[1],new_moves)
                if self.timeout == 1:
                    break
                alpha = max(alpha,v)
                if(alpha >= beta):
                   return alpha
            return v


