import asyncio
import discord


async def confirm(ctx, prompt: str, cancelMess: str):
    confirmMess = await ctx.send(prompt)
    await confirmMess.add_reaction('✅')
    await confirmMess.add_reaction('❌')

    # wait_for stolen from docs example
    def check(react, reactor):
        return reactor == ctx.author and str(react.emoji) in ('✅', '❌') and confirmMess.id == react.message.id

    try:
        reaction, user = await ctx.bot.wait_for('reaction_add', timeout=30, check=check)
    except asyncio.TimeoutError:  # timeout cancel
        await confirmMess.edit(text=cancelMess)
    else:
        if reaction.emoji == '✅':
            await confirmMess.delete()
            return True

        else:  # ❌ react cancel
            await confirmMess.remove_reaction('✅', ctx.bot.user)
            await confirmMess.remove_reaction('❌', ctx.bot.user)
        try:
            await confirmMess.remove_reaction('❌', user)
        except (discord.Forbidden, discord.NotFound):
            pass
        await confirmMess.edit(content=cancelMess)
