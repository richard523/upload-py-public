import time
from img_gen import generateImage
import os
from dotenv import load_dotenv
import flickrapi
import webbrowser
import asyncio
from typing import Literal, Sequence
import discord
from discord import app_commands
from upload import upload_to_db


intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

load_dotenv()
DISCORD_CLIENT_KEY = os.getenv("DISCORD_CLIENT_KEY")
GUILD_ID = os.getenv("GUILD_ID")
IMG_API_KEY = os.getenv("IMG_API_KEY")
IMG_API_SECRET = os.getenv("IMG_API_SECRET")

flickr = flickrapi.FlickrAPI(IMG_API_KEY, IMG_API_SECRET)



@tree.command(name = "generate", description = "Describe an image for me to generate. WARNING: STABLE DIFFUSION MAY AMPLIFY STEREOTYPES.", guild=discord.Object(id=GUILD_ID)) #Add the guild ids in which the slash command will appear. If it should be in all, remove the argument, but note that it will take some time (up to an hour) to register the command if it's for all guilds.
async def first_command(interaction: discord.Interaction, description: str):
    
    await interaction.response.defer(ephemeral=False)
    generateImage(description)
    send = await interaction.followup.send(f"Completed image generation of... {description}. This program is not responsible for any stereotypes produced.\nRead more here: <https://techpolicy.press/researchers-find-stable-diffusion-amplifies-stereotypes/>", file=discord.File(f"{description}.png"))
    
    # original = await interaction.original_response()
    attachment_url = send.attachments[0].url
    
    print(f"Finished command! \"{description}\" by \"{interaction.user.name}\" #{interaction.user.discriminator} ({interaction.user.id}) time: {time.strftime('%Y-%m-%d %H:%M:%S')} all attachments: {attachment_url}")
    
    print(upload_to_db(attachment_url, description, interaction.user.name, time.strftime('%Y-%m-%d %H:%M:%S'), interaction.user.id))

@client.event
async def on_ready():
    await tree.sync(guild=discord.Object(id=GUILD_ID))
    print("Ready!")

client.run(DISCORD_CLIENT_KEY)
