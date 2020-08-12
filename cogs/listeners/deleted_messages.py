from discord.ext import commands

from eggbot import deleteLog


class DeletedMess(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_raw_message_delete(self, payload):
        """Deleted message logging"""
        if deleteLog is True:
            print('In the channel with ID {p.channel_id}, a message with ID {p.message_id} was deleted.'.format(
                p=payload))
            if payload.cached_message:
                message = payload.cached_message
                if len(message.content) > 0:
                    content = "\n" + message.content
                else:
                    content = message.content
                print(str('{a} said:'.format(a=str(message.author)) + content))
                if len(message.attachments) > 0:
                    print("Attachments: {}".format(str(message.attachments)))
            else:
                print('The message could not be retrieved.')


def setup(bot):
    bot.add_cog(DeletedMess(bot))
