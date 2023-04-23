## strinhg all information about the current state of a chess game, rsponsible for determining th valid moves at the current state and keep move log

class GameState():
    def __init__(self):
        #2d array 8x8 list and each list has two characters
        self.moveLog = []
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "bB", "--", "--", "--", "--", "--"],
            ["--", "wR", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]]
        self.whiteToMove = True
        self.whiteKingLocation = (7, 4)
        self.blackKingLocation = (0, 4)
        self.checkMate = False
        self.staleMate = False

    def makeMove(self, move):
        if self.board[move.startRow][move.startCol] != "--":
            self.board[move.startRow][move.startCol] = "--"
            self.board[move.endRow][move.endCol] = move.pieceMoved
            self.moveLog.append(move)
            self.whiteToMove = not self.whiteToMove # switch the player from white to black
            if move.pieceMoved == "wK":
                self.whiteKingLocation = (move.endRow, move.endCol)
            elif move.pieceMoved == "bK":
                self.blackKingLocation = (move.endRow, move.endCol)


    def undoMove(self):
        if len(self.moveLog) != 0:
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol]= move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove
            if move.pieceMoved == "wK":
                self.whiteKingLocation = (move.startRow, move.startCol)
            elif move.pieceMoved == "bK":
                self.blackKingLocation = (move.startRow, move.startCol)



    def validMoves(self):
        moves = self.possibleMoves()
        for i in range(len(moves)-1, -1, -1):
            self.makeMove(moves[i]) # turn switched within the subroutine makeMove
            self.whiteToMove = not self.whiteToMove
            if self.inCheck():
                moves.remove(moves[i])
            self.whiteToMove = not self.whiteToMove
            self.undoMove()
        return moves
        if len(moves) == 0:
            if self.inCheck():
                self.checkMate = True
            else:
                self.staleMate = True
        else:
            self.checkMate = False
            self.staleMate = False



    def squareUnderAttack(self, r, c):
        self.whiteToMove = not self.whiteToMove
        moves = self.possibleMoves()
        self.whiteToMove = not self.whiteToMove
        for move in moves:
            if move.endRow == r and move.endCol == c:
                return True
        return False

    def inCheck(self):
        if self.whiteToMove:
            return self.squareUnderAttack(self.whiteKingLocation[0], self.whiteKingLocation[1])
        else:
            return self.squareUnderAttack(self.blackKingLocation[0], self.blackKingLocation[1])


    def possibleMoves(self):
        moves = []
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                turn = self.board[r][c][0]
                if (turn == "w" and self.whiteToMove) or (turn == "b" and not self.whiteToMove):
                    piece_type = self.board[r][c][1]
                    if piece_type == "p":
                        self.pawnMoves(r, c, moves)
                    elif piece_type == "R":
                        self.rookMoves(r, c, moves)
                    elif piece_type == "N":
                        self.knightMoves(r, c, moves)
                    elif piece_type == "B":
                        self.bishopMoves(r, c, moves)
                    elif piece_type == "K":
                        self.kingMoves(r, c, moves)
                    elif piece_type == "Q":
                        self.queenMoves(r, c, moves)

        return moves

    def pawnMoves(self, r, c, moves):
        if self.whiteToMove:
            if self.board[r - 1][c] == "--":
                moves.append(Move((r, c), (r - 1, c), self.board))
                if r == 6 and self.board[r - 2][c] == "--":
                    moves.append(Move((r, c), (r - 2, c), self.board))
            if c - 1 >= 0:
                if self.board[r - 1][c - 1][0] == "b":
                    moves.append(Move((r, c), (r - 1, c - 1), self.board))
            if c + 1 <= 7:
                if self.board[r - 1][c + 1][0] == "b":
                    moves.append(Move((r, c), (r - 1, c + 1), self.board))



        else:
            if self.board[r + 1][c] == "--":
                moves.append(Move((r, c), (r + 1, c), self.board))
                if r == 1 and self.board[r + 2][c] == "--":
                    moves.append(Move((r, c), (r + 2, c), self.board))
            if c - 1 >= 0: # check left to the board
                if self.board[r + 1][c - 1][0] == "w":
                    moves.append(Move((r, c), (r + 1, c - 1), self.board))
            if c + 1 <= 7: # check right to the board
                if self.board[r + 1][c + 1][0] == "w":
                    moves.append(Move((r, c), (r + 1, c + 1), self.board))



    def knightMoves(self, r, c, moves):
        directions = [(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2)]
        allyColor = "w" if self.whiteToMove else "b"
        for d in directions:
            endRow = r + d[0]
            endCol = c + d[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColor:
                    moves.append(Move((r, c), (endRow, endCol), self.board))



    def bishopMoves(self, r, c, moves):
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)] # topleft, topright, bottomleft, bottomright
        enemyColor = "b" if self.whiteToMove else "w"
        for d in directions:
            for i in range(1, 8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--":
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                    elif endPiece[0] == enemyColor:
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                        break
                    else:
                        break
                else:
                    break


    def rookMoves(self, r, c, moves):
        directions = [(-1, 0), (0, -1), (1, 0), (0, 1)] # up left down right
        enemyColor = "b" if self.whiteToMove else "w"
        for d in directions:
            for i in range(1, 8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--":
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                    elif endPiece[0] == enemyColor:
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                        break
                    else:
                        break
                else:
                    break


    def queenMoves(self, r, c, moves):
        self.rookMoves(r, c, moves)
        self.bishopMoves(r, c, moves)

    def kingMoves(self, r, c, moves):
        directions= [(1, -1), (1, 0), (0, 1), (1, 1), (-1, 0), (0, -1), (-1, -1), (-1, 1)]
        enemyColor = "b" if self.whiteToMove else "w"
        for d in directions:
            endRow = r + d[0]
            endCol = c + d[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece == "--":
                    moves.append(Move((r, c), (endRow, endCol), self.board))
                elif endPiece[0] == enemyColor:
                    moves.append(Move((r, c), (endRow, endCol), self.board))

        pass

    def literalRookMoves(self, r, c, moves):
         # move right
         if c < 7:
            hoz_pos = list(range(c + 1, 8, 1))
            for col in hoz_pos:
                 if self.board[r][col] == "--":
                    moves.append(Move((r, c), (r, col), self.board))
                 elif self.board[r][col][0] == "b":
                    moves.append(Move((r, c), (r, col), self.board))
         # move left
         if c > 0:
            hoz_neg = list(range(c - 1, -1, -1))
            for neg_col in hoz_neg:
                if self.board[r][neg_col] == "--":
                    moves.append(Move((r, c), (r, neg_col), self.board))
                elif self.board[r][neg_col][0] == "b":
                    moves.append(Move((r, c), (r, neg_col), self.board))
        # move up
         if r > 0:
            ver_pos = list(range(r + 1, 8, 1))
            for row in ver_pos:
                if self.board[row][c] == "--":
                    moves.append(Move((r, c), (row, c), self.board))
                elif self.board[row][c][0] == "b":
                    moves.append(Move((r, c), (row, c), self.board))
            # move down
         if r < 7:
            ver_neg = list(range(r - 1, -1, -1))
            for neg_ver in ver_neg:
                if self.board[neg_ver][c] == "--":
                    moves.append(Move((r, c), (neg_ver, c), self.board))
                elif self.board[neg_ver][c][0] == "b":
                    moves.append(Move((r, c), (neg_ver, c), self.board))





class Move():
    '''dictionary for switching computer notation to the user notation of the row count: the user bottom or the lowest is essentially the lower num or 0 whereas in the computer
    notation, it comprehend 8 or the largest index. The user notation is referred to as ranks
    '''
    # from user notation to computer notation
    ranksToRows = {"1" : 7, "2" : 6, "3" : 5, "4" : 4, "5" : 3, "6" : 2, "7" : 1, "8" : 0}
    rowsToRanks = {v : k for k, v in ranksToRows.items()}
    # rowToRanks = {"7" : 1, "6" : 2, "5" : 3, "4" : 4, "3" : 5, "2" : 6, "1" : 7, "0" : 8}

    # files are the letter notation indicating the column
    filesToCols = {"a" : 0, "b" : 1, "c" : 2, "d" : 3, "e" : 4, "f" : 5, "g" : 6, "h": 7}
    colsToFiles = {v : k for k, v in filesToCols.items()}

    def __init__(self, startSq, endSq, board): # keeping track of which the piece before being captured or disappeared so keeping information of the beginningand the final of the board
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol
        print(self.moveID)


    def __eq__(self, other):
       if isinstance(other, Move):
           return self.moveID == other.moveID
       return False



    def getChessNotation(self): # switch the computer notation to computer notation for both the initial and the final square
        return self.getRankFiles(self.startRow, self.startCol) + self.getRankFiles(self.endRow, self.endCol)

    def getRankFiles(self, r, c): # switch the computer notation to computer notation for each individual square
        return self.colsToFiles[c] + self.rowsToRanks[r]
