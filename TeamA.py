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
        self.possible_moves = set (((2,2),(2,3),(2,4),(2,5),(3,2),(3,5),(4,2), (4,5), (5,2), (5,3), (5,4), (5,5)))
	
    def get_possible_moves (self, row, col):
        possible_moves = set()
        for i in self.directions:
            check_row = row + i[0]
            check_col = col + i[1]
            if (0 <= check_row < self.size and 0 <= check_col < self.size and self.board[check_row][check_col]==' '):
                possible_moves.add((check_row, check_col))
		
        return possible_moves
   

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

            #Places piece of opponent's color at (row,col) and then returns
            #  the best move, determined by the make_move(...) function

    def play_square(self, row, col, playerColor, oppColor):
    # Place a piece of the opponent's color at (row,col)
         if (row, col) != (-1, -1):
                self.place_piece(row, col, oppColor, playerColor)
		# obtain new possible moves surronding the last square played and add them, also delete the last square played
		self.possible_moves.remove((row, col))
		self.possible_moves = self.possible_moves.union(self.get_possible_moves(row, col))
                
                # Determine best move and and return value to Matchmaker
                self.r = -1
                self.c = -1
                # print("|||||||||||||||||||||||||||||||||||||||||||||")
                # self.PrintBoard()
                # print("|||||||||||||||||||||||||||||||||||||||||||||")
                self.MaxplyMaster(playerColor,oppColor,-1000,1000,0)
                self.place_piece(self.r, self.c,playerColor,oppColor)
		self.possible_moves.remove((self.r, self.c))
		self.possible_moves = self.possible_moves.union(self.get_possible_moves(self.r, self.c))
                
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

    

    def FindMoves(self, playerColor, oppColor):
        moves = []
        for move in self.possible_moves:
                if (self.islegal(move[0], move[1], playerColor, oppColor)):
                    moves.append((move[0], move[1]))
        if(moves):
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
	

    def MaxplyMaster(self,playerColor,oppColor,alpha,beta,depth):
	    moves = self.FindMoves(playerColor,oppColor)
            v = -1000
	    changed = 0
            for move in moves:
                board = copy.deepcopy(self.board)
		if self.place_piece(move[0],move[1],playerColor,oppColor):
			changed = 1
			self.possible_moves.remove((move[0],move[1]))
			new_moves = self.get_possible_moves(move[0], move[1])
			self.possible_moves = self.possible_moves.union(new_moves)
			
                v = self.minply(playerColor,oppColor,alpha,beta,depth+1)
                if(alpha < v):
                    self.r,self.c = move[0],move[1]
                    alpha = v
                self.board = board
		if changed == 1:
			changed = 0
			# backtrack and add the move removed
			self.possible_moves.add((move[0],move[1]))
			# fetch the moves which are valid and which should not be removed during backtracking
			valid_moves = self.find_valid_moves(new_moves)
			# subtract  the valid moves from the new_moves so they won't be removed from possible_moves set
			new_moves -= valid_moves
			# remove the moves which were added based on the move removed previously
			self.possible_moves -= new_moves
			
                if(beta <= alpha):
                    return alpha
            return v


    def minply(self,playerColor,oppColor,alpha,beta,depth):
	if(depth >= DEPTHLIMIT):
	    return self.evaluationfn(playerColor,oppColor)
        else:
	    moves = self.FindMoves(oppColor,playerColor)
	    v = 1000
	    changed = 0
            for move in moves:
                board = copy.deepcopy(self.board)
		if self.place_piece(move[0],move[1], oppColor, playerColor):
			changed = 1
			self.possible_moves.remove((move[0],move[1]))
			new_moves = self.get_possible_moves(move[0], move[1])
			self.possible_moves = self.possible_moves.union(new_moves)
			
                v = min(v,self.maxply(playerColor,oppColor,alpha,beta,depth+1))
                self.board = board
		# backtrack and add the move removed
	        if changed == 1:
            		changed = 0
			self.possible_moves.add((move[0],move[1]))
			# fetch the moves which are valid and which should not be removed during backtracking
			valid_moves = self.find_valid_moves(new_moves)
			# subtract  the valid moves from the new_moves so they won't be removed from possible_moves set
			new_moves -= valid_moves
			# remove the moves which were added based on the move removed previously
			self.possible_moves -= new_moves
			
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
	    changed = 0
            for move in moves:
                board = copy.deepcopy(self.board)
                if self.place_piece(move[0],move[1],playerColor,oppColor):
			changed = 1
			self.possible_moves.remove((move[0],move[1]))
			new_moves = self.get_possible_moves(move[0], move[1])
			self.possible_moves = self.possible_moves.union(new_moves)
			
                v = max(v,self.minply(playerColor,oppColor,alpha,beta,depth+1))
                self.board = board
		if changed == 1:
            		changed = 0
			self.possible_moves.add((move[0],move[1]))
			# fetch the moves which are valid and which should not be removed during backtracking
			valid_moves = self.find_valid_moves(new_moves)
			# subtract  the valid moves from the new_moves so they won't be removed from possible_moves set
			new_moves -= valid_moves
			# remove the moves which were added based on the move removed previously
			self.possible_moves -= new_moves
			#self.PrintBoard()
			#print ("old possible moves:"+str(self.possible_moves))
                
                
                alpha = max(alpha,v)
                if(alpha >= beta):
                    return alpha
            return v



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



