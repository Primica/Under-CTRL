import discord
from discord.ext import commands


class MessageLogs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener("on_message_delete")
    async def del_msg(self, message):
        channel = discord.utils.get(message.guild.text_channels, name="messages-logs")
        if channel:
            embed = discord.Embed(
                title="Message Deleted",
                description=f"**Author:** {message.author.mention}\n**Channel:** {message.channel.mention}\n**Message:** {message.content}",
                color=discord.Color.red()
            )
            embed.set_thumbnail(url=message.author.avatar.url)
            await channel.send(embed=embed)

    @commands.Cog.listener("on_message_edit")
    async def edit_msg(self, before, after):
        channel = discord.utils.get(before.guild.text_channels, name="messages-logs")
        if channel:
            embed = discord.Embed(
                title="Message Edited",
                description=f"**Author:** {before.author.mention}\n**Channel:** {before.channel.mention}\n**Before:** {before.content}\n**After:** {after.content}",
                color=discord.Color.orange()
            )
            embed.set_thumbnail(url=before.author.avatar.url)
            await channel.send(embed=embed)


def setup(bot):
    bot.add_cog(MessageLogs(bot))
