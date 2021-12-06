import concurrent.futures

import datetime

from cogs.commands.gamiing.ttd2 import *
from cogs.commands.gamiing.tttAI import *


chode = {}


# noinspection PyAttributeOutsideInit,PyPropertyAccess,PyMethodOverriding
class discordTicTacAI(discordTicTac):
    def __init__(self, ctx: commands.Context):
        """fuck subclassing tttAI overwriting it all here makes much more sense"""
        discordTicTac.__init__(self, ctx, ctx.bot.user)
        # I AM PROFESSOR COPY PASTE
        self.aiConditional = lambda i_curPlayer, i_val, bestValue: \
            (abs(inf * i_curPlayer - i_val)) < (abs(inf * i_curPlayer - bestValue))

    # noinspection PyTypeChecker
    async def awaitInput(self, player: discord.User, opponent: discord.User):
        if player.id == self.ctx.bot.user.id:
            await self.renderBoard(self.pieces, player.name)
            self.fuckeringers = await self.ctx.send('My turn.')
            await self.aiTurn()
        elif await self.userInput(player):
            await(self.announceWin(opponent, abs(self.currentPlayerID - 1)))
            return True
        await self.fuckeringers.delete()
        return False

    # noinspection PyShadowingNames
    async def aiTurn(self):
        """Use a variant of the MinMax algorithm to make a move."""
        i_curPlayer = fuckers[self.currentPlayerID]
        aaaaaaa = datetime.datetime.now()
        # 3. Run in a custom process pool:
        loop = asyncio.get_running_loop()
        with concurrent.futures.ProcessPoolExecutor() as pool:
            node = await loop.run_in_executor(
                pool, ActiveNode, self.pieces, self.IDtoMark(self.currentPlayerID), fuckers[self.currentPlayerID])
        print(f'Completed in {datetime.datetime.now() - aaaaaaa}')
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

    # noinspection PyUnresolvedReferences
    async def renderBoard(self, board: dict, playerName: str):
        if self.p1.bot:
            mario = 'Me'
            loogi = self.p2.name
        else:
            mario = self.p1.name
            loogi = 'Me'
        self.embed.title = f'TicTacToe: {mario} VS {loogi}'
        if playerName:
            self.embed.set_author(name=f'{playerName}\'s turn. ({self.IDtoMark(self.currentPlayerID)})')
        else:
            self.embed.remove_author()

        self.gfx.syncData(dictToScanLines(board))
        self.gfx.syncEmbed(self.embed)
        await self.gfx.blit()
