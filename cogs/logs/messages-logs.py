import discord
from discord.ext import commands

class MessageLogs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener("on_message_delete")
    async def on_message_delete(self, message):
        channel = discord.utils.get(message.guild.text_channels, name="message-logs")
        if channel:
            embed = discord.Embed(
                title="Message Deleted",
                description=f"**Author:** {message.author.mention}\n**Channel:** {message.channel.mention}\n\n{message.content}",
                color=discord.Color.red()
            )
            await channel.send(embed=embed)

    @commands.Cog.listener("on_message_edit")
    async def on_message_edit(self, before, after):
        channel = discord.utils.get(before.guild.text_channels, name="message-logs")
        if channel:
            embed = discord.Embed(
                title="Message Edited",
                description=f"**Author:** {before.author.mention}\n**Channel:** {before.channel.mention}\n\n**Before:** {before.content}\n\n**After:** {after.content}",
                color=discord.Color.red()
            )
            await channel.send(embed=embed)


def setup(bot):
    bot.add_cog(MessageLogs(bot))

