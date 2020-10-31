import random
from cogs.commands.gamiing.minmax import MinMax, inf
from cogs.commands.gamiing.minmax import conduncedMainNode as ActiveNode
from cogs.commands.gamiing.tictacterminal import ticTacToe

fuckers = {0: -1, 1: 1}


class tttAi(ticTacToe):
    def __init__(self):
        super(tttAi, self).__init__()
        self.awaitPInput = self.awaitP1Input
        if random.randrange(0, 2):
            self.awaitP1Input = self.awaitPInput
            self.awaitP2Input = self.aiTurn
        else:
            self.awaitP1Input = self.aiTurn
            self.awaitP2Input = self.awaitPInput
        self.aiConditional = lambda i_curPlayer, i_val, bestValue: \
            (abs(inf * i_curPlayer - i_val)) < (abs(inf * i_curPlayer - bestValue))

    # noinspection PyShadowingNames
    def aiTurn(self):
        """Use a variant of the MinMax algorithm to make a move."""
        print(f'AI\'s turn. ({self.IDtoMark(self.currentPlayerID)})')
        i_curPlayer = fuckers[self.currentPlayerID]
        node = ActiveNode(board=self.pieces, curMark=self.IDtoMark(self.currentPlayerID),
                          playerNum=fuckers[self.currentPlayerID])
        bestChoice = self.search(node, i_curPlayer)
        if self.pieces != bestChoice:
            self.pieces = bestChoice
        else:
            # switch to the secondary conditional because fuck you
            # a new class is inited for every game, so this is fine
            self.aiConditional = lambda i_curPlayer, i_val, bestValue: \
                (abs(inf * i_curPlayer - i_val)) > (abs(inf * i_curPlayer - bestValue))
            bestChoice = self.search(node, i_curPlayer)
            if self.pieces != bestChoice:
                self.pieces = bestChoice
            else:
                # exit plan 😎
                print('shite')
                exit()

    def search(self, node: ActiveNode, i_curPlayer: int):
        bestChoice = self.pieces
        bestValue = -i_curPlayer * inf
        for n_child in node.children:
            i_val = MinMax(n_child, -i_curPlayer)  # negative to the user???
            if self.aiConditional(i_curPlayer, i_val, bestValue):
                bestValue = i_val
                bestChoice = n_child.board
        return bestChoice


if __name__ == '__main__':
    game = tttAi()
    game.run()
