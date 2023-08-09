import pygame

from piece import *

def drawPiece(surface,posX,posY,piece : Piece,imgSize=45):
    img = pygame.image.load(piece.texture)
    img = pygame.transform.scale(img, (imgSize,imgSize))
    img_centre = posX,posY
    piece.textureRect = img.get_rect(center=img_centre)
    surface.blit(img, piece.textureRect)