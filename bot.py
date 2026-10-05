import os
import asyncio
import discord
from discord import app_commands
from python_aternos import Client

DISCORD_TOKEN = os.environ["MTU1NjMzMzU2MjU1MzE3MjA4MQ.GGxenj.QjA42BCmwf4kzOIvu44vB1dajqnbUx5uRJluMU"]
ATERNOS_USER = os.environ["SGDP27"]
ATERNOS_PASS = os.environ["SGDPmc"]
ROLE_ID = int(os.environ.get("ALLOWED_ROLE_ID", "0"))  # 0 = tout le monde
ATERNOS_SESSION = os.environ.get("ATERNOS_SESSION")     # optionnel (cookie)

# Connexion à Aternos (syntaxe python-aternos v3)
aternos = Client()
if ATERNOS_SESSION:
    aternos.login_with_session(ATERNOS_SESSION)
else:
    aternos.login(ATERNOS_USER, ATERNOS_PASS)
server = aternos.account.list_servers()[0]

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)


def allowed(interaction: discord.Interaction) -> bool:
    if ROLE_ID == 0:
        return True
    return any(r.id == ROLE_ID for r in getattr(interaction.user, "roles", []))


@tree.command(name="start", description="Lance le serveur Minecraft")
async def start(interaction: discord.Interaction):
    if not allowed(interaction):
        await interaction.response.send_message("Tu n'as pas la permission.", ephemeral=True)
        return
    await interaction.response.defer()
    try:
        await asyncio.to_thread(server.fetch)
        if server.status != "offline":
            await interaction.followup.send(f"Le serveur est déjà `{server.status}`.")
            return
        await asyncio.to_thread(server.start)
        await interaction.followup.send("Démarrage du serveur en cours... ⏳")
    except Exception as e:
        await interaction.followup.send(f"Erreur : `{e}`")


@tree.command(name="stop", description="Arrête le serveur Minecraft")
async def stop(interaction: discord.Interaction):
    if not allowed(interaction):
        await interaction.response.send_message("Tu n'as pas la permission.", ephemeral=True)
        return
    await interaction.response.defer()
    try:
        await asyncio.to_thread(server.fetch)
        await asyncio.to_thread(server.stop)
        await interaction.followup.send("Arrêt du serveur.")
    except Exception as e:
        await interaction.followup.send(f"Erreur : `{e}`")


@tree.command(name="status", description="Statut du serveur")
async def status(interaction: discord.Interaction):
    await interaction.response.defer()
    try:
        await asyncio.to_thread(server.fetch)
        await interaction.followup.send(
            f"Statut : `{server.status}` | Joueurs : {server.players_count}/{server.slots}"
        )
    except Exception as e:
        await interaction.followup.send(f"Erreur : `{e}`")


@client.event
async def on_ready():
    await tree.sync()
    print(f"Connecté en tant que {client.user}")


client.run(DISCORD_TOKEN)
