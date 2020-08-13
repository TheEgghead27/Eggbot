import simplejson as json

import discord
from discord.ext import commands

from eggbot import host_check, colors, roles, joinRoles

# this guarantees that joinRoles come from the right place (because without this, it's a WTF moment)
roles = roles
joinRoles = joinRoles
roleEmbeds = {}


def load(role):
    global joinRoles, roles
    joinRoles = role["join"]
    roles = role["reactions"]


class Roles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def roleGiver(self, ctx, *args):
        if host_check(ctx):
            global roleEmbeds
            args = list(args)
            try:
                role, emoji, colo = await self.roleProcess(ctx, args)
            except TypeError:
                return
            emb = discord.Embed(title=ctx.guild.name + " Roles", description="Read below for details.", color=colo)
            emb.add_field(name=role.name + " role",
                          value="React with {emote} to get the {role} role.".format(emote=emoji,
                                                                                    role=role.
                                                                                    mention),
                          inline=False)
            emb.add_field(name="Note:",
                          value="You will receive a confirmation DM for your role, as the bot is not always "
                                "online to give out the role", inline=False)
            mess = await ctx.send(embed=emb)
            await mess.add_reaction(emoji)
            roleData = {str(emoji): {"role": role.id}}
            roles[str(mess.id)] = roleData
            with open("roles.json", "w") as j:
                json.dump(roles, j)
            rolls = [role.id]
            emojis = [str(emoji)]
            roleEmbeds[ctx.message.channel] = [emb.to_dict(), mess.id, roleData, rolls, emojis]
            emb = discord.Embed(title="Role giver set up!",
                                description="If you need to add more roles, use `e!addRoles` "
                                            "(same syntax) soon (before the bot is shut off) "
                                            "to add another role.",
                                color=0x0ac845)
            await ctx.author.send(embed=emb)

    @commands.command()
    async def addRole(self, ctx, *args):
        if host_check(ctx):
            args = list(args)
            try:
                info = roleEmbeds[ctx.message.channel]
            except KeyError:
                await ctx.send("Role giver message not found in cache! Are you in the right channel, or did "
                               "the bot reboot?")
                return
            try:
                role, emoji, colo = await self.roleProcess(ctx, args)
            except TypeError:
                return
            if str(emoji) in info:
                await ctx.send("This emoji is already in use!")
                return
            if role.id in info[3]:
                await ctx.send("This role is already available!")
                return
            info[3].append(role.id)
            info[3].append(role.id)
            mess = await ctx.channel.fetch_message(info[1])
            emb = discord.Embed.from_dict(info[0])
            emb.insert_field_at(index=-1, name=role.name + " role", value="React with {emote} to get the {role} role.".
                                format(emote=emoji, role=role.mention), inline=False)
            await mess.edit(embed=emb)
            await mess.add_reaction(emoji)
            info = info[2]
            info[str(emoji)] = {"role": role.id}
            roles[str(mess.id)] = info
            with open("roles.json", "w") as j:
                json.dump(roles, j)

    async def roleProcess(self, ctx, args):
        args = list(args)
        try:
            role = args[0]
            if len(role) == 18:
                role = ctx.guild.get_role(int(role))
            elif len(role) == 22:
                role = ctx.guild.get_role(int(role[-19:-1]))
            else:
                raise ValueError
            del args[0]
        except ValueError:
            await ctx.send("Invalid role was passed.")  # maybe change this
            return
        except IndexError:
            await ctx.send("Role was not given.")  # maybe change this
            return
        if role is None:
            await ctx.send("Invalid role was passed.")  # maybe change this
            return
        try:
            emoji = args[0]
            if len(emoji) == 1:
                pass
            else:
                emoji = self.bot.get_emoji(int(emoji[-19:-1]))
            del args[0]
        except ValueError:
            await ctx.send("Invalid emoji was passed.")  # maybe change this
            return
        except IndexError:
            await ctx.send("Emoji was not given.")  # maybe change this
            return
        if emoji is None:
            await ctx.send("Invalid role was passed.")  # maybe change this
            return
        try:
            if len(args) >= 2:
                colo = args[0] + ' ' + args[1]
            else:
                colo = args[0]
            if colo in colors:
                colo = colors[colo]
            else:
                await ctx.send("Invalid color name was passed.")  # maybe change this
                return
        except IndexError:
            await ctx.send("Invalid color name was passed.")  # maybe change this
            return
        await ctx.message.delete()
        return role, emoji, colo

    @commands.command()
    async def joinRole(self, ctx):
        """Command to set role for new server members"""
        if ctx.guild:
            if ctx.author.guild_permissions.administrator:
                if ctx.message.role_mentions:
                    role = ctx.message.role_mentions[0]
                    joinRoles[str(ctx.guild.id)] = role.id
                    await ctx.send('@{r} was set as the role for new members.'.format(r=role.name))
                else:
                    try:
                        role = int(ctx.message.content.split(' ')[1])
                        if not len(str(role)) == 18:
                            await ctx.send('Role ID machine broken :(')
                            return
                    except (ValueError, IndexError):
                        return
                    await ctx.send('There was no role mentioned?')
            else:
                await ctx.send("You're not an admin, so no.")
        else:
            await ctx.send("This isn't a server! Who's gonna join this? What roles are there to assign? None. "
                           "There is nothing to execute the command on.")

    @commands.Cog.listener()
    async def on_member_join(self, member):
        """Assign role on member joining server, if a role is set."""
        if str(member.guild.id) in joinRoles:
            role = member.guild.get_role(joinRoles[str(member.guild.id)])
            await member.add_roles(role)


def setup(bot):
    bot.add_cog(Roles(bot))
