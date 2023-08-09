import pygame
import sys

import consts
import game
from move import *
from square import *

class Main:

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode( (consts.WIDTH, consts.HEIGHT) )
        pygame.display.set_caption("Chess")
        self.game = game.Game()
        self.board = self.game.board
        self.dragger = self.game.dragger

    def mainloop(self):

        while True:
            self.game.drawBG(self.screen)
            self.game.showLastMove(self.screen)
            self.game.showMoves(self.screen)
            self.game.drawPieces(self.screen)

            if self.dragger.dragging:
                self.dragger.updateScreen(self.screen)

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:

                    self.dragger.updateMousePos(event.pos)
                    
                    selectedRow = self.dragger.mouseY // consts.SQSIZE
                    selectedCol = self.dragger.mouseX // consts.SQSIZE

                    if Square.inRange(selectedCol,selectedRow) and self.board.layout[selectedRow][selectedCol].isOccupied():
                        piece = self.board.layout[selectedRow][selectedCol].piece
                        if piece.color != self.game.currPlayer:
                            break


                        self.board.calc_moves(piece,selectedRow,selectedCol,True)
                        self.dragger.selectPiece()
                        self.dragger.dragPiece(piece)

                        self.game.drawBG(self.screen)
                        self.game.showMoves(self.screen)
                        self.game.drawPieces(self.screen)

                elif event.type == pygame.MOUSEMOTION:
                    if self.dragger.dragging:
                        self.dragger.updateMousePos(event.pos)
                        self.game.drawBG(self.screen)
                        self.game.showLastMove(self.screen)
                        self.game.showMoves(self.screen)
                        self.game.drawPieces(self.screen)
                        self.dragger.updateScreen(self.screen)

                elif event.type == pygame.MOUSEBUTTONUP:
                    if self.dragger.dragging:
                        self.dragger.updateMousePos(event.pos)

                        releasedRow = self.dragger.mouseY // consts.SQSIZE
                        releasedCol = self.dragger.mouseX // consts.SQSIZE

                        start = Square(self.dragger.initRow,self.dragger.initCol)
                        end = Square(releasedRow,releasedCol)
                        move = Move(start,end)

                        if self.board.valid_move(piece,move):

                            captured = self.board.layout[move.end.row][move.end.col].isOccupied()  
                            sName = "capture" if captured else "move"
                            self.game.playSound(sName)
                            
                            self.board.move(self.dragger.piece,move)
                            self.game.drawBG(self.screen)
                            self.game.showLastMove(self.screen)
                            self.game.drawPieces(self.screen)
                            self.game.nextPlayer()

                    self.dragger.undragPiece()
                    

                elif event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                


            pygame.display.update()


console = Main()
console.mainloop()