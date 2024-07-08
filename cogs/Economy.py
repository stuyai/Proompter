from discord.ext import commands
import discord
from discord import app_commands

class Economy(commands.Cog):
    def __init__(self, client:commands.Bot):
        self.client = client
        super().__init__()
    
    @commands.Cog.listener()
    async def on_ready(self):
        print("Economy.py is ready")
    
    @app_commands.command(name="balance", description="Check your balance")
    async def balance(self, interaction:discord.Interaction):
        await interaction.response.send_message("This is your balance {testing}", ephemeral=True)
        

async def setup(client):
    await client.add_cog(Economy(client))

        