import discord
from discord.ext import commands, tasks
import asyncio
from collections import defaultdict, deque
from datetime import datetime, timedelta

user_messages = defaultdict(lambda: deque(maxlen=4))


class Automod(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.user_message_count = defaultdict(int)
        self.spam_limit = 5

    @commands.Cog.listener("on_message")
    async def anti_link(self, message):
        if message.author.bot:
            return
        if 'https://' in message.content or 'discord.gg' in message.content:
            await message.delete()
            await message.channel.send(f'{message.author.mention}, you cannot send links here.', delete_after=5)

    @commands.Cog.listener("on_message")
    async def anti_mention(self, message):
        if message.author.bot:
            return
        # If the messages contain more or equal to 3 mentions, even if it's the 3 same mentions delete the message
        if len(message.mentions) >= 3:
            await message.delete()
            await message.channel.send(f'{message.author.mention}, You are not allowed to ping such a number of persons'
                                       f'', delete_after=5)
            return

    @commands.Cog.listener("on_message")
    async def anti_spam(self, message):
        if message.author.bot:
            return
        now = datetime.utcnow()
        user_id = message.author.id
        user_messages[user_id].append(now)

        if len(user_messages[user_id]) >= 4:
            if (now - user_messages[user_id][0]) < timedelta(seconds=5):
                # Purge the last 5 messages from the user
                await message.channel.purge(limit=5, check=lambda m: m.author.id == user_id)
                await message.channel.send(f'{message.author.mention}, you are sending messages too quickly.', delete_after=5)
                await message.author.add_roles(discord.utils.get(message.guild.roles, name='Muted'))
                await asyncio.sleep(15 * 60)
                await message.author.remove_roles(discord.utils.get(message.guild.roles, name='Muted'))


def setup(bot):
    bot.add_cog(Automod(bot))
