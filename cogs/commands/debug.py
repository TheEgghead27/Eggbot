import ast
import datetime

import discord
from discord.ext import commands

from eggbot import host_check, hosts


class Debug(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['latency'])
    async def ping(self, ctx):
        """Displays the latency of the bot (code logic stolen from Ear Tensifier)"""
        msg = await ctx.send('Pinging...')
        emb = discord.Embed(title="Pong!", color=0x000000)
        messLatency = round((msg.created_at.timestamp() - ctx.message.created_at.timestamp()) * 1000, 3)
        emb.add_field(name="Message Latency", value=f"{messLatency} ms")
        emb.add_field(name="API Latency", value=f"{round(self.bot.latency * 1000, 3)} ms")
        await msg.edit(content=None, embed=emb)

    @commands.command(aliases=['TestArgs'], brief='{arguments}')
    async def test_args(self, ctx, *args):
        """Displays how the provided arguments are presented to the bot"""
        arghs = args
        argsleft = len(arghs)
        emb = discord.Embed(title="Arguments", description="Arguments", color=0x0f88f0)
        if argsleft == 0:
            emb.add_field(name="Error", value="No arguments detected", inline=False)
        else:
            argNumber = 0
            while 0 < argsleft:
                argnotext = str(argNumber + 1)
                emb.add_field(name="Argument " + argnotext, value=arghs[argNumber], inline=False)
                argsleft = argsleft - 1
                argNumber = 1 + argNumber
            argnotext = str(len(arghs))
            emb.add_field(name="Total Arguments", value=argnotext, inline=False)
        await ctx.send(embed=emb)

    # Code partially used from https://gist.github.com/nitros12/2c3c265813121492655bc95aa54da6b9
    # Code 100% yoinked from CatLamp
    @commands.command(name="eval", hidden=True, brief='{code (use newlines for multi-line code)}')
    @commands.check(host_check)
    async def evaluate(self, ctx, *, code):
        """Executes the specified code (command stolen from CatLamp)"""
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
            from eggbot import hosts, token, Bee, kirilist, eggs, eggTrigger, spic, simp, ohno, roles, colors, stonks, \
                warehouse, joinRoles, insults, beeEmbed, logging, dmLog, audit, deleteLog, times, activityTypes, \
                flagFields, mmyes, scores

            env = {
                'client': self.bot,
                'bot': self.bot,
                'discord': discord,
                'commands': commands,
                'ctx': ctx,
                'hosts': hosts,
                # 'token': token,
                'Bee': Bee,
                'kirilist': kirilist,
                'eggs': eggs,
                'eggTrigger': eggTrigger,
                'spic': spic,
                'simp': simp,
                'ohno': ohno,
                'roles': roles,
                'colors': colors,
                'stonks': stonks,
                'warehouse': warehouse,
                'joinRoles': joinRoles,
                'insults': insults,
                'beeEmbed': beeEmbed,
                'logging': logging,
                'dmLog': dmLog,
                'audit': audit,
                'deleteLog': deleteLog,
                'times': times,
                'activityTypes': activityTypes,
                'flagFields': flagFields,
                'mmyes': mmyes,
                'scores': scores
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

    @commands.command(aliases=["print", "printEmoji"], hidden=True, brief='{emoji}')
    @commands.check(host_check)
    async def print_emoji(self, ctx, arg1):
        """Prints the first argument"""
        print(arg1)
        await ctx.send('Check the console!')

    @commands.command(hidden=True)
    @commands.check(host_check)
    async def embedTest(self, ctx):
        embed = discord.Embed(title='Go to YouTube', url='https://www.youtube.com/',
                              description='New video guys click on the title or click [here](https://www.youtube.com/)')
        # embed.timestamp = datetime.datetime.today()
        embed.timestamp = datetime.datetime(year=1980, month=1, day=1, hour=5)
        await ctx.send(embed=embed)

    @commands.command(hidden=True)
    @commands.check(host_check)
    async def files(self, ctx):
        """Sends Eggbot's saved data."""
        targets = ['discord.log', 'roles.json', 'stonks.json']
        files = []
        for i in targets:
            files.append(discord.File(filename=i, fp=i))
        await ctx.send(files=files)
        if ctx.author.id == hosts[0]:
            await ctx.author.send(file=discord.File(filename="config.json", fp="config.json"))


def insert_returns(body):
    # insert return stmt if the last expression is a expression statement
    if isinstance(body[-1], ast.Expr):
        body[-1] = ast.Return(body[-1].value)
        ast.fix_missing_locations(body[-1])


def setup(bot):
    bot.add_cog(Debug(bot))
