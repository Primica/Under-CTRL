import discord
from discord.ext import commands
from discord import slash_command, Embed
import asyncio


class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(name='mute', description='Mute a user for a specific time')
    @commands.has_permissions(manage_messages=True)
    async def mute(self, ctx, user: discord.Member, time: int):
        role = discord.utils.get(ctx.guild.roles, name='Muted')
        if role is None:
            role = await ctx.guild.create_role(name='Muted')
            for channel in ctx.guild.channels:
                await channel.set_permissions(role, send_messages=False)
        await user.add_roles(role)
        await ctx.respond(f'{user.mention} has been muted for {time} minutes.', delete_after=5)
        await asyncio.sleep(time * 60)  # time is in minutes
        await user.remove_roles(role)
        await ctx.respond(f'{user.mention} has been unmuted.', delete_after=5)

    @slash_command(name='unmute', description='Unmute a user')
    @commands.has_permissions(manage_messages=True)
    async def unmute(self, ctx, user: discord.Member):
        role = discord.utils.get(ctx.guild.roles, name='Muted')
        if role is None:
            return await ctx.respond('There is no Muted role in this server.', delete_after=5)
        await user.remove_roles(role)
        await ctx.respond(f'{user.mention} has been unmuted.', delete_after=5)

    @slash_command(name='kick', description='Kick a user')
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, user: discord.Member, *, reason=None):
        await user.kick(reason=reason)
        await ctx.respond(f'{user.mention} has been kicked for {reason}.', delete_after=5)

    @slash_command(name='warn', description='Warn a user')
    @commands.has_permissions(manage_messages=True)
    async def warn(self, ctx, member: discord.Member, reason: str):
        embed = Embed(
            title='You have been warned!',
            description=f'**Reason:** {reason}',
            color=discord.Color.red()
        )
        embed.set_footer(text="Please follow the rules next time or severe actions will be taken.")
        await member.send(embed=embed)
        await ctx.respond(f'{member.mention} has been warned for {reason}', delete_after=5)

    @slash_command(name='voice-mute', description='Mute a user in voice channel')
    @commands.has_permissions(manage_messages=True)
    async def voice_mute(self, ctx, member: discord.Member):
        await member.edit(mute=True)
        await ctx.respond(f'{member.mention} has been muted in voice channel.', delete_after=5)

    @slash_command(name='voice-unmute', description='Unmute a user in voice channel')
    @commands.has_permissions(manage_messages=True)
    async def voice_unmute(self, ctx, member: discord.Member):
        await member.edit(mute=False)
        await ctx.respond(f'{member.mention} has been unmuted in voice channel.', delete_after=5)

    @slash_command(name='voice-move', description='Move a user to another voice channel')
    @commands.has_permissions(manage_messages=True)
    async def voice_move(self, ctx, member: discord.Member, channel: discord.VoiceChannel):
        if member.voice is None:
            await ctx.respond(f'{member.mention} is not in a voice channel.', delete_after=5)
            return
        await member.move_to(channel)
        await ctx.respond(f'{member.mention} has been moved to {channel}.', delete_after=5)

    @slash_command(name='clear', description='Clear messages in a channel')
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount: int):
        # If the amount is greater than 50 return an error
        if amount > 50:
            return await ctx.respond('You cannot delete more than 50 messages at once.', delete_after=5)
        await ctx.channel.purge(limit=amount + 1)
        await ctx.respond(f'{amount} messages have been deleted.', delete_after=5)


def setup(bot):
    bot.add_cog(Moderation(bot))
