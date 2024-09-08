from discord import app_commands
from discord.ext import commands
import discord
from utils import gptFunctions, EconomyFunctions


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
        await interaction.response.defer()

        balance = EconomyFunctions.getBalance(
            str(interaction.user.id), interaction.user.name
        )

        if balance < 10:
            await interaction.followup.send(
                "You do not have enough mone to use this command", ephemeral=True
            )
            return
        else:
            EconomyFunctions.setBalance(
                str(interaction.user.id), interaction.user.name, balance - 10
            )

        try:
            if len(message) < 1:
                await interaction.response.send_message("Please provide a query")
                return

            if "gpt" in model:
                response = gptFunctions.perform_gpt_query(query=message, model=model)
            elif "gemini" in model:
                response = gptFunctions.perform_google_query(query=message, model=model)
            elif "claude" in model:
                response = gptFunctions.perform_claude_query(query=message, model=model)
            elif "llama" in model or "mixtral" in model:
                response = gptFunctions.perform_llama_or_mixtral_query(
                    query=message, model=model
                )

            embed = discord.Embed(title="Chatbot Prompt", color=discord.Color.blue())
            embed.set_author(
                name=f"query by {interaction.user.display_name} and response from {model}",
                icon_url=interaction.user.avatar,
            )
            embed.add_field(name="Query", value=message, inline=False)
            # embed.add_field(name="Response", value=response, inline=False)
            response_chunks = [response[i:i+1024] for i in range(0, len(response), 1024)]
            for i, chunk in enumerate(response_chunks):
                embed.add_field(name=f"Response {i+1}", value=chunk, inline=False)
            embed.add_field(name="Remaining Balance", value=balance - 10, inline=False)
            await interaction.followup.send(embed=embed)
        except Exception as e:
            await interaction.followup.send(f"An error occured: {e}", ephemeral=True)

    @app_commands.checks.has_permissions(administrator=True)
    @app_commands.command(name="qotw", description="Get the question of the week")
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def qotw(self, interaction: discord.Interaction, websites: str):
        # https://stackoverflow.com/questions/67249570/how-do-i-mention-everyone-in-discord-py
        await interaction.response.defer()
        try:
            response = await gptFunctions.createQOTW(websites)
            sources = ""
            for source in websites.split(','):
                sources += f"{source.strip()}\n"
            sources = f"Sources: \n{sources}"
            await interaction.followup.send(
                response + "\n\n" + sources,
                allowed_mentions=discord.AllowedMentions(everyone=True),
                suppress_embeds=True,
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
        models = gptFunctions.get_models()
        await interaction.response.send_message("\n".join(models))

    @commands.cooldown(1, 15, commands.BucketType.user)
    @app_commands.command(
        name="max_context",
        description="lists the max number of context tokens a model can have",
    )
    async def max_context(self, interaction: discord.Interaction):
        context = gptFunctions.get_input_contexts()
        await interaction.response.send_message(
            "\n".join(f"{key}: {value}" for key, value in context.items())
        )

    @commands.cooldown(1, 15, commands.BucketType.user)
    @app_commands.command(
        name="max_output",
        description="lists the max number of output tokens a model can have",
    )
    async def max_output(self, interaction: discord.Interaction):
        output = gptFunctions.get_output_contexts()
        await interaction.response.send_message(
            "\n".join(f"{key}: {value}" for key, value in output.items())
        )


async def setup(client):
    await client.add_cog(ChatBotPrompts(client))
