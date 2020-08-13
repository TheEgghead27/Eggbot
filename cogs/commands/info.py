from asyncio import sleep

import discord
from discord.ext import commands

from eggbot import hosts, host_check, eggC


class Info(commands.Cog, name="Bot Info"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="help")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def documentation(self, ctx):
        kiriPerson = self.bot.get_user(255070100325924864)
        owner = self.bot.get_user(int(hosts[0]))
        emb = discord.Embed(title="Eggbot Commands", description="The commands in this bot", color=0x1888f0)
        emb.add_field(name="e!help", value="Displays this manual", inline=False)
        emb.add_field(name="e!economyHelp", value="Displays the economy manual", inline=False)
        emb.add_field(name="e!kiri [number]",
                      value="Displays an image of Eijiro Kirishima from My Hero Academia. You can "
                            "specify the number of images you want to be sent. "
                            "[request from {user}]".format(user=kiriPerson), inline=False)
        emb.add_field(name="e!test_args [words go here]", value="Test arguments", inline=False)
        emb.add_field(name="e!about [blank for self, mention a user/type the user id to target the specified user]",
                      value="Reveals basically everything (legal) I can get on you", inline=False)
        emb.add_field(name="e!github", value="Links to Eggbot's repo", inline=False)
        emb.add_field(name="e!invite", value="Links to an invite link for Eggbot.", inline=False)
        emb.add_field(name="e!server", value="DMs you an invite to the Eggbot Discord Server.", inline=False)
        emb.add_field(name="e!joinRole [@role]", value="Sets a role that is automatically given to new users "
                                                       "(when the bot is online).", inline=False)
        emb.add_field(name="e!vacuum [number]", value="Mass deletes [number] messages.", inline=False)
        # good lord I fucked up the timer syntax badly
        emb.add_field(name="e!timer \"name\" (quotes mandatory) [time format] (and if you want more units of time) and "
                           "[time format]",
                      value="Creates a timer that pings the requesting user after a specified time.",
                      inline=False)
        emb.add_field(name="e!rateFood", value="Rates food. [beware foul language]", inline=False)
        emb.add_field(name="e!get_icon", value="Links to a copy of the server icon.", inline=False)
        emb.add_field(name="e!admins", value="Lists the admins for this copy of Eggbot.", inline=False)
        emb.add_field(name="e!settings", value="Displays the logging configuration for the current instance of Eggbot.",
                      inline=False)
        emb.add_field(name="egg", value="egg", inline=False)
        emb.add_field(name="e!eggCount", value="[depreciated] ||Counts the day's eggs!||", inline=False)
        emb.add_field(name="simp", value="SIMP", inline=False)
        emb.add_field(name="moyai", value="🗿", inline=False)
        emb.add_field(name="Privacy Policy", value="The privacy policy for Eggbot can be found [here]"
                                                   "(https://github.com/TheEgghead27/Eggbot/blob/master/PRIVACY.md)",
                      inline=False)
        emb.set_footer(text="This instance of Eggbot is hosted by {owner}.".format(owner=owner))
        await ctx.send(embed=emb)

    @documentation.error
    async def help_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send("bro this is all I have, no need to spam me for more")
            return
        else:
            raise error

    @commands.command()
    async def github(self, ctx):
        emb = discord.Embed(title="Github Repo", description="https://github.com/TheEgghead27/Eggbot",
                            color=0x26a343)
        await ctx.send(embed=emb)

    @commands.command()
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def invite(self, ctx):
        emb = discord.Embed(title="Bot Invite",
                            description="https://discordapp.com/api/oauth2/authorize?client_id=681295724188794890&"
                                        "permissions=271969345&scope=bot", color=0xffffff)
        await ctx.send(embed=emb)

    @invite.error
    async def invite_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send("Bruh, you don't need that many bot invites. Ask again later.")
        else:
            raise error

    @commands.command()
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def server(self, ctx):
        egg_guild = self.bot.get_guild(675750662058934324)
        if ctx.guild != egg_guild:
            emb = discord.Embed(title="Official Eggbot Discord Server", description="https://discord.gg/rTfkdvX",
                                color=0x000000)
            await ctx.message.author.send(embed=emb)
            await ctx.send("Sent server invite to your DMs!")
        else:
            await ctx.send("You're already in the Eggbot Server!")

    @server.error
    async def server_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send("Bro, you don't need that many invite links. Ask again later.")
        else:
            raise error

    @commands.command()
    async def eggCount(self, ctx):
        if host_check(ctx):
            emb = discord.Embed(title="Number of times you people used egg since last reboot:", color=0xffffff)
            emb.add_field(name="Egg count:", value=str(eggC), inline=False)
            await ctx.send(embed=emb)
        else:
            await ctx.send("This command has been disabled.")

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
    async def admins(self, ctx):
        c = len(hosts)
        d = 0
        e = 0
        emb = discord.Embed(title='Admins for this Eggbot:')
        while c > 0:
            try:
                user = self.bot.get_user(int(hosts[d]))
                if str(user) != 'None':
                    if e == 0:
                        emb.add_field(name="Owner", value=str(user), inline=False)
                    else:
                        emb.add_field(name="Admin {}".format(str(e)), value=str(user), inline=False)
                    e += 1
                else:
                    await wrongAdmins(ctx, hosts[d])
            except ValueError:
                await wrongAdmins(ctx, hosts[d])
            d += 1
            c -= 1
        await ctx.send(embed=emb)


def setup(bot):
    bot.add_cog(Info(bot))


async def wrongAdmins(ctx, wrongAdmin):
    await ctx.send('There is an unsolved reference in the hosts list, {}.'.format(wrongAdmin))
    await sleep(0.75)
