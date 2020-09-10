import asyncio
import os
import sys

import discord
from discord.ext import commands, tasks

from cogs.misc.save import write
from eggbot import host_check, hosts
from cogs.commands.files import getFiles
from cogs.listeners.pagination import Pagination


class InstanceManagement(commands.Cog, name="Instance Management"):
    def __init__(self, bot):
        self.bot = bot
        self.pagination = Pagination(bot)
        self.sigtermHandler.start()

    @commands.command(hidden=True)
    @commands.check(host_check)
    async def shutdown(self, ctx):
        """Shuts down the bot"""
        if await self.check(ctx, "shut down", "Shutdown"):
            if self.bot.heroku:
                await ctx.send('I might be unable to shut down!')

            await self.papate(ctx, embedColor=0xff0000, phrase="shutting down", timer=True)
            await self.bot.close()
            exit(0)

    @commands.command(name="restart", aliases=["reboot"], hidden=True)
    @commands.check(host_check)
    async def restart(self, ctx):
        """Restarts the bot using the default Python interpreter"""
        if await self.check(ctx, "restart", "Restart"):
            import os
            await self.papate(ctx, embedColor=0xffff00, phrase="restarting", timer=True)
            if not self.bot.heroku:
                # on a local host, execv won't have a visible terminal
                os.startfile("eggbot.py")
                exit(0)
            else:
                # on heroku, it's fine to do this
                os.execv(sys.executable, ['python3'] + sys.argv)

    @commands.command(hidden=True)
    @commands.check(host_check)
    async def reload(self, ctx):
        """Reloads the bot commands and listeners. Only runnable by admins."""
        if await self.check(ctx, "reload", "Reload"):
            await self.papate(ctx, embedColor=0xffff00, phrase="reloading", timer=False)
            self.bot.cmds = []
            # *reload commands and listeners
            cogDirectories = ['cogs/commands/',
                              'cogs/listeners/']  # bot will look for python files in these directories
            for cogDir in cogDirectories:
                loadDir = cogDir.replace('/', '.')
                for cog in os.listdir(cogDir):
                    if cog.endswith('.py'):  # tries to reload all .py files in the folders, use cogs/misc instead
                        try:
                            self.bot.reload_extension(loadDir + cog[:-3])  # from load_extension to reload_extension xD
                        except commands.ExtensionNotLoaded:
                            try:
                                self.bot.load_extension(loadDir + cog[:-3])
                            except commands.NoEntryPointError:
                                print(f"{loadDir + cog[:-3]} is not a proper cog!")
                            except commands.ExtensionAlreadyLoaded:
                                print('you should not be seeing this\n if you do, youre screwed')
                            except commands.ExtensionFailed as failure:
                                print(f'{failure.name} failed! booooo')
                        except commands.ExtensionFailed as failure:
                            print(f'{failure.name} failed! booooo')

            # reload help command
            from cogs.commands.help import EmbedHelpCommand
            self.bot.help_command = EmbedHelpCommand()

            await self.bot.change_presence(activity=discord.Game(self.bot.status))

    @commands.command(name="papate", hidden=True)
    @commands.check(host_check)
    async def silent(self, ctx):
        """\"Silently\" purges the pagination queue and timers."""
        if await self.check(ctx, "purge", "Purge"):
            await self.papate(ctx, embedColor=0x0ff00, phrase="purging", timer=False)
            await self.bot.change_presence(activity=discord.Game(self.bot.status))

    async def papate(self, ctx, embedColor, phrase, timer):
        formatted = phrase[0].upper() + phrase[1:] + '...'
        await self.bot.change_presence(activity=discord.Game(formatted))
        emb = discord.Embed(title=formatted, description="Please wait...",
                            color=embedColor)
        await ctx.send(embed=emb)
        write(self.bot)
        if self.bot.heroku:  # dm the files for safe-keeping
            await self.bot.get_user(hosts[0]).send(files=getFiles(['roles.json', 'stonks.json']))
        # timer purge
        if timer:
            for i in self.bot.timerUsers:
                await i.send(f'The bot is {phrase}. Your timer has been cancelled.')
        # paginated purge
            await self.pagination.flush()
        self.bot.paginated = {}

    async def check(self, ctx, verb: str, noun: str):
        confirmMess = await ctx.send(f'Are you sure you want to {verb} the bot?')
        await confirmMess.add_reaction('✅')
        await confirmMess.add_reaction('❌')

        # wait_for stolen from docs example
        def confirm(react, reactor):
            return reactor == ctx.author and str(react.emoji) in ('✅', '❌') and confirmMess.id == react.message.id

        try:
            reaction, user = await self.bot.wait_for('reaction_add', timeout=30, check=confirm)
        except asyncio.TimeoutError:  # timeout cancel
            await confirmMess.edit(text=f'{noun} cancelled.')
        else:
            if reaction.emoji == '✅':
                await confirmMess.delete()
                return True

            else:  # ❌ react cancel
                await confirmMess.remove_reaction('✅', self.bot.user)
                await confirmMess.remove_reaction('❌', self.bot.user)
            try:
                await confirmMess.remove_reaction('❌', user)
            except (discord.Forbidden, discord.NotFound):
                pass
            await confirmMess.edit(content=f'{noun} cancelled.')

    def cog_unload(self):
        self.sigtermHandler.cancel()

    @tasks.loop(hours=24)
    async def sigtermHandler(self):
        """Dummy task to handle Heroku SIGTERM shutdowns"""
        pass

    @sigtermHandler.after_loop
    async def on_autoSave_cancel(self):
        if self.sigtermHandler.is_being_cancelled() and self.bot.heroku:
            write(self.bot)
            if self.bot.heroku:  # dm the files for safe-keeping
                await self.bot.get_user(hosts[0]).send(content='Restarting...', files=getFiles(['roles.json',
                                                                                                'stonks.json']))
            # timer purge
            for i in self.bot.timerUsers:
                await i.send('The bot is being force-restarted. Your timer has been cancelled.')
            # paginated purge
            await self.pagination.flush()
            self.bot.paginated = {}

    @sigtermHandler.before_loop
    async def before_autoSave(self):
        await self.bot.wait_until_ready()


def setup(bot):
    bot.add_cog(InstanceManagement(bot))
