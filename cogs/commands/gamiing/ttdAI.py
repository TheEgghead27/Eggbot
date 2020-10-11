import datetime

import asyncio
from asyncio.exceptions import TimeoutError
# import discord (DiscordX already has discord)
from discord.ext import commands
import random
import threading

from cogs.commands.gamiing.DInput import DInput
from cogs.commands.gamiing.DiscordX import *
from cogs.commands.gamiing.tictacterminal import ticTacToe
from cogs.commands.gamiing.minmax import inf, Node, MinMax


def selectInit(pieces: dict):
    new = 'a1'
    piecesNew = pieces.copy()
    piecesNew[new] = str(piecesNew[new]).lower() + 'S'
    return new, piecesNew


def up(old: str, pieces: dict):
    table = {
        'a': 'c', 'b': 'a', 'c': 'b'
    }
    new = table[old[0]] + old[1]
    piecesNew = pieces.copy()
    piecesNew[new] = str(piecesNew[new]).lower() + 'S'
    return new, piecesNew


def down(old: str, pieces: dict):
    table = {
        'a': 'b', 'b': 'c', 'c': 'a'
    }
    new = table[old[0]] + old[1]
    piecesNew = pieces.copy()
    piecesNew[new] = str(piecesNew[new]).lower() + 'S'
    return new, piecesNew


def left(old: str, pieces: dict):
    table = {
        '1': '3', '2': '1', '3': '2'
    }
    new = old[0] + table[old[1]]
    piecesNew = pieces.copy()
    piecesNew[new] = str(piecesNew[new]).lower() + 'S'
    return new, piecesNew


def right(old: str, pieces: dict):
    table = {
        '1': '2', '2': '3', '3': '1'
    }
    new = old[0] + table[old[1]]
    piecesNew = pieces.copy()
    piecesNew[new] = str(piecesNew[new]).lower() + 'S'
    return new, piecesNew


directionShuffle = {
    '⬆': up, '⬇': down, '⬅': left, '➡': right
}


# noinspection PyAttributeOutsideInit,PyPropertyAccess,PyMethodOverriding
class discordTicTac(ticTacToe):
    def __init__(self, ctx: commands.Context):
        ticTacToe.__init__(self)
        self.ctx = ctx
        self.p1 = ctx.author
        self.p2 = ctx.bot.user

        # randomize player order
        if random.randrange(0, 2):
            self.spicy = True
        else:
            self.spicy = False

    async def run(self):
        self.embed = discord.Embed(title=f'Starting {self.ctx.author}\' game of TicTacToe...',
                                   description=f"⬛⬛⬛\n⬛⬛⬛\n⬛⬛⬛", color=0x00ff00)

        self.confirmMess = await self.ctx.send(embed=self.embed)

        self.p1In = DInput(self.ctx.bot, self.confirmMess, self.p1)

        self.gfx = DiscordX(target_message=self.confirmMess, data=dictToScanLines(self.pieces), resolution=[3, 3],
                            embed=self.embed,
                            conversionTable={'None': '⬛', 'X': '❌', 'O': '⭕',
                                             'oS': '<:oS:757696246755622923>', 'xS': '<:xS:757697702216597604>',
                                             'noneS': '<:noneS:757697725906026547>'})

        await self.p1In.initReactions()

        for i in range(9):
            self.currentPlayerID = i % 2
            if self.spicy:
                self.currentPlayerID = abs(self.currentPlayerID - 1)

            for self.player in self.players:  # figure out which player to use
                if self.players[self.player] == self.currentPlayerID:
                    break

            if self.player == '1':
                curPlayer = self.p1
                print('unack')
                if await self.awaitP1Input():
                    await self.cleanBoard()
                    return
            else:
                curPlayer = self.p2
                await self.renderBoard(self.pieces, curPlayer.name)
                await self.awaitP2Input()

            if self.winCheck(self.pieces):
                await self.cleanBoard()
                await self.announceWin(curPlayer, self.currentPlayerID)
                return
        await self.cleanBoard()
        await self.ctx.send('wow a tie amazing')

    # noinspection PyTypeChecker
    async def awaitP1Input(self):
        await self.ctx.send(content=self.p1.mention, delete_after=0.01)
        if await self.userInput(self.p1):
            await(self.announceWin(self.p2, abs(self.currentPlayerID - 1)))
            return True
        return False

    # noinspection PyTypeChecker
    async def awaitP2Input(self):
        startTime = datetime.datetime.now()
        # make curPlayer correspond to positive or negative
        if self.currentPlayerID == 0:
            i_curPlayer = -1
        else:
            i_curPlayer = self.currentPlayerID

        depth = 0
        for i in self.pieces:
            if self.pieces[i] is None:  # if that space is empty
                depth += 1  # queue a depth

        # make some childrens with the current info
        node = Node(depth, i_curPlayer, self.pieces, self.IDtoMark(self.currentPlayerID), self.winCheck)
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
        self.pieces = i_bestNode.board
        print(datetime.datetime.now() - startTime)
        #self.fuckMe(i_bestNode)

    def fuckMe(self, node):
        for i in node.children:
            self.fuckMe(i)
            print(i.board)
        print(node.board)

    async def renderBoard(self, board: dict, playerName: str):
        self.embed.title = f'TicTacToe: {self.p1} VS {self.p2}'
        if playerName:
            self.embed.set_author(name=f'{playerName}\'s turn. ({self.IDtoMark(self.currentPlayerID)})')
        else:
            self.embed.remove_author()

        self.gfx.syncData(dictToScanLines(board))
        self.gfx.syncEmbed(self.embed)
        await self.gfx.blit()

    async def userInput(self, p):
        waiting = True
        selection, temp = selectInit(self.pieces)
        await self.renderBoard(temp, p.name)
        hek = 1
        while waiting:
            print(f'wait ing {hek}')
            thing = await self.p1In.awaitInput()
            if type(thing) == TimeoutError:  # if theres a timeout
                await self.ctx.send(f'{p.mention}\'s game timed-out. Be quicker bro!!!')
                return p
            else:
                if thing == '✅':
                    waitingTemp = await self.processInput(selection)
                    waiting = waitingTemp

                else:
                    selection, temp = directionShuffle[thing](selection, self.pieces)
                    await self.renderBoard(temp, p.name)
            hek += 1

    async def processInput(self, Input):
        if self.pieces[Input] is not None:
            errorEmb = discord.Embed(title='Error: Invalid Selection.',
                                     description="That space is occupied!",
                                     color=0xff0000)
            await self.ctx.send(embed=errorEmb, delete_after=7.5)
        elif Input not in self.pieces:  # this shouldn't happen but fuck you
            errorEmb = discord.Embed(title='Error: Invalid Input.',
                                     description="You can only have A-C and 1-3 as inputs!",
                                     color=0xff0000)
            await self.ctx.send(embed=errorEmb, delete_after=7.5)
        else:
            # noinspection PyTypeChecker
            self.pieces[Input] = self.IDtoMark(self.currentPlayerID)
            return False
        return True

    async def announceWin(self, winner: discord.User, ID: int):
        await self.ctx.send(f'Player {winner.mention} ({self.IDtoMark(ID)}) wins!')

    async def cleanBoard(self):
        asyncio.ensure_future(self.p1In.removeReactions(('⬆', '⬇', '⬅', '➡', '✅'), self.ctx.bot.user))
        await self.renderBoard(self.pieces, '')
