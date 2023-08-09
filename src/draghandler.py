import consts
import animator

class Dragger:

    def __init__(self):
        self.mouseX = 0
        self.mouseY = 0
        self.piece = None
        self.dragging = False
        self.initCol = 0
        self.initRow = 0
    
    def updateMousePos(self,pos):
        self.mouseX, self.mouseY = pos

    def selectPiece(self):
        self.initRow = self.mouseY // consts.SQSIZE
        self.initCol = self.mouseX // consts.SQSIZE
    
    def dragPiece(self,piece):
        self.piece = piece
        self.dragging = True

    def undragPiece(self):
        self.piece = None
        self.dragging = False

    def updateScreen(self,surface):
        self.piece.getTexture(128)
        animator.drawPiece(surface,self.mouseX,self.mouseY,self.piece,60)
