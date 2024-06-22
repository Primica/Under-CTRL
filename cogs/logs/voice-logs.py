import discord
from discord.ext import commands


class VoiceLogs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # When a member joins a voice channel
    @commands.Cog.listener("on_voice_state_update")
    async def voice_join(self, member, before, after):
        if before.channel is None and after.channel is not None:
            channel = discord.utils.get(member.guild.text_channels, name="voice-logs")
            if channel:
                embed = discord.Embed(
                    title="Member Joined Voice Channel",
                    description=f"{member.mention} has joined {after.channel.mention}.",
                    color=discord.Color.green()
                )
                embed.set_thumbnail(url=member.avatar.url)
                await channel.send(embed=embed)
        elif before.channel is not None and after.channel is None:
            channel = discord.utils.get(member.guild.text_channels, name="voice-logs")
            if channel:
                embed = discord.Embed(
                    title="Member Left Voice Channel",
                    description=f"{member.mention} has left {before.channel.mention}.",
                    color=discord.Color.red()
                )
                embed.set_thumbnail(url=member.avatar.url)
                await channel.send(embed=embed)
        elif before.channel is not None and after.channel is not None and before.channel != after.channel:
            channel = discord.utils.get(member.guild.text_channels, name="voice-logs")
            if channel:
                embed = discord.Embed(
                    title="Member Changed Voice Channel",
                    description=f"{member.mention} has moved from {before.channel.mention} to {after.channel.mention}.",
                    color=discord.Color.blurple()
                )
                embed.set_thumbnail(url=member.avatar.url)
                await channel.send(embed=embed)

    # When a member is muted in a voice channel
    @commands.Cog.listener("on_voice_state_update")
    async def mute_voice(self, member, before, after):
        if before.mute is False and after.mute is True:
            channel = discord.utils.get(member.guild.text_channels, name="voice-logs")
            if channel:
                embed = discord.Embed(
                    title="Member Muted",
                    description=f"{member.mention} has been muted in {before.channel.mention}.",
                    color=discord.Color.red()
                )
                embed.set_thumbnail(url=member.avatar.url)
                await channel.send(embed=embed)
        elif before.mute is True and after.mute is False:
            channel = discord.utils.get(member.guild.text_channels, name="voice-logs")
            if channel:
                embed = discord.Embed(
                    title="Member Unmuted",
                    description=f"{member.mention} has been unmuted in {before.channel.mention}.",
                    color=discord.Color.green()
                )
                embed.set_thumbnail(url=member.avatar.url)
                await channel.send(embed=embed)

    # When a member is deafened in a voice channel
    @commands.Cog.listener("on_voice_state_update")
    async def voice_deafen(self, member, before, after):
        if before.deaf is False and after.deaf is True:
            channel = discord.utils.get(member.guild.text_channels, name="voice-logs")
            if channel:
                embed = discord.Embed(
                    title="Member Deafened",
                    description=f"{member.mention} has been deafened in {before.channel.mention}.",
                    color=discord.Color.red()
                )
                embed.set_thumbnail(url=member.avatar.url)
                await channel.send(embed=embed)
        elif before.deaf is True and after.deaf is False:
            channel = discord.utils.get(member.guild.text_channels, name="voice-logs")
            if channel:
                embed = discord.Embed(
                    title="Member Undeafened",
                    description=f"{member.mention} has been undeafened in {before.channel.mention}.",
                    color=discord.Color.green()
                )
                embed.set_thumbnail(url=member.avatar.url)
                await channel.send(embed=embed)

    # When a member is moved to a different voice channel
    @commands.Cog.listener("on_voice_state_update")
    async def voice_move(self, member, before, after):
        if before.channel is not None and after.channel is not None and before.channel != after.channel:
            channel = discord.utils.get(member.guild.text_channels, name="voice-logs")
            if channel:
                embed = discord.Embed(
                    title="Member Moved Voice Channel",
                    description=f"{member.mention} has been moved from {before.channel.mention} to {after.channel.mention}.",
                    color=discord.Color.blurple()
                )
                embed.set_thumbnail(url=member.avatar.url)
                await channel.send(embed=embed)

    # When a member is disconnected from a voice channel
    @commands.Cog.listener("on_voice_state_update")
    async def voice_disconnect(self, member, before, after):
        if before.channel is not None and after.channel is None:
            channel = discord.utils.get(member.guild.text_channels, name="voice-logs")
            if channel:
                embed = discord.Embed(
                    title="Member Disconnected",
                    description=f"{member.mention} has been disconnected from {before.channel.mention}.",
                    color=discord.Color.red()
                )
                embed.set_thumbnail(url=member.avatar.url)
                await channel.send(embed=embed)


def setup(bot):
    bot.add_cog(VoiceLogs(bot))
