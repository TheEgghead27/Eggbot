from asyncio import ensure_future, sleep
from random import randrange

import discord
from discord.ext import commands

from eggbot import kirilist, beeEmbed, host_check, Bee, insults, owner_check
from cogs.listeners.pagination import Pagination
from cogs.commands.gamiing.ttdAI import discordTicTacAI as Calm4
from cogs.commands.gamiing.ttd2 import discordTicTac as dTTv2
from cogs.commands.gamiing.life import life


class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.pagination = Pagination(self.bot)
        self.live = None

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
        game = Calm4(ctx, ctx.bot.user)
        await game.run()
        self.tttB = game

    # Code partially used from https://gist.github.com/nitros12/2c3c265813121492655bc95aa54da6b9
    # Code 100% yoinked from CatLamp
    @commands.command(name="evalTTT", hidden=True, brief='{code (use newlines for multi-line code)}')
    @commands.check(owner_check)
    async def evaluate(self, ctx, *, code):
        """Executes the specified code (command stolen from CatLamp)"""
        import ast

        def insert_returns(body):
            # insert return stmt if the last expression is a expression statement
            if isinstance(body[-1], ast.Expr):
                body[-1] = ast.Return(body[-1].value)
                ast.fix_missing_locations(body[-1])
        try:
            fn_name = "_eval_expr"

            code = code.strip("` ")
            if code.startswith("py"):
                code = code[2:]

            # add a layer of indentation
            code = "\n".join(f"    {i}" for i in code.splitlines())

            # wrap in async def body
            body = f"async def {fn_name}():\n{code}"

            parsed = ast.parse(body)
            body = parsed.body[0].body

            insert_returns(body)
            from eggbot import hosts, token, Bee, kirilist, eggs, eggTrigger, spic, simp, ohno, colors, \
                insults, beeEmbed, logging, dmLog, audit, deleteLog, times, activityTypes, \
                flagFields, mmyes, scores

            env = {
                'client': self.bot,
                'bot': self.bot,
                'discord': discord,
                'commands': commands,
                'ctx': ctx,
                'hosts': hosts,
                'game': self.tttB,
            }
            exec(compile(parsed, filename="<ast>", mode="exec"), env)
            result = (await eval(f"{fn_name}()", env))
            if len(str(result)) > 2048:
                embed = discord.Embed(title="Result too long",
                                      description=f"The result was too long, so it was printed in terminal.",
                                      color=0x00ff00)
                embed.set_footer(text="Executed successfully.")
                await ctx.send(embed=embed)
            else:
                embed = discord.Embed(description=f"```python\n{str(result)}\n```", color=0x00ff00)
                embed.set_footer(text="Executed successfully.")
                await ctx.send(embed=embed)
        except Exception as exception:
            if len(str(exception)) > 2048:  # I doubt this is needed, but just in case
                embed = discord.Embed(title="Error too long",
                                      description=f"The error was too long, so it was printed in terminal",
                                      color=0xff0000)
                embed.set_footer(text="Error occurred while executing.")
                await ctx.send(embed=embed)
            else:
                embed = discord.Embed(description=f"```python\n{str(exception)}\n```", color=0xff0000)
                embed.set_footer(text="Error occurred while executing.")
                await ctx.send(embed=embed)

    @commands.command(aliases=['ttt', "tic_tac_toe"], brief='{@user}')
    async def ticTacToe(self, ctx, victim: discord.Member):
        """Starts a game of tic-tac-toe against the mentioned user."""
        if not victim.bot:
            if victim.id != ctx.author.id:
                if victim.permissions_in(ctx.channel).read_messages:
                    game = dTTv2(ctx, victim)
                    await game.run()
                else:
                    await ctx.send('hey if you cant see the game, is it even fair?')
            else:
                await ctx.send('you cant play tictactoe against yourself lol')
        else:
            await ctx.send('mention a *human* to play dumb')

    @commands.command(hidden=True)
    @commands.check(host_check)
    async def life(self, ctx, *args):
        """life"""
        if self.live:
            await ctx.send('Life is running somewhere else...')
            return
        width, height, born, survive = self.processLifeArgs(args)
        if width * height <= 169:
            if width <= 25:
                live = life(ctx, [width, height], born=born, survive=survive)
                self.live = ensure_future(live.run(owner=self))
            else:
                await ctx.send('Sorry, the maximum width is 25.')
        else:
            await ctx.send('Sorry, the maximum cell count is 13^2.')

    # noinspection PyMethodMayBeStatic
    def processLifeArgs(self, args: tuple):
        width = 0
        height = 0
        born = []
        survive = []
        for i in args:
            try:
                tempInt = int(i)
                if not width:
                    width = tempInt
                elif not height:
                    height = tempInt
            except ValueError:
                if i.lower()[0] == 'b':  # born argument
                    for character in list(i[1:]):
                        try:
                            born.append(int(character))
                        except ValueError:
                            pass
                elif i.lower()[0] == 's':  # survive argument
                    for character in list(i[1:]):
                        try:
                            survive.append(int(character))
                        except ValueError:
                            pass
        if not width:
            width = 10
        if not height:
            height = 10
        return width, height, born, survive

    @commands.command(hidden=True, aliases=['endLife', 'cancelLife', '2020'])
    @commands.check(owner_check)
    async def fuckLife(self, ctx):
        try:
            self.live.cancel()
            await ctx.send('pulled a 2020 on life 😎')
        except AttributeError:
            await ctx.send('i have no life 😔')

    @commands.command(hidden=True)
    @commands.check(host_check)
    async def techDemo(self, ctx):
        """Thing to gauge the embed edit rate-limits"""
        embed = discord.Embed(title=f'Starting {ctx.author}\' game of Life...',
                              description="⬛⬛⬛\n⬛⬛⬛\n⬛⬛⬛",
                              color=0x00ff00)

        embed.title = f"{ctx.author}\'s game of Life..."
        mess = await ctx.send(embed=embed)
        fuck = True
        a = 0
        while fuck:
            embed.description = str(a)
            a += 1
            await mess.edit(embed=embed)


def setup(bot):
    bot.add_cog(Fun(bot))
