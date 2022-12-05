#!/usr/bin/env python3

import discord, importlib, sqlite3
from discord import app_commands

# Define global variables we needed:
get_env     = importlib.machinery.SourceFileLoader("env", ".env")
load_env    = get_env.load_module()
token       = load_env.token # Create a file named as ".env" and define "token" variable in the ".env" file.
description = "A beautiful reminder bot for verses from the Qur'an and hadiths"

# verse-hadithDB database locations
database = {
    "tr": "/usr/share/verse-hadith/verse-hadith-tr.db"
}

# Setting up the bot:
class setup_bot(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.default())
        self.synced = False
    
    async def on_ready(self):
        await self.wait_until_ready()
        if not self.synced:
            await tree.sync(guild = None)
            self.synced = True
        print(f'Logged in as {self.user} (ID: {self.user.id})')

bot = setup_bot()
tree = app_commands.CommandTree(bot)

# Bot commands:
@tree.command(name = "test", description=description, guild = None)
async def verse(interaction: discord.Interaction, string: str):
    await interaction.response.send_message(f"şunu mu diyorsun: {string}")

@tree.command(name = "verse", description=description, guild = None)
async def verse(interaction: discord.Interaction):
    db = sqlite3.connect(database["tr"])
    verse = db.execute("SELECT context, source, source_url FROM verse ORDER BY RANDOM() LIMIT(1);")
    verse, source, link = verse.fetchone()
    embed = discord.Embed(title=f"{source}", url=f"{link}", description=f"{verse}", color=discord.Color.green())
    embed.set_image(url="https://www.islamveihsan.com/wp-content/uploads/2016/11/ayet-702x336.jpg")
    await interaction.response.send_message(embed=embed)

@tree.command(name = "hadith", description=description, guild = None)
async def hadith(interaction: discord.Interaction):
    db = sqlite3.connect(database["tr"])
    hadith = db.execute("SELECT context, source, source_url FROM hadith ORDER BY RANDOM() LIMIT(1);")
    hadith, source, link = hadith.fetchone()
    embed = discord.Embed(title=f"{source}", url=f"{link}", description=f"{hadith}", color=discord.Color.green())
    embed.set_image(url="https://www.sanatinyolculugu.com/wp-content/uploads/2019/11/mescid.jpg")
    await interaction.response.send_message(embed=embed)

# Run the bot.
bot.run(token)