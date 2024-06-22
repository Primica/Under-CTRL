import discord
from discord.ext import commands

whitelist = [894900304506658937]


class MailSys(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener("on_message")
    async def dev_mail(self, message):
        if message.author == self.bot.user:
            return
        if isinstance(message.channel, discord.DMChannel):
            e = discord.Embed(
                description=message.content,
                color=discord.Color.blurple()
            )
            e.set_author(name=message.author.name, icon_url=message.author.avatar.url)
            e.set_footer(text=f"User ID: {message.author.id}")

            if message.attachments:
                file = discord.File("fichier_joint", filename=message.attachments[0].filename)
                await message.attachments[0].save("fichier_joint")
                e.set_image(url=f"attachment://{message.attachments[0].filename}")

                await self.bot.get_channel(1248661972837208134).send(embed=e, file=file)
            else:
                await self.bot.get_channel(1248661972837208134).send(embed=e)

    @commands.command(name='cdm')
    @commands.is_owner()
    async def cdm(self, ctx):
        if isinstance(ctx.channel, discord.DMChannel):
            async for message in ctx.channel.history(limit=100):
                if message.author == self.bot.user:
                    await message.delete()
            await ctx.send("Messages deleted.", delete_after=3)
        else:
            await ctx.send("This command can only be used in DMs.", delete_after=3)

    @commands.command(name='mail')
    async def mail(self, ctx, member: discord.Member, *, content: str):
        if ctx.author.id not in whitelist:
            await ctx.send("You do not have permission to use this command.", ephemeral=True)
            return
        try:
            e = discord.Embed(description=content, color=discord.Color.blurple())
            e.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url)

            if ctx.message.attachments:
                await ctx.message.attachments[0].save("fichier_joint")

                file = discord.File("fichier_joint", filename=ctx.message.attachments[0].filename)

                await member.send(embed=e, file=file)
            else:
                await member.send(embed=e)

            embed = discord.Embed(
                title=f"Message sent to {member.name}",
                description=content,
                color=discord.Color.blurple()
            )
            await ctx.send(embed=embed, delete_after=3)
        except Exception as e:
            await ctx.send(f"An error occurred: {e}", ephemeral=True)

    @discord.slash_command(name='message', description='Send a message to a user')
    async def message(self, ctx, member: discord.Member, content: str):
        if ctx.author.id not in whitelist:
            return await ctx.respond("You do not have permission to use this command.", ephemeral=True)
        try:
            e = discord.Embed(description=content, color=discord.Color.blurple())
            e.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url)

            await member.send(embed=e)

            embed = discord.Embed(
                title=f"Message sent to {member.name}",
                description=content,
                color=discord.Color.blurple()
            )
            await ctx.respond(embed=embed)
        except Exception as e:
            await ctx.respond(f"An error occurred: {e}", ephemeral=True)


def setup(bot):
    bot.add_cog(MailSys(bot))
