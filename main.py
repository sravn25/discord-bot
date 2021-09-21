import discord
import os
import requests 
import json
from dotenv import load_dotenv
# from discord.ext import commands, tasks


client = discord.Client()
load_dotenv()

greetings = ["hi", "hey", "hello", "ello", "yo"]

def get_post(s):
    while True:
        response = requests.get(f"https://meme-api.herokuapp.com/gimme/{s}")
        json_data = json.loads(response.content)
        if json_data["nsfw"] != "false" and json_data["spoiler"] != "false":
            return {
                "link"   : json_data["postLink"],
                "sub"    : json_data["subreddit"],
                "title"  : json_data["title"],
                "author" : json_data["author"],
                "image"  : json_data["preview"][-1],
                }

@client.event 
async def on_ready():
    # Watching Status
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="penguins"))
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return 

    if message.content.startswith("wtf"):
        await message.channel.send("yea wtf")

    if message.content.lower() in greetings:
        await message.channel.send("shut up idiot")

    if message.content.startswith("wholesome"):
        meme = get_post("wholesomememes")
        embed = discord.Embed(title = meme["title"], description = meme["link"], color = discord.Color.blue())
        embed.add_field(name = "author", value = "u/" + meme["author"], inline = True)
        embed.add_field(name = "subreddit", value = "r/" + meme["sub"], inline = True)
        embed.set_image(url = meme["image"])

        await message.channel.send(embed = embed)

    if message.content.startswith("blessed"):
        meme = get_post("blessedimages")
        embed = discord.Embed(title = meme["title"], description = meme["link"], color = discord.Color.blue())
        embed.add_field(name = "author", value = "u/" + meme["author"], inline = True)
        embed.add_field(name = "subreddit", value = "r/" + meme["sub"], inline = True)
        embed.set_image(url = meme["image"])

        await message.channel.send(embed = embed)

    
client.run(os.getenv("DISCORD_TOKEN"))