import discord
from discord.ext import commands
from discord import slash_command, Embed
import datetime


class CandidatureModal(discord.ui.Modal):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.add_item(discord.ui.InputText(label="Rôle souhaité", style=discord.InputTextStyle.short))
        self.add_item(discord.ui.InputText(label="Motivations", style=discord.InputTextStyle.long))
        self.add_item(discord.ui.InputText(label="Expérience", style=discord.InputTextStyle.long))
        self.add_item(discord.ui.InputText(label="Disponibilité", style=discord.InputTextStyle.short))

    async def callback(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title=f"Candidature de {interaction.user}",
            color=discord.Color.nitro_pink()
        )
        embed.add_field(name="Author", value=interaction.user.name, inline=False)
        embed.add_field(name="Rôle souhaité", value=self.children[0].value, inline=False)
        embed.add_field(name="Motivations", value=self.children[1].value, inline=False)
        embed.add_field(name="Expérience", value=self.children[2].value, inline=False)
        embed.add_field(name="Disponibilité", value=self.children[3].value, inline=False)

        channel = interaction.guild.get_channel(1225376692500041728)
        await channel.send(embeds=[embed])
        await interaction.response.send_message("Candidature envoyée !", ephemeral=True)


class CandidatureViewDiscord(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Candidater", style=discord.ButtonStyle.primary, custom_id="candid_discord", emoji="📝")
    async def callback_candidater(self, button, interaction):
        await interaction.response.send_modal(CandidatureModal(title="Candidature"))


class CandidatureModalYes(discord.ui.Modal):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.add_item(discord.ui.InputText(label="Username du candidat", style=discord.InputTextStyle.short))

    async def callback(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="Administration du pôle discord - Candidature acceptée",
            description=f"Votre candidature à été acceptée par {interaction.user.name} le {datetime.datetime.now()}",
        )
        embed.add_field(name="Un entretient vous sera proposé sous 48h par les gérants du pôle associé à votre "
                             "candidature", value="C'est un entretient oral, il est impératif de l'honorer sous peine "
                                                  "de sanctions. La durée de celui-ci vous sera également communiquée.")
        embed.set_footer(text="Merci de votre compréhension et de votre patience.")
        user = interaction.guild.get_member_named(self.children[0].value)
        await user.send(embed=embed)
        e = discord.Embed(
            title="Candidature acceptée",
            description=f"La candidature de {self.children[0].value} a été acceptée. Par {interaction.user.name}",
            color=discord.Color.green()
        )
        await interaction.response.send_message(embed=e)


class CandidatureModalNo(discord.ui.Modal):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.add_item(discord.ui.InputText(label="Username du candidat", style=discord.InputTextStyle.short))
        self.add_item(discord.ui.InputText(label="Motif", style=discord.InputTextStyle.short))

    async def callback(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="Administration du pôle discord - Candidature refusée",
            description=f"Votre candidature à été refusée par {interaction.user.name} le {datetime.datetime.now()}",
        )
        embed.add_field(name="Motif", value=self.children[1].value)
        embed.set_footer(text="Merci de votre compréhension.")
        user = interaction.guild.get_member_named(self.children[0].value)
        await user.send(embed=embed)
        e = discord.Embed(
            title="Candidature refusée",
            description=f"La candidature de {self.children[0].value} a été refusée. Par {interaction.user.name}",
            color=discord.Color.red()
        )
        e.add_field(name="Motif", value=self.children[1].value, inline=False)
        await interaction.response.send_message(embed=e)


class DiscordDecisionView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Accepter", style=discord.ButtonStyle.green, custom_id="yes", emoji="✅")
    async def callback_yes(self, button, interaction):
        self.disable_all_items()
        await interaction.response.send_modal(CandidatureModalYes(title="Message de confirmation"))

    @discord.ui.button(label="Refuser", style=discord.ButtonStyle.red, custom_id="no", emoji="❌")
    async def callback_no(self, button, interaction):
        self.disable_all_items()
        await interaction.response.send_modal(CandidatureModalNo(title="Message de refus"))


class CandidaturesDiscord(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(name='candidature-discord', description='Envoie le panel de candidature Discord')
    @commands.has_permissions(administrator=True)
    async def candidature_discord(self, ctx, channel: discord.TextChannel):
        embed = Embed(
            title="Conditions de Recrutement",
            description="Pour candidater, vous devez remplir les conditions suivantes :",
            color=discord.Color.blurple()
        )
        embed.add_field(name="1. Avoir minimum 15 ans", value="Nous recrutons des personnes matures et responsables.")
        embed.add_field(name="2. Connaître discord", value="Avoir des connaissances approfondies sur Discord.")
        embed.add_field(name="3. Être actif", value="Être actif sur le serveur Discord.")
        embed.add_field(name="4. Avoir eu une activité sur le serveur", value="Avoir participé à la vie du serveur "
                                                                              "pendant plusieurs jours.")
        embed.add_field(name="5. Être motivé", value="Avoir une réelle motivation à rejoindre l'équipe.")
        embed.add_field(name="6. Avoir une bonne orthographe", value="Faire attention à son orthographe.")
        embed.set_thumbnail(url=ctx.guild.icon.url)
        embed.set_footer(text="Toutes les candidatures sont étudiées avec attention. Les candidatures troll seront "
                              "sévèrement sanctionnées.")
        await channel.send(embed=embed, view=CandidatureViewDiscord())


def setup(bot):
    bot.add_cog(CandidaturesDiscord(bot))
