import pygame

import consts
import animator

from board import *
from draghandler import *
from config import *


class Game:

    def __init__(self):
        self.board = Board()
        self.config = Config()
        self.currPlayer = 'white'
        self.dragger = Dragger()

    def nextPlayer(self):
        self.currPlayer = 'white' if self.currPlayer == 'black' else 'black'

    def drawBG(self, surface):

        for r in range(consts.ROWS):
            for c in range(consts.COLS):
                if (r+c) % 2 == 0:
                    color = (200,174,125)
                else:
                    color = (101,69,31)
                
                rect = (c * consts.SQSIZE, r * consts.SQSIZE, consts.SQSIZE, consts.SQSIZE)

                pygame.draw.rect(surface,color,rect)

    def drawPieces(self, surface):
        for r in range(consts.ROWS):
            for c in range(consts.COLS):
                if self.board.layout[r][c].piece is self.dragger.piece:
                    continue

                if self.board.layout[r][c].isOccupied():
                    piece = self.board.layout[r][c].piece

                    posX = c * consts.SQSIZE + consts.SQSIZE // 2
                    posY = r * consts.SQSIZE + consts.SQSIZE // 2
                    
                    animator.drawPiece(surface,posX,posY,piece)

    def showMoves(self, surface):
        if self.dragger.dragging:
            piece = self.dragger.piece
            for move in piece.moves:
                rect = (move.end.col * consts.SQSIZE, move.end.row * consts.SQSIZE, consts.SQSIZE, consts.SQSIZE ) 
                color = consts.moveColorDark if (move.end.row+move.end.col) % 2 == 0 else consts.moveColorLight
                pygame.draw.rect(surface,color,rect)

    def showLastMove(self, surface):
        if self.board.lastMove:
            start = self.board.lastMove.start
            end = self.board.lastMove.end

            for sq in [start,end]:
                color = consts.lastMoveColorDark if (sq.row+sq.col)%2 == 0 else consts.lastMoveColorLight
                rect = (sq.col * consts.SQSIZE,sq.row * consts.SQSIZE,consts.SQSIZE,consts.SQSIZE)
                pygame.draw.rect(surface,color,rect)

    def playSound(self, soundName):
        self.config.sounds[soundName].play()