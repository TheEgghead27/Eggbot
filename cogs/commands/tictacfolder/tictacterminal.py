import asyncio

import discord
import random
import re

from discord.ext import commands


class ticTacToe:
    def __init__(self):
        self.pieces = {
            'a1': None, 'a2': None, 'a3': None, 'b1': None, 'b2': None, 'b3': None, "c1": None, "c2": None, "c3": None
        }

        p1Temp = random.randrange(0, 2)
        self.players = {
            '1': p1Temp,
            '2': -p1Temp + 1
        }
        del p1Temp

        self.player = None
        self.currentPlayerID = None

    # noinspection PyMethodMayBeStatic
    def IDtoMark(self, num: int):
        if num == 0:
            return 'O'
        else:
            return 'X'

    def announceWin(self, winner):
        print(f'Player {self.player} ({self.IDtoMark(winner)}) wins!')

    # noinspection PyTypeChecker
    def awaitP1Input(self):
        print(f'Player {self.player}\'s turn. ({self.IDtoMark(self.currentPlayerID)})')
        self.userInput()

    awaitP2Input = awaitP1Input  # replace this with AI shenanigans in min-max edition

    def userInput(self):
        waiting = True
        while waiting:
            Input = input().lower()
            waiting = self.processInput(Input)

    def processInput(self, Input):
        if Input not in self.pieces:
            print('Invalid input, you can only have A-C and 1-3 as inputs!')
        elif self.pieces[Input] is not None:
            print('That space is occupied!')
        else:
            # noinspection PyTypeChecker
            self.pieces[Input] = self.IDtoMark(self.currentPlayerID)
            return False
        return True

    def renderBoard(self, board: dict):
        icons = []
        for i in board.values():
            if i is not None:
                icons.append(f' {i} ')
            else:
                icons.append('   ')
        print(f"{icons[0]}|{icons[1]}|{icons[2]}\n-----------\n{icons[3]}|{icons[4]}|{icons[5]}\n-----------\n"
              f"{icons[6]}|{icons[7]}|{icons[8]}")

    # noinspection PyMethodMayBeStatic
    def winCheck(self, board: dict):
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
                return '1'
        for i in OList:
            for _ in re.findall(i, data):
                return '0'

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
                return '1'
            elif data == 'OOO':
                return '1'

    # noinspection PyAttributeOutsideInit
    def run(self):
        for i in range(9):
            self.currentPlayerID = i % 2

            for self.player in self.players:  # figure out which player to use
                if self.players[self.player] == self.currentPlayerID:
                    break

            if self.player == '1':
                self.awaitP1Input()
            else:
                self.awaitP2Input()
            self.renderBoard(self.pieces)
            if self.winCheck(self.pieces):
                winner = int(self.winCheck(self.pieces))
                self.announceWin(winner)
                return
        print('Draw.')


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


class DiscordPlayer:
    """Data-class for a player in a discordTicTac game."""
    def __init__(self, user: discord.User, ID: int, mark: str):
        self.user = user
        self.id = ID
        self.mark = mark


