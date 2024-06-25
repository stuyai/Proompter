import discord
from discord.ext import commands, tasks
import random


class Status(commands.Cog):
    def __init__(self, client):
        self.client = client

    @tasks.loop(seconds=10)
    async def change_status(self):
        await self.client.change_presence(
            activity=discord.Game(
                f"Here's a fake random number: {int(random.random()*100) + 1}"
            )
        )

    @commands.Cog.listener()
    async def on_ready(self):
        print("Status.py is ready")


async def setup(client):
    await client.add_cog(Status(client))
