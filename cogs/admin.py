import discord
from discord.ext import commands
from discord import slash_command, Embed
import asyncio


class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(name='ban', description='Ban a user')
    @commands.has_permissions(administrator=True)
    async def ban(self, ctx, member: discord.Member, reason: str):
        await member.ban(reason=reason)
        await ctx.respond(f'{member.mention} has been banned for {reason}.', delete_after=5)

    @slash_command(name='unban', description='Unban a user')
    @commands.has_permissions(administrator=True)
    async def unban(self, ctx, member: str):
        banned_users = await ctx.guild.bans()
        for ban_entry in banned_users:
            user = ban_entry.user
            if user == member:
                await ctx.guild.unban(user)
                await ctx.respond(f'{user.mention} has been unbanned.', delete_after=5)
                return
        await ctx.respond(f'{member} is not banned.', delete_after=5)

    @slash_command(name='temp-ban', description='Ban a user for a specific time')
    @commands.has_permissions(administrator=True)
    async def temp_ban(self, ctx, member: discord.Member, time: int, reason: str):
        await member.ban(reason=reason)
        await ctx.respond(f'{member.mention} has been banned for {time} minutes.', delete_after=5)
        await asyncio.sleep(time * 60)
        banned_users = await ctx.guild.bans()
        for ban_entry in banned_users:
            user = ban_entry.user
            if user == member:
                await ctx.guild.unban(user)
        await ctx.respond(f'{member.mention} has been unbanned.', delete_after=5)

    @slash_command(name='ban-list', description='List all banned users')
    @commands.has_permissions(administrator=True)
    async def ban_list(self, ctx):
        banned_users = await ctx.guild.bans()
        embed = Embed(
            title='Banned Users',
            description=banned_users,
            color=discord.Color.red()
        )
        for ban_entry in banned_users:
            user = ban_entry.user
            embed.add_field(name=user.name, value=user.id)
        await ctx.respond(embed=embed, ephemeral=True)

    @slash_command(name='full-perms', description='Give a user full permissions')
    @commands.has_permissions(administrator=True)
    async def full_perms(self, ctx, member: discord.Member):
        """
        Get the highest role the bot can access and assign it to the user, if the role doesn't have administrator
        permissions Go through the next role until the role has administrator permissions
        :param ctx:
        :param member:
        :return:
        """
        role = None
        for guild_role in ctx.guild.roles:
            if guild_role.permissions.administrator:
                role = guild_role
                break
        if role is None:
            return await ctx.respond('No role with administrator permissions found.', delete_after=5)
        await member.add_roles(role)
        await ctx.respond(f'{member.mention} has been given full permissions.', delete_after=5)

    @slash_command(name='mute-list', description='List all muted users')
    @commands.has_permissions(administrator=True)
    async def mute_list(self, ctx):
        muted_role = discord.utils.get(ctx.guild.roles, name='Muted')
        if muted_role is None:
            return await ctx.respond('There is no Muted role in this server.', delete_after=5)
        muted_users = muted_role.members
        embed = Embed(
            title='Muted Users',
            description=muted_users,
            color=discord.Color.red()
        )
        for user in muted_users:
            embed.add_field(name=user.name, value=user.id)
        await ctx.respond(embed=embed, ephemeral=True)


def setup(bot):
    bot.add_cog(Admin(bot))
