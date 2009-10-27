import exceptions

class Game(object):
    '''
    classdocs
    '''
    def __init__(self, computerOpen=False):
        '''
        Constructor
        '''
        self.computerOpen = computerOpen
        self._gameState = [None, None, None, None, None, None, None, None,None]
    def start(self):
        if (self.isOver()):
            raise exceptions.RuntimeError
        if self.computerOpen == True:
            self.answer()
    def gameState(self):
        return self._gameState
    
    def move(self, fieldAddress):
        if self._gameState[fieldAddress] is not None:
            raise exceptions.RuntimeError
        self._gameState[fieldAddress] = 'x'
    def isOver(self):
        return (   all(self._gameState) 
                or self.searchRowDiagonally() 
                or self.searchRowHorizontally() 
                or self.searchRowVertically()
        )
    def searchRowHorizontally(self):
        for i in range(0,3):
            row = self._gameState[3*i:3*i+3]
            if self.isRowOfSameKind(row):
                return True
        return False
    def searchRowVertically(self):
        for i in range(0,3):
            row = self._gameState[i::3]
            if self.isRowOfSameKind(row):
                return True
        return False
    def searchRowDiagonally(self):
        row = [self._gameState[0], self._gameState[4], self._gameState[8]]
        if self.isRowOfSameKind(row):
            return True
        row = [self._gameState[2], self._gameState[4], self._gameState[6]]
        if self.isRowOfSameKind(row):
            return True
        return False
    def isRowOfSameKind(self, row):
        if all(row) and len(dict.fromkeys(row).keys())==1:
            return True        
        return False
    def answer(self):
        index = self._gameState.index(None)
        self._gameState[index] = 'o'
    def play(self, fieldAddress):
        self.move(fieldAddress)
        if not self.isOver():
            self.answer()
class CleverAI(object):
    def __init__(self):
        self.game = None
    def setGame(self,game):
        self.game = game
    def answer(self):
        move = self.spotWinningRow()
        if move is not None:
            return move
        move = self.spotBlockingRow()
        if move is not None:
            return move
        return self.randomMove()
        

    def spotBlockingRow(self):
        return self.spotWinningRow('x')
    def spotWinningRow(self, mark='o'):
        game = self.game._gameState
        #horizontal
        for i in range(0,3):
            row = game[i*3:i*3+3]
            if self.isCandidateRow(row, mark):
                return (game[i*3:]).index(None)+3*i
        #vertical
        for i in range(0,3):
            row = game[i::3]
            if self.isCandidateRow(row, mark):
                return 3*row.index(None)+i
        #diagonal
        row = [game[0], game[4], game[8]]
        if self.isCandidateRow(row, mark):
            return row.index(None)*4
        row = [game[2], game[4], game[6]]
        if self.isCandidateRow(row, mark):
            return row.index(None)*2 + 2
        return None
   
    def isCandidateRow(self, row, mark):
        if row.count(None) == 1 and mark in row and len(dict.fromkeys(row).keys())==2:
            return True
        return False    

    def randomMove(self):
        return self.game._gameState.index(None) 