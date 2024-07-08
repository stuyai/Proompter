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
    @app_commands.command(name="qotw", description="Get the question of the week")
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def qotw(self, interaction: discord.Interaction, websites: str):
        # https://stackoverflow.com/questions/67249570/how-do-i-mention-everyone-in-discord-py
        await interaction.response.defer()
        try:
            response = await gptFunctions.createQOTW(websites)
            await interaction.followup.send(
                response, allowed_mentions=discord.AllowedMentions(everyone=True)
            )
        except Exception as e:
            await interaction.followup.send(f"An error occured: {e}", ephemeral=True)

    @commands.Cog.listener()
    async def on_ready(self):
        print("ChatBotPrompts.py is ready")

    @app_commands.command()
    async def prompting_help(self, interaction: discord.Interaction): ...
    
    @commands.cooldown(1, 15, commands.BucketType.user)
    @app_commands.command(
        name="list_models",
        description="List all the models that can be used by prompting",
    )
    async def list_models(self, interaction: discord.Interaction):
        models = {
            "gpt-4o",
            "gpt-4o-2024-05-13",
            "gpt-3.5-turbo",
            "gpt-4-turbo-2024-04-09",
            "gpt-4-turbo-preview",
            "gpt-4-0125-preview",
            "gpt-4-1106-preview",
            "gpt-4",
            "gpt-4-0613",
            "gpt-4-0314",
            "gpt-3.5-turbo-0125",
            "gpt-3.5-turbo",
            "gpt-3.5-turbo-1106",
            "gpt-3.5-turbo-instruct",
        }
        await interaction.response.send_message("\n".join(models))

    @commands.cooldown(1, 15, commands.BucketType.user)
    @app_commands.command(
        name="max_tokens",
        description="lists the max number of context tokens a model can have",
    )
    async def max_tokens(self, interaction: discord.Interaction):
        openAI_max_context = {
            "gpt-4o": 128000,
            "gpt-4o-2024-05-13": 128000,
            "gpt-3.5-turbo": 128000,
            "gpt-4-turbo-2024-04-09": 128000,
            "gpt-4-turbo-preview": 128000,
            "gpt-4-0125-preview": 128000,
            "gpt-4-1106-preview": 128000,
            "gpt-4": 8192,
            "gpt-4-0613": 8192,
            "gpt-4-0314": 8192,
            "gpt-3.5-turbo-0125": 16385,
            "gpt-3.5-turbo": 16385,
            "gpt-3.5-turbo-1106": 16385,
            "gpt-3.5-turbo-instruct": 4096,
        }
        await interaction.response.send_message(
            "\n".join(
                [
                    f"{key}:" + " {:,}".format(int(value))
                    for key, value in openAI_max_context.items()
                ]
            )
        )


async def setup(client):
    await client.add_cog(ChatBotPrompts(client))
