import copy
from square import *
from piece import *
from move import *

import consts

class Board:

    def __init__(self):
        self.layout = [ [0,0,0,0,0,0,0,0] for r in range(consts.ROWS) ]
        self.lastMove = None
        self.createLayout()
        self.addPieces('white')
        self.addPieces('black')

    def createLayout(self):
        for r in range(consts.ROWS):
            for c in range(consts.COLS):
                self.layout[r][c] = Square(r,c)

    def addPieces(self,color):
        row_pawn, row_other = (6,7) if color == 'white' else (1,0)

        for col in range(consts.COLS):
            self.layout[row_pawn][col] = Square(row_pawn,col,Pawn(color))

        self.layout[row_other][0] = Square(row_other,0,Rook(color))
        self.layout[row_other][7] = Square(row_other,7,Rook(color))

        self.layout[row_other][1] = Square(row_other,1,Knight(color))
        self.layout[row_other][6] = Square(row_other,6,Knight(color))

        self.layout[row_other][2] = Square(row_other,2,Bishop(color))
        self.layout[row_other][5] = Square(row_other,5,Bishop(color))

        self.layout[row_other][3] = Square(row_other,3,Queen(color))
        self.layout[row_other][4] = Square(row_other,4,King(color))

        self.layout[3][2] = Square(3,2,Rook(color))
        self.layout[4][3] = Square(4,3,Knight(color))
        self.layout[3][5] = Square(3,5,King(color))

    def calc_moves(self,piece:Piece,row,col,checking):

        def pawn_moves():
            step = 2 if not piece.moved else 1
            
            start = row + piece.dir
            end = row + ( (step+1) * piece.dir)

            startSQ = Square(row,col)

            for ind in range(start,end,piece.dir):
                if not Square.inRange(ind):
                    continue

                if self.layout[ind][col].isOccupied():
                    break
                
                reward = self.layout[ind][col].piece
                nextMove = Move(startSQ,Square(ind,col,reward))
                if checking:
                    if not self.checked(piece,nextMove):
                        piece.addMove(nextMove)
                else:
                    piece.addMove(nextMove)
                

            diagons = [col-1,col+1]
            for diagon in diagons:
                if not Square.inRange(start,diagon):
                    continue
                if self.layout[start][diagon].isEnemy(piece.color):
                    reward = self.layout[start][diagon].piece
                    nextMove = Move(startSQ,Square(start,diagon,reward))
                    if checking:
                        if not self.checked(piece,nextMove):
                            piece.addMove(nextMove)
                    else:
                        piece.addMove(nextMove)

        def knight_moves():
            
            possible_moves = [
                (row-2,col-1),(row-2,col+1),
                (row-1,col-2),(row-1,col+2),
                (row+1,col-2),(row+1,col+2),
                (row+2,col-1),(row+2,col+1)
            ]

            for move in possible_moves:
                nextRow, nextCol = move

                if not Square.inRange(nextRow,nextCol):
                    continue

                if self.layout[nextRow][nextCol].isAlly(piece.color):
                    continue
                

                startSQ = Square(row,col)
                reward = self.layout[nextRow][nextCol].piece
                endSQ = Square(nextRow,nextCol,reward)

                nextMove = Move(startSQ,endSQ)
                if checking:
                    if not self.checked(piece,nextMove):
                        piece.addMove(nextMove)
                else:
                    piece.addMove(nextMove)
                

        def straightline_moves(incrs):

            for incr in incrs:
                rplus, cplus = incr

                nextRow = row + rplus
                nextCol = col + cplus

                while True:
                    if (not Square.inRange(nextRow,nextCol)) or (self.layout[nextRow][nextCol].isAlly(piece.color)):
                        break
                    reward = self.layout[nextRow][nextCol].piece

                    nextMove = Move(Square(row,col),Square(nextRow,nextCol,reward))
                    
                    if checking:
                        if not self.checked(piece,nextMove):
                            piece.addMove(nextMove)
                    else:
                        piece.addMove(nextMove)   

                    if self.layout[nextRow][nextCol].isEnemy(piece.color):
                        break

                    nextRow += rplus
                    nextCol += cplus
                
        def king_moves():
            possible_moves = [
                (row-1,col-1),(row-1,col+1),
                (row+1,col-1),(row+1,col+1),
                (row,col-1),(row,col+1),
                (row-1,col),(row+1,col)
            ]

            for move in possible_moves:
                nextRow, nextCol = move

                if not Square.inRange(nextRow,nextCol):
                    continue

                if self.layout[nextRow][nextCol].isAlly(piece.color):
                    continue
                

                startSQ = Square(row,col)
                endSQ = Square(nextRow,nextCol)

                nextMove = Move(startSQ,endSQ)
                piece.addMove(nextMove)

        if isinstance(piece,Pawn):
            pawn_moves()
        elif isinstance(piece,Knight):
            knight_moves()
        elif isinstance(piece,Rook):
            straightline_moves([
                (-1,0),(1,0),(0,-1),(0,1) # up down left right
            ])
        elif isinstance(piece,Bishop):
            straightline_moves([
                (-1,-1),(-1,1),(1,-1),(1,1) # UL UR BL BR
            ])
        elif isinstance(piece,Queen):
            straightline_moves([
                (-1,0),(1,0),(0,-1),(0,1),
                (-1,-1),(-1,1),(1,-1),(1,1)
            ])
        elif isinstance(piece,King):
            king_moves()
        else:
            return
    
    def valid_move(self,piece,move):
        return move in piece.moves

    def move(self,piece,move):
        start = move.start
        end = move.end

        self.layout[start.row][start.col].piece = None
        
        if isinstance(piece, Pawn) and self.canPromote(end):
            piece = Queen(piece.color)

        self.layout[end.row][end.col].piece = piece
        piece.moved = True
        piece.clearMoves()

        self.lastMove = move

    def canDefend(self,board,start:Square,piece:Piece):
        for r in range(consts.ROWS):
            for c in range(consts.COLS):
                if board.layout[r][c].isEnemy(piece.color):
                    defender = board.layout[r][c].piece
                    board.calc_moves(defender,r,c,False)

                    for m in defender.moves:
                        if not isinstance(m,Move):
                            continue
                        
                        if m.end.reward is piece:
                            return True
        return False

    def checked(self, piece, move):
        temp_piece = copy.deepcopy(piece)
        temp_board = copy.deepcopy(self)
        temp_board.move(temp_piece, move)

        for r in range(consts.ROWS):
            for c in range(consts.COLS):
                if temp_board.layout[r][c].isEnemy(temp_piece.color):
                    p = temp_board.layout[r][c].piece
                    temp_board.calc_moves(p,r,c,False)

                    for m in p.moves:
                        if not isinstance(m,Move):
                            continue
                        
                        if isinstance(m.end.reward, King):
                            if not self.canDefend(temp_board,m.start,p):
                                return True
                       
        return False

    

    def canPromote(self,end):
        return end.row == 0 or end.row == 7