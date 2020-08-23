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

    def get_ending_note(self):
        memberIDs = []
        for i in self.context.guild.members:
            memberIDs.append(i.id)
        if 472714545723342848 in tuple(memberIDs):
            return "Use e!help [command] for more info on a command. || This help command's format was stolen from " \
                   "Ear Tensifier".format(self.clean_prefix.lower().strip(" "))
        return 'Use e!help [command] for more info on a command.'.format(self.clean_prefix.lower().strip(" "))

    def get_command_signature(self, command):
        return '{0.qualified_name} {0.signature}'.format(command)

    async def send_bot_help(self, mapping):
        embed = discord.Embed(title='Bot Commands', colour=self.COLOUR)
        for cog, Commands in mapping.items():
            name = 'Misc.' if cog is None else cog.qualified_name
            filtered = await self.filter_commands(Commands, sort=True)
            if filtered:
                # stealing this formatting from Ear Tensifier because
                if self.context.author.id in owners:
                    def commandCheck(CheckCommand):
                        return CheckCommand
                else:
                    def commandCheck(CheckCommand):
                        return not CheckCommand.hidden
                new = []
                for c in Commands:
                    # print(c.clean_params)
                    if commandCheck(c):
                        new.append(c.name)
                new.sort()
                Commands = new
                del new
                value = ''
                for c in Commands:
                    value += f'`{c}`, '
                value = value.rstrip(", ")
                if cog and cog.description:
                    value = '{0}\n{1}'.format(cog.description, value)

                embed.add_field(name=name, value=value, inline=False)

        embed.set_footer(text=self.get_ending_note())
        await self.get_destination().send(embed=embed)

    async def send_cog_help(self, cog):
        embed = discord.Embed(title='{0.qualified_name} Commands'.format(cog), colour=self.COLOUR)
        if cog.description:
            embed.description = cog.description

        filtered = await self.filter_commands(cog.get_commands(), sort=True)
        for command in filtered:
            embed.add_field(name=self.get_command_signature(command), value=command.short_doc or '...', inline=False)

        embed.set_footer(text=self.get_ending_note())
        await self.get_destination().send(embed=embed)

    async def send_group_help(self, group):
        embed = discord.Embed(title=group.qualified_name, colour=self.COLOUR)
        if group.help:
            embed.description = group.help

        if isinstance(group, commands.Group):
            filtered = await self.filter_commands(group.commands, sort=True)
            for command in filtered:
                embed.add_field(name=self.get_command_signature(command), value=command.short_doc or '...',
                                inline=False)

        embed.set_footer(text=self.get_ending_note())
        await self.get_destination().send(embed=embed)

    async def send_command_help(self, Command):
        embed = discord.Embed(title='e!' + Command.qualified_name, colour=self.COLOUR)
        if Command.qualified_name == 'help':
            embed.description = "Displays the documentation for Eggbot."
        elif Command.help:
            embed.description = Command.help

        if isinstance(Command, commands.Group):
            filtered = await self.filter_commands(Command.commands, sort=True)
            for command in filtered:
                embed.add_field(name=self.get_command_signature(command), value=command.short_doc or '...',
                                inline=False)

        embed.set_footer(text=self.get_ending_note())
        await self.get_destination().send(embed=embed)

    async def command_not_found(self, string):
        return "Invalid command. Check `e!help` for a list of valid commands."
