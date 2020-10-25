from sys import maxsize as inf
import re


marks = {
    'X': 'O', 'O': 'X',
}
XList = ['X..X..X', 'X...X...X', '..X.X.X..']  # columns and diagonals
OList = ['O..O..O', 'O...O...O', '..O.O.O..']


# ======================================================================================================================
# TREE BUILDER
class DataNode:
    def __init__(self, board: dict, curMark: str, playerNum: int, value: int = 0, depth: int = 0):
        self.board = board
        self.curMark = curMark
        self.playerNum = playerNum
        self.value = value
        self.children = []
        self.depth = depth


class ActiveNode(DataNode):
    def __init__(self, board: dict, curMark: str, playerNum: int, value: int = 0, depth: int = 0):
        super(ActiveNode, self).__init__(board=board, curMark=curMark, value=value, playerNum=playerNum, depth=depth)
        self.CreateChildren()

    def CreateChildren(self):
        if self.value == 0 and None in self.board.values():
            for i in self.board:  # search board
                if self.board[i] is None:  # if that space is empty
                    v = self.board.copy()  # make temp copy
                    v[i] = self.curMark  # slap current turn onto the board
                    # watch as polarity shit was the problem in tttAI the whole fucking time
                    self.children.append(ActiveNode(board=v, curMark=marks[self.curMark], value=self.RealVal(v),
                                                    playerNum=-self.playerNum, depth=self.depth + 1))

    def RealVal(self, board: dict):
        """
        if win, award yourself infinity; if lose, award yourself negative infinity; if nothing happened, award nothing
        """

        # stringify the data for column and diagonals
        data = ''
        for i in board.values():
            if i is not None:
                data += i
            else:
                data += ' '
        for i in XList:
            for _ in re.findall(i, data):
                return self.returnWin('X')
        for i in OList:
            for _ in re.findall(i, data):
                return self.returnWin('O')

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
                return self.returnWin('X')
            elif data == 'OOO':
                return self.returnWin('O')
        return 0

    def returnWin(self, winningMark: str):
        if winningMark == self.curMark:
            return inf * self.playerNum
        else:
            return inf * -self.playerNum


# ======================================================================================================================
# ALGORITHM
def MinMax(node: ActiveNode, playerNum: int):
    """hmmm what could this be"""
    if abs(node.value) > 0:
        return node.value - fuck(node.value, node.depth)

    bestValue = inf * -playerNum

    for child in node.children:
        val = MinMax(child, -playerNum)
        if (abs(inf * playerNum - val)) < (abs(inf * playerNum - bestValue)):
            bestValue = val

    return bestValue - fuck(node.value, node.depth)


def fuck(target: int, depth: int):
    """Returns the depth times the polarity of the target"""
    try:
        return (target / abs(target)) * depth
    except ZeroDivisionError:
        return depth
