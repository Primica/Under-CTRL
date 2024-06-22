import discord
from discord.ext import commands


class RolesLogs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # When a member is given a role
    @commands.Cog.listener("on_member_update")
    async def role_add(self, before, after):
        if len(before.roles) < len(after.roles):
            role = next(role for role in after.roles if role not in before.roles)
            channel = discord.utils.get(before.guild.text_channels, name="roles-logs")
            if channel:
                embed = discord.Embed(
                    title="Role Added",
                    description=f"{after.mention} has been given the {role.mention} role.",
                    color=discord.Color.green()
                )
                embed.set_thumbnail(url=after.avatar.url)
                await channel.send(embed=embed)

    # When a member is removed from a role
    @commands.Cog.listener("on_member_update")
    async def role_remove(self, before, after):
        if len(before.roles) > len(after.roles):
            role = next(role for role in before.roles if role not in after.roles)
            channel = discord.utils.get(before.guild.text_channels, name="roles-logs")
            if channel:
                embed = discord.Embed(
                    title="Role Removed",
                    description=f"{after.mention} has been removed from the {role.mention} role.",
                    color=discord.Color.red()
                )
                embed.set_thumbnail(url=after.avatar.url)
                await channel.send(embed=embed)

    # When a role is created
    @commands.Cog.listener("on_guild_role_create")
    async def role_create(self, role):
        channel = discord.utils.get(role.guild.text_channels, name="roles-logs")
        if channel:
            embed = discord.Embed(
                title="Role Created",
                description=f"The {role.mention} role has been created.",
                color=discord.Color.green()
            )
            await channel.send(embed=embed)

    # When a role is deleted
    @commands.Cog.listener("on_guild_role_delete")
    async def role_delete(self, role):
        channel = discord.utils.get(role.guild.text_channels, name="roles-logs")
        if channel:
            embed = discord.Embed(
                title="Role Deleted",
                description=f"The {role.name} role has been deleted.",
                color=discord.Color.red()
            )
            await channel.send(embed=embed)

    # When a role is updated
    @commands.Cog.listener("on_guild_role_update")
    async def role_update(self, before, after):
        if before.name != after.name:
            channel = discord.utils.get(before.guild.text_channels, name="roles-logs")
            if channel:
                embed = discord.Embed(
                    title="Role Updated",
                    description=f"The {before.mention} role has been renamed to {after.mention}.",
                    color=discord.Color.blurple()
                )
                await channel.send(embed=embed)
        elif before.color != after.color:
            channel = discord.utils.get(before.guild.text_channels, name="roles-logs")
            if channel:
                embed = discord.Embed(
                    title="Role Updated",
                    description=f"The {before.mention} role color has been changed.",
                    color=discord.Color.blurple()
                )
                await channel.send(embed=embed)
        elif before.permissions != after.permissions:
            channel = discord.utils.get(before.guild.text_channels, name="roles-logs")
            if channel:
                embed = discord.Embed(
                    title="Role Updated",
                    description=f"The {before.mention} role permissions have been changed.",
                    color=discord.Color.blurple()
                )
                await channel.send(embed=embed)
        elif before.hoist != after.hoist:
            channel = discord.utils.get(before.guild.text_channels, name="roles-logs")
            if channel:
                embed = discord.Embed(
                    title="Role Updated",
                    description=f"The {before.mention} role hoist status has been changed.",
                    color=discord.Color.blurple()
                )
                await channel.send(embed=embed)
        elif before.mentionable != after.mentionable:
            channel = discord.utils.get(before.guild.text_channels, name="roles-logs")
            if channel:
                embed = discord.Embed(
                    title="Role Updated",
                    description=f"The {before.mention} role mentionable status has been changed.",
                    color=discord.Color.blurple()
                )
                await channel.send(embed=embed)
        elif before.position != after.position:
            channel = discord.utils.get(before.guild.text_channels, name="roles-logs")
            if channel:
                embed = discord.Embed(
                    title="Role Updated",
                    description=f"The {before.mention} role position has been changed.",
                    color=discord.Color.blurple()
                )
                await channel.send(embed=embed)
        elif before.managed != after.managed:
            channel = discord.utils.get(before.guild.text_channels, name="roles-logs")
            if channel:
                embed = discord.Embed(
                    title="Role Updated",
                    description=f"The {before.mention} role managed status has been changed.",
                    color=discord.Color.blurple()
                )
                await channel.send(embed=embed)


def setup(bot):
    bot.add_cog(RolesLogs(bot))
