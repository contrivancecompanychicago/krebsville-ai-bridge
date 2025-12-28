@bot.event
async def on_ready():
    await bot.tree.sync(guild=discord.Object(id=YOUR_SERVER_ID))
    print(f"Logged in as {bot.user}. Zone 0 Commands Synced!")
