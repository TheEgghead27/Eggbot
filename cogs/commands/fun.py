from asyncio import sleep
from random import randrange

import discord
from discord.ext import commands

from eggbot import kirilist, beeEmbed, host_check, Bee, insults
from cogs.listeners.pagination import Pagination
from cogs.commands.tictacfolder.tictacterminal import discordTicTac


class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.pagination = Pagination(self.bot)

    @commands.command(brief="{optional: page number}")
    @commands.cooldown(1, 7.5, commands.BucketType.user)
    async def bee(self, ctx):
        """Displays The Bee Movie's script, now with 99% less spam!"""
        args = ctx.message.content.split(' ')
        try:
            page = int(args[1]) - 1
            if 0 <= page < len(beeEmbed):
                emb = discord.Embed.from_dict(beeEmbed[page])
                beeMess = await ctx.send(embed=emb)
                await self.pagination.paginate(beeMess, 'bee', page, 1200)
            else:
                raise ValueError
        except (ValueError, IndexError):
            emb = discord.Embed.from_dict(beeEmbed[0])
            beeMess = await ctx.send(embed=emb)
            await self.pagination.paginate(beeMess, 'bee', 0, 1200)

    @commands.command(hidden=True)
    @commands.check(host_check)
    async def beeGen(self, ctx):
        """Generates and prints a new set of e!bee embeds based on bee.txt"""
        beeTime = False
        script = list(Bee)
        beeLen = len(script) // 2  # know how many sets of text (name & dialogue) there are
        limitCheck = 25
        messNo = 1
        color_list = [0xffff00, 0x000000]
        bs = []
        emb = discord.Embed(title="The Bee Movie Script", color=color_list[0])
        for _ in range(beeLen):  # why did i do this?!?!
            if limitCheck == 25:  # make sure the embed limits don't cut off the dialogue
                limitCheck = 0
                if beeTime:  # don't send an empty embed
                    bs.append(emb.to_dict())
                    # await ctx.send(embed=emb)
                emb = discord.Embed(title="The Bee Movie Script", color=color_list[0])
                emb.set_footer(text="Page {n}/56 | Adapted from scripts.com".format(n=str(messNo)))
                # alternate colors
                color_list.append(color_list[0])
                del color_list[0]
                messNo = messNo + 1  # keep the message numbers rising
                async with ctx.typing():
                    beeTime = True
                    await sleep(1)
            emb.add_field(name=script[0], value=script[1], inline=False)  # add the name and dialogue
            del script[0], script[0]  # delete the used dialogue (replace with increment read number, coz i wanna)
            limitCheck = limitCheck + 1
        bs.append(emb.to_dict())
        await ctx.send("Done, check terminal!")
        print(bs)

    @commands.command(hidden=True, brief="{optional: number of embeds}")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def kiri(self, ctx, *args):
        """Displays an image of Eijiro Kirishima from My Hero Academia. You can specify the number of images you want
        to be sent. [request from Karkat's Stolen Identity#0909]"""
        try:
            send_amount = args[0]
            send_amount = int(send_amount)
            if send_amount > 5:
                await ctx.send("wowowoah, you gotta chill, we don't need spam on our hands! "
                               "We've limited you to 5 images.")
                send_amount = 5
            while send_amount > 0:
                await self.kiriContent(ctx)
                await sleep(1)
                send_amount = send_amount - 1
        except (ValueError, IndexError):
            await self.kiriContent(ctx)

    @kiri.error
    async def kiri_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send("I get that you're excited about the anime guy, but chill, k?")
        else:
            raise error

    async def kiriContent(self, ctx):
        kiriPerson = self.bot.get_user(255070100325924864)
        emb = discord.Embed(title="Here's a picture of Eijiro Kirishima, our beloved Red Riot~", color=0xc60004)
        emb.set_image(url=kirilist[randrange(0, len(kirilist))])  # randomly uploads an image from the list
        emb.set_footer(text=f"This command, and its related images were requested and sourced from {kiriPerson}")
        await ctx.send(embed=emb)

    @commands.command(hidden=True)
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def song(self, ctx):
        """The screams of the damned"""
        micheal = await ctx.message.author.voice.channel.connect(timeout=60.0, reconnect=True)
        await sleep(5)
        await micheal.disconnect()

    @song.error
    async def song_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send("The damned have a limited amount of bandwidth. Ask again later.")
        elif isinstance(error, commands.CommandInvokeError):
            await ctx.send("The damned get only one vessel per server. Try again when this one expires.")
        else:
            raise error

    @commands.command()
    async def rateFood(self, ctx):
        """Rates your food like a certain angry chef"""
        await ctx.send(insults[randrange(0, len(insults) - 1)])

    @commands.command(hidden=True)
    async def pp(self, ctx):
        """pp"""
        if ctx.message.channel.is_nsfw():
            try:
                await ctx.send(content="Here's the good stuff.", file=discord.File(filename="pp.png", fp="pp.png"))
            except FileNotFoundError:
                await ctx.send("Oops! pp not found! It's probably too small! xD")
        else:
            await ctx.send("This content is NSFW, ya dingus!")

    @commands.command(hidden=True, aliases=['tttB', "tic_tac_toe_beta"])
    @commands.check(host_check)
    async def tictactoeBeta(self, ctx):
        """Beta tic tac toe thing"""
        if ctx.message.mentions:
            victim = ctx.message.mentions[0]
            if not victim.bot:
                if victim.id != ctx.author.id:
                    game = discordTicTac(ctx, ctx.message.mentions[0])
                    await game.run()
                else:
                    await ctx.send('damn youre lonely, but dont worry, '
                                   'im gonna learn how to play the game for you soon™')
            else:
                await ctx.send('mention a *human* to play dumb')
        else:
            await ctx.send('mention a human to play dumb')

    @commands.command(aliases=['ttt', "tic_tac_toe"], brief='{@user}')
    async def ticTacToe(self, ctx):
        """Starts a game of tic-tac-toe against the mentioned user."""
        if ctx.message.mentions:
            victim = ctx.message.mentions[0]
            if not victim.bot:
                if victim.id != ctx.author.id:
                    game = discordTicTac(ctx, ctx.message.mentions[0])
                    await game.run()
                else:
                    await ctx.send('damn youre lonely, but dont worry, im gonna learn how to play the game for you')
            else:
                await ctx.send('mention a *human* to play dumb')
        else:
            await ctx.send('mention a human to play dumb')


def setup(bot):
    bot.add_cog(Fun(bot))
