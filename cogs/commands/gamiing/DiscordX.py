import discord
from typing import List


coordinateTypeIThink = List[int]


class DiscordX:
    def __init__(self, target_message: discord.Message, data: list, resolution: coordinateTypeIThink,
                 conversionTable: dict = None, embed: discord.Embed = None):
        if conversionTable is not None:
            self.conversionTable = conversionTable
        else:  # NOTE: 'None' is pretty much required as a placeholder or else I will fucking crucify you
            self.conversionTable = {'1': '⬜', 'None': '⬛'}

        self.mess = target_message
        if embed:
            self.embed = embed
        else:
            try:
                self.embed = self.mess.embeds[0]
            except IndexError:
                print('The "Graphics API" can\'t find an Embed!')
        self.data = data
        self.width = resolution[0]
        self.height = resolution[1]

    def syncData(self, data: list):
        """Synchronizes the class data with the provided information. (For compatibility)"""
        self.data = data

    def syncEmbed(self, data: discord.Embed):
        """Synchronizes the embed with the provided information. (For extra dynamic garbage)"""
        self.embed = data

    async def blit(self):
        interlaced = []
        temp = ''
        counter = 0
        for i in self.data:
            interlaced.append(i)
            if counter == self.width - 1:
                temp += '\n'
                for item in interlaced:
                    try:
                        temp += self.conversionTable[str(item)]
                    except KeyError:
                        try:
                            temp += self.conversionTable['None']
                        except KeyError:
                            temp += self.conversionTable[str(item)]
                interlaced = []
                counter = 0
            else:
                counter += 1
        if interlaced:  # if theres leftovers, just slap it into some extra rows lol
            temp += '\n'
            for item in interlaced:
                try:
                    temp += self.conversionTable[str(item)]
                except KeyError:
                    try:
                        temp += self.conversionTable['None']
                    except KeyError:
                        temp += "⬛"
            for _ in range(0, self.width - len(interlaced)):
                try:
                    temp += self.conversionTable['None']
                except KeyError:
                    temp += "⬛"

        if len(temp.split('\n')) - 1 < self.height:  # if we don't have enough data
            temp += '\n'
            for _ in range(0, self.width):  # fill in blank rows to meet resolution minimum
                try:
                    temp += self.conversionTable['None']
                except KeyError:
                    temp += "⬛"
        self.embed.description = temp
        await self.mess.edit(embed=self.embed)


def dictToScanLines(pieces: dict):
    icons = []
    for i in pieces.values():
        icons.append(i)
    return icons
