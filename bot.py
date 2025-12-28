import discord
from discord import app_commands
from discord.ext import commands
import os
from dotenv import load_dotenv

# Import your custom logic from your GitHub repo files
from logic.tug_of_war import calculate_tug_of_war
from logic.humanity_audit import run_audit

# Load environment variables
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

class DovicBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):
        # This syncs your slash commands with Discord
        await self.tree.sync()
        print(f"Synced slash commands for {self.user}")

bot = DovicBot()

@bot.event
async def on_ready():
    print(f'DOVIC System Online. Logged in as {bot.user}')
    # Set the bot's status to show the current Zone
    await bot.change_presence(activity=discord.Game(name="Zone 0: Mainframe Terminal"))

# --- SLASH COMMANDS (The Player's Tools) ---

@bot.tree.command(name="audit", description="Run a Humanity Audit to check for PADOOS bias.")
async def audit(interaction: discord.Interaction):
    await interaction.response.defer() # Give the bot time to talk to Firebase
    
    # Run the logic from your humanity_audit.py
    result_msg = run_audit(interaction.user.id)
    
    # Update the Tug-of-War pole
    new_integrity, tug_msg = calculate_tug_of_war("GRANT_HUMANITY_AUDIT", 10)
    
    # Create the Visual Embed for the "Tug-of-War"
    embed = discord.Embed(title="⚠️ System Integrity Report", color=discord.Color.blue())
    embed.add_field(name="Audit Result", value=result_msg, inline=False)
    embed.add_field(name="Humanity Index", value=f"{new_integrity}%", inline=True)
    embed.set_footer(text=tug_msg)
    
    await interaction.followup.send(embed=embed)

@bot.tree.command(name="padoos_status", description="Check the current PADOOS logistics priority.")
async def status(interaction: discord.Interaction):
    # This would pull directly from your Firebase 'System_Logic'
    await interaction.response.send_message("🔍 `PADOOS Status: BIAS_DETECTED. Priority: CORPORATE_TIER.`")

bot.run(TOKEN)
