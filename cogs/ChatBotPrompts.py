from discord import app_commands
from discord.ext import commands
import discord
from utils import gptFunctions


class ChatBotPrompts(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
        super().__init__()

    @app_commands.command(
        name="simple_query", description="Give a simple query to the bot"
    )
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def simple_query(
        self, interaction: discord.Interaction, message: str, model: str = "gpt-4o"
    ):
        if len(message) < 1:
            await interaction.response.send_message("Please provide a query")
            return
        response = gptFunctions.perform_gpt_query(query=message, model=model)
        embed = discord.Embed(title="Chatbot Prompt", color=discord.Color.blue())
        embed.set_author(
            name=f"query by {interaction.user.display_name} and response from {model}",
            icon_url=interaction.user.avatar,
        )
        embed.add_field(name="Query", value=message, inline=False)
        embed.add_field(name="Response", value=response, inline=False)
        await interaction.response.send_message(embed=embed)

    @app_commands.checks.has_permissions(administrator=True)
    @app_commands.command()
    async def qotw(self, interaction: discord.Interaction): 
        ...

    @commands.Cog.listener()
    async def on_ready(self):
        print("ChatBotPrompts.py is ready")


async def setup(client):
    await client.add_cog(ChatBotPrompts(client))
