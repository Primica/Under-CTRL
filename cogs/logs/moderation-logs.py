import discord
from discord.ext import commands


class ModerationLogs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # When a member is banned
    @commands.Cog.listener("on_member_ban")
    async def on_member_ban(self, guild, user):
        channel = discord.utils.get(guild.text_channels, name="moderation-logs")
        if channel:
            embed = discord.Embed(
                title="Member Banned",
                description=f"{user.mention} has been banned.",
                color=discord.Color.red()
            )
            embed.set_thumbnail(url=user.avatar.url)
            await channel.send(embed=embed)

    # When a member is unbanned
    @commands.Cog.listener("on_member_unban")
    async def on_member_unban(self, guild, user):
        channel = discord.utils.get(guild.text_channels, name="moderation-logs")
        if channel:
            embed = discord.Embed(
                title="Member Unbanned",
                description=f"{user.mention} has been unbanned.",
                color=discord.Color.green()
            )
            embed.set_thumbnail(url=user.avatar.url)
            await channel.send(embed=embed)

    # When a member is kicked
    @commands.Cog.listener("on_member_remove")
    async def on_member_remove(self, member):
        channel = discord.utils.get(member.guild.text_channels, name="moderation-logs")
        if channel:
            embed = discord.Embed(
                title="Member Kicked",
                description=f"{member.mention} has been kicked.",
                color=discord.Color.red()
            )
            embed.set_thumbnail(url=member.avatar.url)
            await channel.send(embed=embed)


def setup(bot):
    bot.add_cog(ModerationLogs(bot))


