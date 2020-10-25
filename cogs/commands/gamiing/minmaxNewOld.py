import threading  # actual blast processing so things don't run like shit
from sys import maxsize as inf
from cogs.commands.gamiing.tictacterminal import *


fuckingHell = 0
marks = {
    'X': 'O', 'O': 'X',
}


# ======================================================================================================================
# TREE BUILDER
class EmptyNode:
    def __init__(self):
        self.board = {'a1': None, 'a2': None, 'a3': None, 'b1': None, 'b2': None, 'b3': None, 'c1': None, 'c2': None,
                      'c3': None}
        self.mark = 'Y'
        self.curMark = 'Z'
        self.parent = None
        self.playerNum = 0
        self.value = 0
        self.children = []


class Node(EmptyNode):
    def __init__(self, playerNum: int, board: dict, myMark: str, curMark: str, parent=None):
        super().__init__()
        global fuckingHell
        fuckingHell += 1
        self.board = board  # game state
        self.mark = myMark  # mark of your side
        self.curMark = curMark  # mark taking the current turn
        self.parent = parent  # parent Node object to add yourself to the children
        self.playerNum = playerNum  # polarity of you
        self.value = self.RealVal(self.board)  # check for wins, if no win, then nothing
        self.children = []
        if self.value == 0:  # with no win
            self.CreateChildren()  # try to make children
            for i in self.children:  # for all your children
                self.value += i.value  # add their value to the total
            if self.value:
                self.value /= len(self.children)  # then get the average
        if self.parent:  # if there is mama
            self.parent.children.append(self)  # devote yourself to mother

    def CreateChildren(self):
        nodes = []
        threads = []
        if None in self.board.values():  # if we didn't fill board
            for i in self.board:  # search board
                if self.board[i] is None:  # if that space is empty
                    v = self.board.copy()  # make temp copy
                    v[i] = self.curMark  # slap current turn onto the board
                    # make more childs
                    nodes.append((self.playerNum, v, self.mark, marks[self.mark], self))

            # 4 thread system
            # # part 1
            # p1 = nodes[:int(len(nodes) / 2)]
            # threads.append(threading.Thread(target=self.runNodeChunk, args=p1[:int(len(p1) / 2)]))
            # threads.append(threading.Thread(target=self.runNodeChunk, args=p1[int(len(p1) / 2):]))
            # # part 2
            # p2 = nodes[:int(len(nodes) / 2)]
            # threads.append(threading.Thread(target=self.runNodeChunk, args=p2[:int(len(p2) / 2)]))
            # threads.append(threading.Thread(target=self.runNodeChunk, args=p2[int(len(p2) / 2):]))

            # 2 thread system
            threads.append(threading.Thread(target=self.runNodeChunk, args=nodes[:int(len(nodes) / 2)]))
            threads.append(threading.Thread(target=self.runNodeChunk, args=nodes[int(len(nodes) / 2):]))

            for i in threads:  # for all the prepared fetuses
                i.start()  # birth
            for i in threads:  # for all the born children
                i.join()  # wait for the hospital man to overcharge you

    # noinspection PyMethodMayBeStatic
    def runNodeChunk(self, *args):
        for i in args:
            Node(i[0], i[1], i[2], i[3], i[4])

    def RealVal(self, board: dict):
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

    def returnWin(self, winner: str):
        if winner == self.mark:
            return inf * self.playerNum
        else:
            return inf * -self.playerNum


def genNodes(playerNum=-1, board=None, mark='X'):
    """Generates an initial node based on default settings."""
    if board is None:
        board = {'a1': None, 'a2': None, 'a3': None, 'b1': None, 'b2': None, 'b3': None, 'c1': None, 'c2': None,
                 'c3': None}
    return Node(playerNum=playerNum, board=board, myMark=mark, curMark=mark)


def countNodes():
    return f'{fuckingHell}'

# ======================================================================================================================
