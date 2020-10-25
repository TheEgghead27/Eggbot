import datetime
import threading

from cogs.commands.gamiing.ttd2 import *
# from cogs.commands.gamiing.minmax import inf, Node, MinMax
from cogs.commands.gamiing.minmaxNewOld import genNodes, inf, fuckingHell, EmptyNode


chode = {}


# noinspection PyAttributeOutsideInit,PyPropertyAccess,PyMethodOverriding
class discordTicTacAI(discordTicTac):
    def __init__(self, ctx: commands.Context, p2: discord.abc.User):
        super(discordTicTacAI, self).__init__(ctx, p2)
        self.Node = None
        self.waitig = None

    # noinspection PyTypeChecker
    async def run(self):
        self.embed = discord.Embed(title=f'Starting {self.ctx.author}\' game of TicTacToe...',
                                   description=f"⬛⬛⬛\n⬛⬛⬛\n⬛⬛⬛", color=0x00ff00)

        self.confirmMess = await self.ctx.send(embed=self.embed)

        self.p1In = DInput(self.ctx.bot, self.confirmMess, self.p1)
        self.p2In = DInput(self.ctx.bot, self.confirmMess, self.p2)

        self.gfx = DiscordX(target_message=self.confirmMess, data=dictToScanLines(self.pieces), resolution=[3, 3],
                            embed=self.embed,
                            conversionTable={'None': '⬛', 'X': '❌', 'O': '⭕',
                                             'oS': '<:oS:757696246755622923>', 'xS': '<:xS:757697702216597604>',
                                             'noneS': '<:noneS:757697725906026547>'})

        await self.p1In.initReactions()
        self.waitig = await self.ctx.send("Initializing the AI Core...")

        for i in range(9):
            self.currentPlayerID = i % 2
            print(self.currentPlayerID, self.IDtoMark(self.currentPlayerID))

            for self.player in self.players:  # figure out which player to use
                if self.players[self.player] == self.currentPlayerID:
                    break

            if self.player == '1':
                curPlayer = self.p1
                curOp = self.p2
            else:
                curPlayer = self.p2
                curOp = self.p1

            if not curPlayer.bot:
                if await self.awaitInput(curPlayer, curOp):
                    await self.cleanBoard()
                    return
            else:
                await self.aiMove()

            if self.winCheck(self.pieces):
                await self.cleanBoard()
                await self.announceWin(curPlayer, self.currentPlayerID)
                return
        await self.cleanBoard()
        await self.ctx.send('wow a tie amazing')

    def checkForUpdates(self):
        """Set self.Node to be equal to current state, if there's nothing, assume current node is up to date."""
        if not self.Node:
            global chode
            if chode and self.currentPlayerID == 0:  # save bot making first turn as a default Node
                self.Node = chode
            else:
                startTime = datetime.datetime.now()
                print('Generating!')
                #fuck = threading.Thread(target=genNodes, args=(self.currentPlayerID, self.pieces,
                #                                               self.IDtoMark(self.currentPlayerID)))
                #fuck.run()
                #fuck.join()

                #self.Node = fuck.
                self.Node = genNodes(playerNum=self.currentPlayerID, board=self.pieces,
                                     mark=self.IDtoMark(self.currentPlayerID))
                if self.currentPlayerID == 0:
                    chode = self.Node
                print(f'Generated {fuckingHell} Nodes in {datetime.datetime.now() - startTime}.')
            if self.waitig:
                asyncio.ensure_future(self.waitig.delete())
                self.waitig = None

        for i in self.Node.children:
            if i.board == self.pieces:
                self.Node = i

    idPolarityDict = {0: -1, 1: 1}

    def IDToPolarity(self, ID: int):
        return self.idPolarityDict[ID]

    async def aiMove(self):
        """Use a variant of the MinMax algorithm to make a move."""
        fuck = threading.Thread(target=self.checkForUpdates)

        fuck.run()

        # self.checkForUpdates()
        bestNode = EmptyNode()
        bestNode.value = -self.IDToPolarity(self.currentPlayerID) * inf  # use the enemy win next turn as worst move
        for i in self.Node.children:  # check every child
            # Closer to winning gives a lower result [(win - win)[∞ - ∞] = 0 / (win - lose)[∞ -- ∞] = 2∞]
            if abs(self.IDToPolarity(self.currentPlayerID) * inf - bestNode.value) > \
                    abs(self.IDToPolarity(self.currentPlayerID) * inf - i.value):
                bestNode = i
        self.pieces = bestNode.board
