from discord.ext import commands
import discord
from discord import app_commands
import json
from utils import EconomyFunctions

class Economy(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
        super().__init__()

    @commands.Cog.listener()
    async def on_ready(self):
        print("Economy.py is ready")

    @app_commands.command(name="balance", description="Check your balance")
    async def balance(self, interaction: discord.Interaction):
        await interaction.response.defer()
        print("debug: balance command called")
        with open("userData.json", "r") as f:
            data = json.load(f)
            print(f"debug: data loaded {str(data)}")
        print(f"interaction id: {interaction.user.id}")
        print(f"debug: member {interaction.user.id}")
        member = interaction.user.id
        
        if str(member) not in data:
            
            print("debug: member not in data")
            data[str(member)] = {}
            data[str(member)]["name"] = interaction.user.name
            data[str(member)]["balance"] = 100
            
            with open ("userData.json", "w") as f:
                json.dump(data, f, indent=4)
                print("debug: member added to data")
                
        # set the name:
        data[str(member)]["name"] = interaction.user.name
        print("debug: member in data")            
        embed = discord.Embed(title=f"Balance for {interaction.user.name}", description="Current balance for user",color=discord.Color.blue())
        embed.add_field(name="Balance", value=data[str(member)]["balance"], inline=False)
        embed.set_thumbnail(url=interaction.user.avatar)
        print("debug: balance command sending message")
        await interaction.followup.send(embed=embed, ephemeral=True)
        print("debug: balance command finished")
        
    @app_commands.checks.has_permissions(administrator=True)
    @app_commands.command(name="restoreallbalances", description="restore values to all balances")
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def restoreAllBalances(self, interaction: discord.Interaction, value: int):
        with open("userData.json", "r") as f:
            data = json.load(f)
            
        for key in data:
            data[key]["balance"] = value
            
        with open("userData.json", "w") as f:
            json.dump(data, f, indent=4)
            
        await interaction.response.send_message("All balances have been restored")
        
    @app_commands.checks.has_permissions(administrator=True)
    @app_commands.command(name="setuservalue", description="restore one user's balance")
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def setUserValue(self, interaction: discord.Interaction, member: discord.Member, value: int):
        EconomyFunctions.setBalance(member.id, member.name, value)
        await interaction.response.send_message(f"User {member.name} now has a balance of {value}")


async def setup(client):
    await client.add_cog(Economy(client))
