from discord.ext import commands
import discord
from startup import getOwners

owners = getOwners()


class EmbedHelpCommand(commands.HelpCommand):
    """This is an example of a HelpCommand that utilizes embeds.
    It's pretty basic but it lacks some nuances that people might expect.
    1. It breaks if you have more than 25 cogs or more than 25 subcommands. (Most people don't reach this)
    2. It doesn't DM users. To do this, you have to override `get_destination`. It's simple.
    Other than those two things this is a basic skeleton to get you started. It should
    be simple to modify if you desire some other behaviour.

    To use this, pass it to the bot constructor e.g.:

    bot = commands.Bot(help_command=EmbedHelpCommand())
    """
    # Set the embed colour here
    COLOUR = discord.Colour.from_rgb(24, 136, 240)

    def get_ending_note(self, main):
        if main and str(self.context.channel.type) == "text":
            memberIDs = []
            for i in self.context.guild.members:
                memberIDs.append(i.id)
            if 472714545723342848 in tuple(memberIDs):
                return "Use e!help [command] for more info on a command. || This help command's format was stolen " \
                       "from Ear Tensifier".format(self.clean_prefix.lower().strip(" "))
        return 'Use e!help [command] for more info on a command.'.format(self.clean_prefix.lower().strip(" "))

    def get_command_signature(self, command):
        return '{0.qualified_name} {0.signature}'.format(command)

    async def send_bot_help(self, mapping):
        embed = discord.Embed(title='Bot Commands', colour=self.COLOUR)
        for cog, Commands in mapping.items():
            name = 'Misc.' if cog is None else cog.qualified_name
            filtered = await self.filter_commands(Commands, sort=True)
            if filtered:
                try:
                    if self.context.author.id in owners:
                        def commandCheck(CheckCommand):
                            return CheckCommand
                    else:
                        def commandCheck(CheckCommand):
                            return not CheckCommand.hidden
                except TypeError:
                    def commandCheck(CheckCommand):
                        return not CheckCommand.hidden
                # stealing this formatting from Ear Tensifier because
                new = []
                for c in Commands:
                    if commandCheck(c):
                        new.append(c.name)
                new.sort()
                Commands = new
                del new
                value = ''
                if name == "Bot Info":
                    value += f'`help`, '
                for c in Commands:
                    if c != "help":
                        value += f'`{c}`, '
                value = value.rstrip(", ")
                if cog and cog.description:
                    value = '{0}\n{1}'.format(cog.description, value)
                if value:
                    embed.add_field(name=name, value=value, inline=False)

        embed.set_footer(text=self.get_ending_note(main=True))
        await self.get_destination().send(embed=embed)

    async def send_command_help(self, Command):
        if Command.brief is None:
            syntax = ""
        else:
            syntax = Command.brief
        embed = discord.Embed(title=f'e!{Command.qualified_name} {syntax}', colour=self.COLOUR)
        if Command.qualified_name == 'help':
            embed.description = "Displays the documentation for Eggbot."
        elif Command.help:
            embed.description = Command.help
        if Command.aliases:
            value = ''
            for a in Command.aliases:
                if a != "help":
                    value += f'`{a}`, '
            value = value.rstrip(", ")
            embed.add_field(name='Aliases', value=value)

        embed.set_footer(text=self.get_ending_note(main=False))
        await self.get_destination().send(embed=embed)

    async def command_not_found(self, string):
        return "Invalid command. Check `e!help` for a list of valid commands."
