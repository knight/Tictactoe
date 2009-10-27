import exceptions
import unittest
import tictactoe


class GameTests(unittest.TestCase):


    def setUp(self):
        self.sut = tictactoe.Game()
    def tearDown(self):
        pass
    def testGameShouldStartEmpty(self):
        sut = self.sut
        self.assertEquals(
            [None, None, None, None, None, None, None, None, None ], 
            sut.gameState()
        )
    def testPlayerShouldCheckAnEmptyField(self):
        sut = self.sut
        sut.move(0)
        self.assertTrue('x' in sut.gameState())
    def testPlayerShouldNotBeAbleToCheckAnOccupiedField(self):
        sut = self.sut
        sut.move(0)
        self.failUnlessRaises(exceptions.RuntimeError, sut.move, 0)
    def testIfThereIsThreeInARowTheGameIsOver(self):
        sut = self.sut
        sut.move(0)
        sut.move(1)
        sut.move(2)
        self.assertTrue(sut.isOver(), "The game should be over. There's a row")
    def testTheGameIsOverIfThereIsAVerticalRow(self):
        sut = self.sut
        sut.move(0)
        sut.move(3)
        sut.move(6)
        self.assertTrue(sut.isOver(), "The game should be over. There's a vertical row")
    def testTheGameIsOverIfThereIsADiagonalRow(self):
        sut = self.sut
        sut.move(0)
        sut.move(4)
        sut.move(8)
        self.assertTrue(sut.isOver(), "The game should be over")
    def testTheGameIsOverIfRowIsOfTheSameKind(self):
        sut = self.sut
        sut._gameState = ['x', 'x', 'o', None, None, None, None, None, None]
        self.assertFalse(sut.isOver(), "The game can only be over if the row is of the same kind")
    def testIfThereAreNotThreeInTheRowTheGameIsNotOver(self):
        sut = self.sut
        sut.move(0)
        sut.move(1)
        self.assertFalse(sut.isOver(), "After two moves the game should not be finished yet")
    def testTheGameIsOverIfThereAreNoFreeFieldLeft(self):
        sut = self.sut
        sut._gameState = ['x','o','x', 
                          'o','x','x',
                          'o','x','o']
        self.assertTrue(sut.isOver(), "No place left to make a new move")
    def testIfThereIsAMoveThereIsAResponse(self):
        sut = self.sut
        sut.move(0)
        sut.answer()
        self.assertTrue('o' in sut.gameState())
    def testIfComputerStartsThereShouldAlreadyBeComputersMove(self):
        sut = tictactoe.Game(computerOpen = True)
        sut.start()
        self.assertTrue('o' in sut._gameState, 'The computer starts so there should be at least one of its marks')
    def testYouCanNotStartAnAlreadyFinishedGame(self):
        sut = tictactoe.Game()
        sut._gameState = ['o','o','x',
                          'x','o','o',
                          'o','x','x']
        self.failUnlessRaises(exceptions.RuntimeError, sut.start)
    def testTheComputerBeginsAndShouldEasilyBeTheWinnar(self):
        sut = tictactoe.Game(computerOpen=True)
        sut.start()
        sut.play(3)
        sut.play(6)
        self.assertTrue(sut.isOver(), "The computer should easily win")

class AiTest(unittest.TestCase):
    def setUp(self):
        self.sut = tictactoe.CleverAI()
        
    def tearDown(self):
        pass
    def testTheAIShouldSpotAnOpportunityToWin(self):
        sut = self.sut
        fake = tictactoe.Game()
        fake._gameState =  [
                  'o','x','x',
                  None,'o','x',
                  None,None,None
        ]
        sut.setGame(fake)
        sut.answer()
        self.assertEqual(8, sut.answer())
    def testTheAIShouldSpotAnOpportunityToBlock(self):
        sut = self.sut
        fake = tictactoe.Game()
        fake._gameState = [
                  'o', 'x', 'x',
                  None,'x', None,
                  None,'o', None                           
        ]
        sut.setGame(fake)
        self.assertEqual(6,sut.answer(), "The AI should be clever enough to block the opponent")
    def testTheAIShouldTryToWinInsteadBlockingTheOpponent(self):
        sut = self.sut
        fake = tictactoe.Game()
        fake._gameState = [
                 'x', None,  'o',
                 'x', None,  'o',
                None, None, None
        ]
        sut.setGame(fake)
        self.assertEqual(8, sut.answer(), "To Win is a better strategy")
    def testTheAIShouldMakeAMoveEvenIfThereIsNoOpportunity(self):
        sut = self.sut
        fake = tictactoe.Game()
        fake._gameState = [
                'x', None, 'o',
                None, None, None,
                None, None, None
        ]
        sut.setGame(fake)
        self.assertTrue(sut.answer() is not None, "The AI could choose a move to make")
        
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testGameShouldStartEmpty']
    unittest.main()