from sys import maxsize  # infinity (a really big number)


class Node(object):
    def __init__(self, i_depth, i_playerNum, i_sticksRemaining, i_value=0):
        self.i_depth = i_depth  # how deep are we in the tree (decreases every iteration
        self.i_playerNum = i_playerNum  # (either +1 or -1)
        self.i_sticksRemaining = i_sticksRemaining  # amount of sticks left
        self.i_value = i_value  # gamestate: -inf, 0 or +inf
        self.children = []
        self.CreateChildren()

    def CreateChildren(self):
        if self.i_depth >= 0:  # have we passed the DEPTH of 0 (stop of recursion)
            for i in range(1, 3):  # (how many stick are we gonna remove)
                v = self.i_sticksRemaining - i
                self.children.append(Node(self.i_depth - 1, -self.i_playerNum, v,
                                          self.RealVal(v)))  # add to childrens list, depth goes down, player switches

    def RealVal(self, value):
        if (value == 0):
            return maxsize * self.i_playerNum  # e.g. bullybot
        elif (value < 0):
            return maxsize * -self.i_playerNum  # this bot
        return 0


def MinMax(node, i_depth, i_playerNum):
    if (i_depth == 0) or (abs(node.i_value) == maxsize):  # have we reached depth 0 or the best node?
        return node.i_value  # passing the best node up to the current node

    i_bestValue = maxsize * -i_playerNum  # possitive p

    for i in range(len(node.children)):
        child = node.children[i]
        i_val = MinMax(child, i_depth - 1, -i_playerNum)
        if (abs(maxsize * i_playerNum - i_val) < abs(maxsize * i_playerNum - i_bestValue)):
            i_bestValue = i_val  # store the found best value in this variable

    # debug
    return i_bestValue


def WinCheck(i_sticks, i_playerNum):
    if i_sticks <= 0:
        print("*" * 30)
        if i_playerNum > 0:
            if i_sticks == 0:
                print("\tHuman won!")
            else:
                print("\tToo many chosen, you lost!")
        else:
            if i_sticks == 0:
                print("\tComputer won!")
            else:
                print("\tComputer done did fucked up..")
        print("*" * 30)
        return 0
    return 1


if __name__ == '__main__':
    i_stickTotal = 11
    i_depth = 4
    i_curPlayer = 1
    print("""Instructions: Be the player to pick up the last stick.
                \t\t\tYou can only pick up one (1) or two (2) at a time.""")

    while (i_stickTotal > 0):
        ## HUMAN TURN
        print("\n%d sticks remain. How many will you pick up?" % i_stickTotal)
        i_choice = input("\n1 or 2:                 ")
        # i_choice = 1 debug
        i_stickTotal -= int(float(i_choice))  # store choice of human
        ## COMPUTER TURN
        if WinCheck(i_stickTotal, i_curPlayer):
            i_curPlayer *= -1
            node = Node(i_depth, i_curPlayer, i_stickTotal)
            bestChoice = -100
            i_bestValue = -i_curPlayer * maxsize
            ## DETERMINE NUMBER OF STICKS TO REMOVE
            for i in range(len(node.children)):
                n_child = node.children[i]
                i_val = MinMax(n_child, i_depth, -i_curPlayer)
                if (abs(i_curPlayer * maxsize - i_val) <=
                        abs(i_curPlayer * maxsize - i_bestValue)):
                    i_bestValue = i_val
                    bestChoice = i
            bestChoice += 1
            print("Comp chooses: " + str(bestChoice) + "\tBased on value: " + str(i_bestValue))
            i_stickTotal -= bestChoice
            WinCheck(i_stickTotal, i_curPlayer)
            i_curPlayer *= -1  # switch players