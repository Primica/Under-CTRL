import discord
from discord import slash_command
from discord.ext import commands


class Gestion(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(name='rank', description='Rank a user')
    @commands.has_role(1224454647943663616)
    async def rank(self, ctx, member: discord.Member, role: discord.Role):
        # If the role is higher than the author's highest role, return an error
        if role.position > ctx.author.top_role.position:
            return await ctx.respond('You cannot assign a role higher than your highest role.', ephemeral=True)
        await member.add_roles(role)
        await ctx.respond(f'{member.mention} has been ranked as {role.name}.', delete_after=5)

    @slash_command(name='unrank', description='Unrank a user')
    @commands.has_role(1224454647943663616)
    async def unrank(self, ctx, member: discord.Member, role: discord.Role):
        await member.remove_roles(role)
        await ctx.respond(f'{member.mention} has been unranked.', delete_after=5)


def setup(bot):
    bot.add_cog(Gestion(bot))