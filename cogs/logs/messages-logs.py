import discord
from discord.ext import commands


class MessageLogs(commands.Cog):
    def __ini__(self, bot):
        self.bot = bot

    # When a message is deleted
    @commands.Cog.listener("on_message_delete")
    async def message_del(self, message):
        embed = discord.Embed(
            title="Message deleted",
            description=f"Message sent by {message.author.mention} deleted in {message.channel.mention}",
            color=discord.Color.red()
        )
        embed.add_field(name="Content", value=message.content, inline=False)
        embed.set_thumbnail(url=message.author.avatar.url)
        # Get channel by name
        channel = discord.utils.get(message.guild.text_channels, name="messages-logs")
        await channel.send(embed=embed)

    # When a message is edited
    @commands.Cog.listener("on_message_edit")
    async def message_ed(self, before, after):
        embed = discord.Embed(
            title="Message edited",
            description=f"Message sent by {before.author.mention} edited in {before.channel.mention}",
            color=discord.Color.green()
        )
        embed.add_field(name="Before", value=before.content, inline=False)
        embed.add_field(name="After", value=after.content, inline=False)
        embed.set_thumbnail(url=before.author.avatar.url)
        # Get channel by name
        channel = discord.utils.get(before.guild.text_channels, name="messages-logs")
        await channel.send(embed=embed)

    # When a message is pinned
    @commands.Cog.listener("on_message_pin")
    async def message_pin(self, message):
        embed = discord.Embed(
            title="Message pinned",
            description=f"Message sent by {message.author.mention} pinned in {message.channel.mention}",
            color=discord.Color.green()
        )
        embed.add_field(name="Content", value=message.content, inline=False)
        embed.set_thumbnail(url=message.author.avatar.url)
        # Get channel by name
        channel = discord.utils.get(message.guild.text_channels, name="messages-logs")
        await channel.send(embed=embed)

    # When a message is unpinned
    @commands.Cog.listener("on_message_unpin")
    async def message_unpin(self, message):
        embed = discord.Embed(
            title="Message unpinned",
            description=f"Message sent by {message.author.mention} unpinned in {message.channel.mention}",
            color=discord.Color.red()
        )
        embed.add_field(name="Content", value=message.content, inline=False)
        embed.set_thumbnail(url=message.author.avatar.url)
        # Get channel by name
        channel = discord.utils.get(message.guild.text_channels, name="messages-logs")
        await channel.send(embed=embed)


def setup(bot):
    bot.add_cog(MessageLogs(bot))

