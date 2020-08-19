import discord
from discord.ext import commands

from eggbot import host_check


class Debug(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        """Stole the basic code off of Ear Tensifier lol"""
        msg = await ctx.send('Pinging...')
        emb = discord.Embed(title="Pong!", color=0x000000)
        messLatency = round((msg.created_at.timestamp() - ctx.message.created_at.timestamp()) * 1000, 3)
        emb.add_field(name="Message Latency", value=f"{messLatency} ms")
        emb.add_field(name="API Latency", value=f"{round(self.bot.latency * 1000, 3)} ms")
        await msg.edit(content=None, embed=emb)

    @commands.command()
    async def test_args(self, ctx, *args):
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

    @commands.command()
    @commands.check(host_check)
    async def print_emoji(self, ctx, *args):
        print(args[0])
        await ctx.send('Check the console!')

    @commands.command()
    @commands.check(host_check)
    async def embedTest(self, ctx):
        embed = discord.Embed(title='Go to YouTube', url='https://www.youtube.com/',
                              description='New video guys click on the title or click [here](https://www.youtube.com/)')
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Debug(bot))
