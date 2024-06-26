import discord
from discord.ext import commands

import asyncio

# for tokens
import dotenv
import os


dotenv.load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

client = commands.Bot(command_prefix="!", intents=discord.Intents.all())


@client.event
async def on_ready():
    await client.tree.sync()
    print("Bot is ready")


#  load cogs
async def load_cogs():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await client.load_extension(f"cogs.{filename[:-3]}")

# error handling
@client.event
async def on_command_error(ctx, error):
    await ctx.send(f"Sorry, but there was an error: {error}")


async def main():
    async with client:
        await load_cogs()
        await client.start(TOKEN)


asyncio.run(main())
