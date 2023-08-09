class Square:

    def __init__(self,row,col,reward=None):
        self.row = row
        self.col = col
        self.reward = reward
        self.piece = reward

    def isOccupied(self):
        return self.piece != None
    
    def isAlly(self,color):
        return self.isOccupied() and self.piece.color == color

    def isEnemy(self,color):
        return self.isOccupied() and self.piece.color != color

    def isEmptyOrEnemy(self,color):
        return not self.isAlly()

    @staticmethod
    def inRange(*args):
        for arg in args:
            if arg < 0 or arg > 7:
                return False
        return True
    
    def __eq__(self, other: object):
        return self.row == other.row and self.col == other.col