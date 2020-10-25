import threading  # actual blast processing so things don't run like shit
from sys import maxsize as inf
from cogs.commands.gamiing.tictacterminal import *


fuckingHell = 0
marks = {
    'X': 'O', 'O': 'X',
}


def flipFlop(mark):
    return marks[mark]

# ======================================================================================================================
# TREE BUILDER
class Node:
    def __init__(self, i_depth, i_playerNum, board, mark, winCheck, i_value=0, parent=None, done=False):
        global fuckingHell
        fuckingHell += 1
        self.i_depth = i_depth
        self.i_playerNum = i_playerNum
        self.board = board
        self.mark = mark
        self.winCheck = winCheck
        self.i_value = i_value
        self.children = []
        self.parent = parent
        self.done = (abs(i_value) == inf)
        self.CreateChildren()

    def CreateChildren(self):
        threads = []
        if (self.i_depth >= 0) and (self.i_value == 0):  # if we're supposed to make more childs and we didn't reach end
            for i in self.board:  # make children that remove either 1 or 2 sticks
                if self.board[i] is None:  # if that space is empty
                    v = self.board.copy()
                    v[i] = self.mark
                    # make more childs
                    threads.append(threading.Thread(target=Node, args=(self.i_depth - 1, -self.i_playerNum, v,
                                                                       flipFlop(self.mark), self.winCheck,
                                                                       self.RealVal(v, self.mark), self, self.done)))
            for i in threads:
                i.start()
                i.join()
        if self.parent:
            self.parent.children.append(self)
        else:
            print('alive')

    # noinspection PyMethodMayBeStatic
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


if __name__ == '__main__':
    import datetime

    # noinspection PyShadowingNames
    def fuckMe(node):
        for i in node.children:
            fuckMe(i)
        print(node.board)
        print(node.i_value)


    print('do')
    startTime = datetime.datetime.now()
    # make curPlayer correspond to positive or negative
    i_curPlayer = -1

    depth = 0
    board = {'a1': None, 'a2': None, 'a3': None, 'b1': None, 'b2': None, 'b3': None, 'c1': None, 'c2': None,
             'c3': None}
    for i in board.values():
        if i is None:  # if that space is empty
            depth += 1  # queue a depth

    # make some childrens with the current info
    node = Node(depth, i_curPlayer, board, 'O', None)
    print(f'Nodes have been generated in: {datetime.datetime.now() - startTime}')
    i_bestValue = -i_curPlayer * inf  # placeholder of enemy win (worst value)
    i_bestNode = node
    for n_child in node.children:  # search all the childrens
        i_val = MinMax(n_child, depth, -i_curPlayer)  # get the best value from those childs
        if abs(i_curPlayer * inf - abs(i_val)) < abs(i_curPlayer * inf - i_bestValue):  # if this value is best
            print('a Chosen one')
            print(i_val, i_bestValue)
            print(abs(i_curPlayer * inf - i_val), abs(i_curPlayer * inf - i_bestValue))
            # it gets Chosen
            i_bestNode = n_child
            print(i_bestNode.i_value)
            i_bestValue = abs(i_val)
    print(f'Best Node: {i_bestNode.board}')
    print(f'Best Node Child: {i_bestNode.children[0].i_value}')
    fuckMe(node=i_bestNode)
    print(datetime.datetime.now() - startTime)
    # self.fuckMe(i_bestNode)
