import threading  # actual blast processing so things don't run like shit
from sys import maxsize as inf
from cogs.commands.gamiing.tictacterminal import *


fuckingHell = 0
marks = {
    'X': 'O', 'O': 'X',
}


# ======================================================================================================================
# TREE BUILDER
class Node:
    def __init__(self, playerNum: int, board: dict, mark: str, parent=None):
        global fuckingHell
        fuckingHell += 1
        self.board = board
        self.mark = mark
        self.parent = parent
        self.playerNum = playerNum

    def RealVal(self, board: dict, mark: str):
        """
        if win, award yourself infinity; if lose, award yourself negative infinity; if nothing happened, award nothing
        """
        XList = ['X..X..X', 'X...X...X', '..X.X.X..']  # columns and diagonals
        OList = ['O..O..O', 'O...O...O', '..O.O.O..']

        # stringify the data for column and diagonals
        data = ''
        for i in board.values():
            if i is not None:
                data += i
            else:
                data += ' '
        for i in XList:
            for _ in re.findall(i, data):
                if 'X' == mark.upper():
                    return inf * self.i_playerNum
                else:
                    return inf * -self.i_playerNum
        for i in OList:
            for _ in re.findall(i, data):
                if 'O' == mark.upper():
                    return inf * self.i_playerNum
                else:
                    return inf * -self.i_playerNum

        # row check
        for rowLetter in ['a', 'b', 'c']:
            data = ''
            for piece in board:
                if piece.lower()[0] == rowLetter:
                    i = board[piece]
                    if i is not None:
                        data += i
                    else:
                        data += ' '
            if data == 'XXX':
                if 'X' == mark.upper():
                    return inf * self.i_playerNum
                else:
                    return inf * -self.i_playerNum
            elif data == 'OOO':
                if 'O' == mark.upper():
                    return inf * self.i_playerNum
                else:
                    return inf * -self.i_playerNum
        return 0


def genNodes(playerNum=0, board=None, mark='X'):
    """Generates an initial node based on default settings."""
    if board is None:
        board = {'a1': None, 'a2': None, 'a3': None, 'b1': None, 'b2': None, 'b3': None, 'c1': None, 'c2': None,
                 'c3': None}
    return Node(playerNum=playerNum, board=board, mark=mark)


# ======================================================================================================================
# ALGORITHM
def MinMax(node, i_depth, i_playerNum):
    global fuckingHell
    if fuckingHell:
        print(fuckingHell)
        fuckingHell = 0
    if (i_depth == 0) or (abs(node.i_value) == inf):  # we either went as deep as we were supposed to, or someone won
        if node.done:
            return node.i_value / 9
        return node.i_value

    i_bestValue = inf * i_playerNum  # playerNum *should be the enemy, so opposite it (why did you not do that before)

    for child in node.children:  # vibe check all the children to see if they meet the above
        i_val = MinMax(child, i_depth - 1, -i_playerNum)  # address the depth change, reverse the player number

        # if the current value is better than the best, make it king
        if abs(inf * i_playerNum - i_val) < (abs(inf * i_playerNum - i_bestValue)):
            i_bestValue = i_val

    return (i_bestValue / 9) * 8
