from random import randint

from discord.ext import commands
from cogs.commands.gamiing.DiscordX import *
import asyncio


class life:
    def __init__(self, ctx: commands.Context, resolution: coordinateTypeIThink):
        self.blocks = []
        self.ctx = ctx
        self.resolution = resolution
        self.width = resolution[0]
        self.height = resolution[1]
        self.pieces = self.generateData()
        self.embed = discord.Embed(title=f'Starting {self.ctx.author}\' game of Life...',
                                   description=self.generateBlankScreen(),
                                   color=0x00ff00)
        self.gfx = None

    def generateBlankScreen(self):
        rowTemplate = '\n'
        for i in range(0, self.width):
            rowTemplate += '⬛'
        rowTemplate *= self.height
        return rowTemplate

    def generateData(self):
        fuck = {}
        for x in range(0, self.width):
            for y in range(0, self.height):
                fuck[(x, y)] = randint(0, 1)
        return fuck

    async def run(self, owner):
        genNumber = 0
        try:
            confirmMess = await self.ctx.send(embed=self.embed)

            self.gfx = DiscordX(target_message=confirmMess, data=dictToScanLines(self.pieces),
                                resolution=self.resolution, embed=self.embed, noWarn=True,
                                conversionTable={'0': '⬛', '1': '⬜', 'None': '⬛'})

            self.embed.title = f"{self.ctx.author}\'s game of Life..."
            self.gfx.syncEmbed(self.embed)

            while True:
                genNumber += 1

                self.gfx.embed.set_footer(text=f'Generation: {genNumber}')

                self.gfx.syncData(dictToScanLines(self.pieces))
                await asyncio.sleep(1)
                await self.gfx.blit()
                if 1 not in self.pieces.values():
                    await self.ctx.send('All cells have died. Ending game...')
                    raise asyncio.CancelledError

                new = self.pieces.copy()
                for i in self.pieces:
                    neighbors = self.getNeighbors(i)

                    # Any live cell with fewer than two live neighbours dies, as if by underpopulation.
                    if neighbors < 2:
                        new[i] = 0

                    # Any live cell with two or three live neighbours survives.
                    # Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.
                    elif neighbors == 3:
                        new[i] = 1
                    # Any live cell with two or three live neighbours lives on to the next generation.
                    elif neighbors in (2, 3) and self.pieces[i] == 1:
                        pass

                    # All other live cells die in the next generation. Similarly, all other dead cells stay dead.
                    else:
                        new[i] = 0

                if self.pieces != new:
                    self.pieces = new
                else:
                    await self.ctx.send('No change between generations detected. Ending game...')
                    raise asyncio.CancelledError

        except asyncio.CancelledError:
            self.gfx.embed.title = f"{self.ctx.author}\'s game of Life"
            # noinspection PyDunderSlots, PyUnresolvedReferences
            self.gfx.embed.color = 0xff0000
            self.gfx.embed.set_footer(text=f'Ended at generation {genNumber}.')
            await self.gfx.blit()
            owner.live = None
            raise

    def getNeighbors(self, target: tuple):
        """Returns the number of neighboring live cells."""
        targetX = target[0]
        targetY = target[1]

        penises = [(targetX - 1, targetY - 1), (targetX, targetY - 1), (targetX + 1, targetY - 1),
                   (targetX - 1, targetY), (targetX + 1, targetY),
                   (targetX - 1, targetY + 1), (targetX, targetY + 1), (targetX + 1, targetY + 1)]

        total = 0
        for i in penises:
            try:
                if self.pieces[i]:
                    total += 1
            except KeyError:
                pass
        return total
