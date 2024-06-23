import discord
from discord.ext import commands


class Exclusive(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Webhook related commands
    @commands.command(name='cw')
    @commands.is_owner()
    async def cw(self, ctx):
        await ctx.message.delete()
        webhook = await ctx.channel.create_webhook(name=f'{ctx.channel.name} Webhook')

        try:
            await ctx.author.send(f'Webhook URL: {webhook.url}')
            await ctx.send('Success', delete_after=5)
        except discord.Forbidden:
            await ctx.send('An error occurred')

    @commands.command(name='dw')
    @commands.is_owner()
    async def dw(self, ctx):
        await ctx.message.delete()
        # Command to delete the webhook link linked to the channel, if there is any for the channel
        webhook = await ctx.channel.webhooks()
        if webhook:
            for hook in webhook:
                await hook.delete()
            await ctx.send('Webhook deleted successfully', delete_after=5)
        else:
            await ctx.send('No webhook found', delete_after=5)

    # Command to send a message as a webhook
    @commands.command(name='sw')
    @commands.is_owner()
    async def sw(self, ctx, *, message):
        await ctx.message.delete()
        webhook = await ctx.channel.webhooks()
        if webhook:
            await webhook[0].send(content=message, username=ctx.author.name, avatar_url=ctx.author.avatar.url)
        else:
            await ctx.send('No webhook found', delete_after=5)


def setup(bot):
    bot.add_cog(Exclusive(bot))
