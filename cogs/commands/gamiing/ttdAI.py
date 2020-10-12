import datetime
import threading

from cogs.commands.gamiing.ttd2 import *
# from cogs.commands.gamiing.minmax import inf, Node, MinMax
from cogs.commands.gamiing.minmax import genNodes


chode = None


# noinspection PyAttributeOutsideInit,PyPropertyAccess,PyMethodOverriding
class discordTicTacAI(discordTicTac):
    def __init__(self, ctx: commands.Context, p2: discord.abc.User):
        super(discordTicTacAI, self).__init__(ctx, p2)

    # noinspection PyTypeChecker
    async def run(self):
        global chode
        self.embed = discord.Embed(title=f'Starting {self.ctx.author}\' game of TicTacToe...',
                                   description=f"⬛⬛⬛\n⬛⬛⬛\n⬛⬛⬛", color=0x00ff00)

        self.confirmMess = await self.ctx.send(embed=self.embed)

        if chode is None:
            waitig = await self.ctx.send("Initializing AI Core...")
            #chode = genNodes()
            await waitig.delete()

        self.p1In = DInput(self.ctx.bot, self.confirmMess, self.p1)
        self.p2In = DInput(self.ctx.bot, self.confirmMess, self.p2)

        self.gfx = DiscordX(target_message=self.confirmMess, data=dictToScanLines(self.pieces), resolution=[3, 3],
                            embed=self.embed,
                            conversionTable={'None': '⬛', 'X': '❌', 'O': '⭕',
                                             'oS': '<:oS:757696246755622923>', 'xS': '<:xS:757697702216597604>',
                                             'noneS': '<:noneS:757697725906026547>'})

        await self.p1In.initReactions()

        for i in range(9):
            self.currentPlayerID = i % 2

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

            if self.winCheck(self.pieces):
                await self.cleanBoard()
                await self.announceWin(curPlayer, self.currentPlayerID)
                return
        await self.cleanBoard()
        await self.ctx.send('wow a tie amazing')
