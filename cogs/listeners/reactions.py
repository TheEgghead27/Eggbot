import discord
from discord.ext import commands


class Reactions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        # get role configurations
        emoji = str(payload.emoji)
        if emoji == '🗿':
            channel = self.bot.get_channel(payload.channel_id)
            message = await channel.fetch_message(payload.message_id)
            await message.add_reaction('🗿')
        if str(payload.message_id) in self.bot.roles:
            roleData = self.bot.roles[str(payload.message_id)]
            if emoji in roleData:
                roleData = roleData[emoji]
                react_guild = self.bot.get_guild(payload.guild_id)
                react_user = react_guild.get_member(payload.user_id)
                if react_user.id == self.bot.user.id:  # don't let the bot count its own reactions
                    return
                else:
                    role = react_guild.get_role(roleData['role'])
                    try:
                        await react_user.add_roles(role)  # edit role
                        if 'addMessage' in roleData:
                            mess = roleData['addMessage']
                        else:
                            mess = "You now have the @{} role.".format(role.name)
                        emb = discord.Embed(title="Role Confirmed!", description=mess, color=0x0ac845)
                        await react_user.send(embed=emb)
                    except discord.Forbidden:
                        emb = discord.Embed(title="Error: Missing Permissions",
                                            description="I don't have permission to "
                                                        "give you that role! Please "
                                                        "notify a moderator so I can "
                                                        "get the `Manage Roles` "
                                                        "permission!", color=0xbc1a00)
                        await react_user.send(embed=emb)
            else:
                return
        else:
            return

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        # get role configurations
        emoji = str(payload.emoji)
        if str(payload.message_id) in self.bot.roles:
            roleData = self.bot.roles[str(payload.message_id)]
            if emoji in roleData:
                roleData = roleData[emoji]
            else:
                return
        else:
            return
        react_guild = self.bot.get_guild(payload.guild_id)
        react_user = react_guild.get_member(payload.user_id)
        if react_user.id == self.bot.user.id:  # don't let the bot count its own reactions
            return
        else:
            role = react_guild.get_role(roleData['role'])
            try:
                await react_user.remove_roles(role)  # edit role
                if 'removeMessage' in roleData:
                    mess = roleData['removeMessage']
                else:
                    mess = "You no longer have the @{} role.".format(role.name)
                emb = discord.Embed(title="Role removed :(", description=mess, color=0xbc1a00)
                await react_user.send(embed=emb)
            except discord.Forbidden:
                emb = discord.Embed(title="Error: Missing Permissions",
                                    description="I don't have permission to give you "
                                                "that role! Please notify a moderator "
                                                "so I can get the `Manage Roles` "
                                                "permission!", color=0xbc1a00)
                await react_user.send(embed=emb)


def setup(bot):
    bot.add_cog(Reactions(bot))