# noinspection PyAttributeOutsideInit,PyPropertyAccess,PyMethodOverriding
class discordTicTac(ticTacToe):
    def __init__(self, ctx: commands.Context, p2: discord.user):
        super(discordTicTac, self).__init__()
        self.ctx = ctx
        self.p1 = DiscordPlayer(ctx.author, 1, 'X')
        self.p2 = DiscordPlayer(p2, 2, 'O')

    async def run(self):
        embed = discord.Embed(title=f'Starting {self.ctx.author}\' game of TicTacToe...', color=0x00ff00)
        embed.description = f"⬛⬛⬛\n⬛⬛⬛\n⬛⬛⬛"

        self.confirmMess = await self.ctx.send(embed=embed)
        for i in ['⬆', '⬇', '⬅', '➡', '✅']:
            await self.confirmMess.add_reaction(i)

        for i in range(9):
            self.currentPlayerID = i % 2

            for self.player in self.players:  # figure out which player to use
                if self.players[self.player] == self.currentPlayerID:
                    break

            if self.player == '1':
                curPlayer = self.p1
                if await self.awaitP1Input():
                    await self.cleanBoard()
                    return
            else:
                curPlayer = self.p2
                if await self.awaitP2Input():
                    await self.cleanBoard()
                    return

            if self.winCheck(self.pieces):
                await self.cleanBoard()
                await self.announceWin(curPlayer)
                return
        await self.cleanBoard()
        await self.ctx.send('wow a tie amazing')

    # noinspection PyTypeChecker
    async def awaitP1Input(self):
        if await self.userInput(self.p1):
            await(self.announceWin(self.p1))
            return True
        return False

    # noinspection PyTypeChecker
    async def awaitP2Input(self):
        if await self.userInput(self.p2):
            await(self.announceWin(self.p1))
            return True
        return False

    def renderBoard(self, board: dict, playerName: str):
        embed = discord.Embed(title=f'TicTacToe: {self.ctx.author} VS {self.p2.user}', color=0x00ff00)
        if playerName:
            embed.set_author(name=f'{playerName}\'s turn. ({self.IDtoMark(self.currentPlayerID)})')

        pieceEmojiIndex = {'None': '⬛', 'X': '❌', 'O': '⭕',
                           'oS': '<:oS:757696246755622923>', 'xS': '<:xS:757697702216597604>',
                           'noneS': '<:noneS:757697725906026547>'}
        icons = []
        for i in board.values():
            icons.append(pieceEmojiIndex[str(i)])
        embed.description = f"{icons[0]}{icons[1]}{icons[2]}\n{icons[3]}{icons[4]}{icons[5]}\n" \
                            f"{icons[6]}{icons[7]}{icons[8]}"
        return embed

    async def userInput(self, p):
        waiting = True
        selection, temp = selectInit(self.pieces)
        await self.confirmMess.edit(embed=self.renderBoard(temp, p.user.name))
        while waiting:
            # wait_for stolen from docs example
            def confirm(react, reactor):
                return reactor == p.user and str(react.emoji) in ('⬆', '⬇', '⬅', '➡', '✅') \
                       and self.confirmMess.id == react.message.id

            try:
                reaction, user = await self.ctx.bot.wait_for('reaction_add', timeout=90, check=confirm)
            except asyncio.TimeoutError:  # timeout cancel
                await self.ctx.send(f'{p.user.mention}\'s game timed-out. Be quicker bro!!!')
                return p.user
            else:
                if reaction.emoji == '✅':
                    waitingTemp = await self.processInput(selection)
                    asyncio.ensure_future(self.removeReactions(['⬆', '⬇', '⬅', '➡', '✅'], user))
                    waiting = waitingTemp

                else:
                    selection, temp = directionShuffle[reaction.emoji](selection, self.pieces)
                    await self.confirmMess.edit(embed=self.renderBoard(temp, p.user.name))
                    asyncio.ensure_future(self.removeReactions([reaction.emoji, '✅'], user))

    async def removeReactions(self, emojis: list, user: discord.User):
        """I made this a function for *blast-processing* and also efficiency"""
        for i in emojis:
            try:
                await self.confirmMess.remove_reaction(i, user)
            except (discord.Forbidden, discord.NotFound):
                pass

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

    async def announceWin(self, winner: DiscordPlayer):
        await self.ctx.send(f'Player {winner.user.mention} ({winner.mark}) wins!')

    async def cleanBoard(self):
        asyncio.ensure_future(self.removeReactions(['⬆', '⬇', '⬅', '➡', '✅'], self.ctx.bot.user))
        await self.confirmMess.edit(embed=self.renderBoard(self.pieces, ''))


if __name__ == '__main__':
    game = ticTacToe()
    game.run()
