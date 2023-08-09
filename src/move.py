from square import * 

class Move:

    def __init__(self, start:Square, end:Square):
        self.start = start
        self.end = end

    def __eq__(self, other: object) :
        return self.start == other.start and self.end == other.end
    
    def show(self):
        print(self.start.row,self.start.col,self.end.row,self.end.col)