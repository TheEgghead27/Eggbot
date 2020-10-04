from sys import maxsize as inf
from cogs.commands.gamiing.tictacterminal import *


# ======================================================================================================================
# TREE BUILDER
class Node:
    def __init__(self, i_depth, i_playerNum, board, mark, winCheck, i_value=0):
        self.i_depth = i_depth
        self.i_playerNum = i_playerNum
        self.board = board
        self.mark = mark
        self.winCheck = winCheck
        self.i_value = i_value
        self.children = []
        self.CreateChildren()

    def CreateChildren(self):
        if self.i_depth >= 0:  # if we're supposed to make more childs
            for i in self.board:  # make children that remove either 1 or 2 sticks
                if self.board[i] is None:  # if that space is empty
                    v = self.board[i].copy()
                    v[i] = self.mark
                    # make more childs
                    self.children.append(Node(self.i_depth - 1, -self.i_playerNum, v, self.mark, self.winCheck,
                                              self.RealVal(v)))

    def RealVal(self, value):
        if value == 0:  # if win, award yourself infinity
            return inf * self.i_playerNum
        elif value < 0:  # if lose, award yourself negative infinity
            return inf * -self.i_playerNum
        return 0  # if nothing happened, award nothing


# ======================================================================================================================
# ALGORITHM
def MinMax(node, i_depth, i_playerNum):
    if (i_depth == 0) or (abs(node.i_value) == inf):  # we either went as deep as we were supposed to, or someone won
        return node.i_value

    i_bestValue = inf * -i_playerNum  # playerNum *should be the enemy, so opposite it (why did you not do that before)

    for child in node.children:  # vibe check all the children to see if they meet the above
        i_val = MinMax(child, i_depth - 1, -i_playerNum)  # address the depth change, reverse the player number

        # if the current value is better than the best, make it king
        if abs(inf * i_playerNum - i_val) < (abs(inf * i_playerNum - i_bestValue)):
            i_bestValue = i_val

    return i_bestValue


class minMaxTicTac(ticTacToe):
    def __init__(self):
        super(minMaxTicTac, self).__init__()

    def awaitP2Input(self):
        print(f'AI\'s turn. ({self.IDtoMark(self.currentPlayerID)})')
        self.userInput()
        if True:
            if self.currentPlayerID == 0:
                i_curPlayer = -1
            else:
                i_curPlayer = self.currentPlayerID
            depth = 0
            for i in self.pieces:
                if self.pieces[i] is None:  # if that space is empty
                    depth += 1
            # make some childrens with the current info
            node = Node(depth, i_curPlayer, self.IDtoMark(self.currentPlayerID), self.pieces, self.winCheck)
            bestChoice = -100  # placeholder
            i_bestValue = -i_curPlayer * inf  # placeholder of enemy win (worst value)
            for i in range(len(node.children)):  # search all the childrens
                n_child = node.children[i]
                i_val = MinMax(n_child, depth, -i_curPlayer)  # get the best value from those childs
                if abs(i_curPlayer * inf - i_val) <= abs(i_curPlayer * inf - i_bestValue):  # if this value is best
                    # it gets Chosen
                    i_bestValue = i_val
                    bestChoice = i
            print(f'Comp chooses: {str(bestChoice)}\tBased on value: {str(i_bestValue)}')
            self.processInput(bestChoice)  # choose the choice
