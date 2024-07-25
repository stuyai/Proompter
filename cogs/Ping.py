from discord.ext import commands
from discord import app_commands
import discord

# import discord


class Ping(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
        super().__init__()

    @app_commands.command(name="ping", description="Check the bot's latency")
    async def ping(self, interaction: discord.Interaction):
        await interaction.response.send_message(
            f"Pong! {round(self.client.latency * 1000)}ms"
        )

    @commands.Cog.listener()
    async def on_ready(self):
        print("Ping.py is ready")


async def setup(client):
    await client.add_cog(Ping(client))
