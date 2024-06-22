import discord
from discord.ext import commands

whitelist = [
    894900304506658937,
    499501948328869898,
    695280272261775421
]


class DecisionModalYes(discord.ui.Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.add_item(discord.ui.InputText(label="Username du destinataire", style=discord.InputTextStyle.short))

    async def callback(self, interaction: discord.Interaction):
        # If statement to check if the user is correct and if he's actually in the guild
        user = interaction.guild.get_member_named(self.children[0].value)
        if user is None:
            await interaction.response.send_message("L'utilisateur n'a pas été trouvé.", ephemeral=True)
            return
        embed = discord.Embed(
            title="Administration du pôle developpement",
            description=f"Veuillez prendre connaissances des informations ci-dessous {self.children[0].value}",
            color=discord.Color.blurple()
        )
        message = ("Bonjour !\n\nNous avons bien reçu votre candidature et nous vous remercions pour l'intérêt que "
                   "vous portez à notre serveur.\n\nNous vous informons que vous avez été retenu pour un entretien "
                   "d'une durée de 1h10. Une convocation vous sera envoyée sous 48h.\n\nCordialement,\n\nBreaking "
                   "Hardware.")
        embed.add_field(name="Informations", value=message, inline=False)
        embed.add_field(name="Post Scriptum",
                        value="Il est impératif de se présenter à l'heure à l'entretien. En cas d'indisponibilité, "
                              "merci de nous prévenir au plus vite.\nSi nous ne sommes pas prévenus, nous serons dans "
                              "l'obligation de refuser votre candidature.",
                        inline=False)
        embed.set_footer(text="Breaking Hardware")
        await user.send(embed=embed)
        e = discord.Embed(
            title="Candidature acceptée",
            description=f"La candidature de {self.children[0].value} a été acceptée. Par {interaction.user.name}",
            color=discord.Color.green()
        )
        await interaction.response.send_message(embed=e)


class DecisionModalNo(discord.ui.Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.add_item(discord.ui.InputText(label="Username du destinataire", style=discord.InputTextStyle.short))
        self.add_item(discord.ui.InputText(label="Motif", style=discord.InputTextStyle.long))

    async def callback(self, interaction: discord.Interaction):
        # If statement to check if the user is correct and if he's actually in the guild
        user = interaction.guild.get_member_named(self.children[0].value)
        if user is None:
            await interaction.response.send_message("L'utilisateur n'a pas été trouvé.", ephemeral=True)
            return
        embed = discord.Embed(
            title="Administration du pôle developpement",
            description=f"Veuillez prendre connaissances des informations ci-dessous {self.children[0].value}",
            color=discord.Color.blurple()
        )
        message = ("Bonjour !\n\nNous avons bien reçu votre candidature et nous vous remercions pour l'intérêt que "
                   "vous portez à notre serveur.\n\nNous vous informons que vous n'avez pas été "
                   "retenu.\n\nCordialement,\n\nBreaking Hardware.")
        embed.add_field(name="Informations", value=message, inline=False)
        embed.add_field(name="Motif", value=self.children[1].value, inline=False)
        embed.set_footer(text="Breaking Hardware")
        await user.send(embed=embed)
        e = discord.Embed(
            title="Candidature refusée",
            description=f"La candidature de {self.children[0].value} a été refusée. Par {interaction.user.name}",
            color=discord.Color.red()
        )
        e.add_field(name="Motif", value=self.children[1].value, inline=False)
        await interaction.response.send_message(embed=e)


class DecisionView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="-y", style=discord.ButtonStyle.green, custom_id="yes", emoji="📦")
    async def callback_yes(self, button, interaction):
        self.disable_all_items()
        await interaction.response.send_modal(DecisionModalYes(title="Message de confirmation"))

    @discord.ui.button(label="-n", style=discord.ButtonStyle.red, custom_id="no", emoji="❌")
    async def callback_no(self, button, interaction):
        self.disable_all_items()
        await interaction.response.send_modal(DecisionModalNo(title="Message de refus"))


class MyModal(discord.ui.Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.add_item(discord.ui.InputText(label="Nom, Prénom", style=discord.InputTextStyle.short))
        self.add_item(discord.ui.InputText(label="Languages de programmations", style=discord.InputTextStyle.short))
        self.add_item(discord.ui.InputText(label="Compétences / expériences", style=discord.InputTextStyle.long))
        self.add_item(discord.ui.InputText(label="Motivations", style=discord.InputTextStyle.long))
        self.add_item(discord.ui.InputText(label="Disponibilité", style=discord.InputTextStyle.short))

    async def callback(self, interaction: discord.Interaction):
        embed = discord.Embed(title=f"Candidature de {interaction.user}", color=discord.Color.nitro_pink())
        embed.add_field(name="Author", value=interaction.user.name, inline=False)
        embed.add_field(name="Nom, Prénom", value=self.children[0].value, inline=False)
        embed.add_field(name="Languages de programmations", value=self.children[1].value, inline=False)
        embed.add_field(name="Compétences / expériences", value=self.children[2].value, inline=False)
        embed.add_field(name="Motivations", value=self.children[3].value, inline=False)
        embed.add_field(name="Disponibilité", value=self.children[4].value, inline=False)

        channel = interaction.guild.get_channel(1249752206698221631)
        await channel.send(embeds=[embed], view=DecisionView())
        await interaction.response.send_message("Candidature envoyée !", ephemeral=True)


class CandidatureView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Candidater", style=discord.ButtonStyle.primary, custom_id="candidater", emoji="📝")
    async def callback_candidater(self, button, interaction):
        await interaction.response.send_modal(MyModal(title="Candidature"))

    @discord.ui.button(label="Informations relatives", style=discord.ButtonStyle.secondary, custom_id="informations",
                       emoji="⚙️")
    async def callback_informations(self, button, interaction):
        embed = discord.Embed(
            title="Informations relatives",
            colour=discord.Colour.orange()
        )
        embed.add_field(
            name="Temps de réponse",
            value="Les candidatures sont traitées sous 48h. Par conséquent, il est inutile de relancer le staff.",
            inline=False
        )
        embed.add_field(
            name="Réclamation",
            value="En cas de réclamation, veuillez contacter la gestion dev en envoyant directement un message au bot"
                  ", le message sera transmis a la gestion en place. Tout abus sera sanctionné.",
            inline=False
        )
        embed.add_field(
            name="Contenu et déroulé de l'entretien",
            value="L'entretient se déroulera en 2 partie : 10 minutes de présentation (tour de table) et 1h d'examen"
                  " de vos compétences sur un sujet donné (algorithmique, programmation, etc...). Ainsi il est "
                  "impératif de prévoir une plage horaire de 1h10 pour l'entretien.",
            inline=False
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)


class Panel(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(name='send-candidature-panel', description='Send the candidature panel')
    @commands.has_permissions(administrator=True)
    async def send_candidature_panel(self, ctx, channel: discord.TextChannel):
        embed = discord.Embed(
            title="Candidatures - Développeurs",
            description="Les candidatures se doivent d'être sérieuses et complètes. Une réponse vous sera donnée sous "
                        "48h. En cas de refus, un motif vous sera donné. En cas d'acceptation, un entretien vous sera "
                        "proposé.",
            color=discord.Color.blurple()
        )
        embed.add_field(name="Note importante", value="Si une première réponse est positive un premier entretien de 30 "
                                                      "minutes vous sera proposé pour faire connaissances, c'est cet "
                                                      "entretien qui déterminera si vous êtes retenu pour passer le "
                                                      "test technique de 60 minutes.", inline=False)
        embed.set_footer(text="Cordialement, L'équipe Breaking Hardware")
        embed.set_thumbnail(url=ctx.guild.icon.url)
        await channel.send(embed=embed, view=CandidatureView())
        await ctx.respond("Panel envoyé !", ephemeral=True)


def setup(bot):
    bot.add_cog(Panel(bot))
