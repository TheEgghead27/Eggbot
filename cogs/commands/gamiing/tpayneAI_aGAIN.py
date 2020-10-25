from sys import maxsize


# ======================================================================================================================
# TREE BUILDER
class Node:
    def __init__(self, depth: int, playerNum: int, sticksRemaining: int, value: int = 0, targetDepth: int = 0):
        """Self explanatory unless you're a wuss"""
        self.value = value
        self.sticksRemaining = sticksRemaining
        self.playerNum = playerNum
        self.depth = depth
        if targetDepth == 0:  # depth penalty so the ai chooses quicker wins
            targetDepth = depth
        self.targetDepth = targetDepth
        del targetDepth
        self.children = []
        self.CreateChildren()

    def CreateChildren(self):
        """take a wild fucking guess as to what this does"""
        if self.depth >= 0:
            for i in range(1, 3):
                v = self.sticksRemaining - i
                # watch as polarity shit was the problem in tttAI the whole fucking time
                self.children.append(Node(self.depth - 1, -self.playerNum, v, self.RealVal(v), self.targetDepth))

    def RealVal(self, value: int):
        """Guess what? Chicken butt"""
        if value == 0:
            return maxsize * self.playerNum
        elif value < 0:
            return maxsize * -self.playerNum
        return 0


# ======================================================================================================================
# ALGORITHM
def MinMax(node: Node, depth: int, playerNum: int):
    """hmmm what could this be"""
    if (depth == 0) or (abs(node.value) > 0):
        return node.value

    bestValue = maxsize * -playerNum

    for child in node.children:
        val = MinMax(child, depth - 1, -playerNum)
        if (abs(maxsize * playerNum - val)) < (abs(maxsize * playerNum - bestValue)):
            bestValue = val

    return bestValue - abs(node.depth - node.targetDepth)


# ======================================================================================================================
# IMPLEMENTATION
def winCheck(sticks, playerNum):
    """Guess what? Chicken butt^2"""
    if sticks <= 0:
        print('*' * 30)
        if playerNum > 0:
            if sticks == 0:
                print("\tYOU WIN!")
            else:
                print('\tTOO MANY! You lose...')
        else:
            if sticks == 0:
                print("\tComp Wins... Better luck next time.")
            else:
                print('fuck')
        print('*' * 30)
        return 0
    return 1


if __name__ == '__main__':
    i_stickTotal = 11
    i_depth = 4
    i_curPlayer = 1  # 1 is human, -1 is bot, maybe consider that next time, eh asshole?
    print('pick up 1 or 2 sticks, you should get the last stick')
    while i_stickTotal > 0:
        print(f'{i_stickTotal} sticks are left how many sticks lol\n')
        i_stickTotal -= int(float(input('\n1 or 2')))
        if winCheck(i_stickTotal, i_curPlayer):
            # important shit pay attention
            i_curPlayer *= -1  # fliperoni to -1 with bot
            print(f'{i_stickTotal} sticks are left computer turn lemoa')
            node = Node(i_depth, i_curPlayer, i_stickTotal)
            bestChoice = -100
            i_bestValue = -i_curPlayer * maxsize
            for i in range(len(node.children)):
                n_child = node.children[i]
                i_val = MinMax(n_child, i_depth, -i_curPlayer)  # negative to the user???
                if (abs(maxsize * i_curPlayer - i_val)) < (abs(maxsize * i_curPlayer - i_bestValue)):
                    i_bestValue = i_val
                    bestChoice = i + 1
            print(f'ai chose {bestChoice}\tbased on {i_bestValue}')
            i_stickTotal -= bestChoice
            winCheck(i_stickTotal, i_curPlayer)
            i_curPlayer *= -1

