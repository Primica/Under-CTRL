import discord
from discord.ext import commands
import json
from cogs.packages.panel import DecisionView, CandidatureView
from cogs.candidatures import CandidatureViewDiscord, DiscordDecisionView

# Loading the config file
with open('config.json') as f:
    config = json.load(f)
    token = config['token']

# Bot prefix and permissions
bot = commands.Bot(command_prefix='+', intents=discord.Intents.all())


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    print(f'Bot ID: {bot.user.id}')
    bot.add_view(DecisionView())
    bot.add_view(CandidatureView())
    bot.add_view(CandidatureViewDiscord())
    bot.add_view(DiscordDecisionView())


@bot.event
async def on_member_join(member):
    # Get channel by ID
    channel = member.guild.get_channel(1211085560286810123)
    embed = discord.Embed(
        title=f'Bienvenue {member.name} à Breaking Hardware !',
        description=f'Tu es le {len(member.guild.members)}ème membre !\n\n '
                    f'Pense à jeter un oeil au réglement, si tu souhaite rentrer dans le staff tu peux faire une '
                    f'candidature !',
        color=discord.Color.blurple()
    )
    embed.set_thumbnail(url=member.avatar.url)
    await channel.send(embed=embed)


@bot.slash_command(name='report', description='Report a user')
async def report(ctx, user: discord.Member, reason: str):
    e = discord.Embed(
        title='User Report',
        description=f'{user.mention} has been reported for {reason}',
        color=discord.Color.red()
    )
    e.set_footer(text=f'Reported by {ctx.author}')
    report_channel = discord.utils.get(ctx.guild.text_channels, name='reports')
    await report_channel.send(embed=e)
    await ctx.respond('The user has been reported successfully.', delete_after=5)


# The cogs in the 'cogs' folder are loaded here
Cogs_main = [
    'moderation',
    'admin',
    'automod',
    'gestion',
    'candidatures',
    'exclusive'
]

# The cogs in the 'packages' folder are loaded here (it's a subfolder of 'cogs' folder)
Cogs_packages = [
    'mail-sys',
    'panel'
]

# The cogs in the 'logs' folder are loaded here (it's a subfolder of 'cogs' folder)
Cogs_logs = [
    'moderation-logs',
    'voice-logs',
    'roles-logs',
    'messages-logs'
]

for cog in Cogs_main:
    bot.load_extension(f'cogs.{cog}')

for cog in Cogs_packages:
    bot.load_extension(f'cogs.packages.{cog}')

for cog in Cogs_logs:
    bot.load_extension(f'cogs.logs.{cog}')

if __name__ == '__main__':
    bot.run(token)
