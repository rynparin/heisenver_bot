import os
import random
import time
import discord
from discord.ext import commands
import pandas as pd
from TOKEN import TOKEN  # token of bot

client = commands.Bot(command_prefix='$')


@client.event
async def on_ready():
    print("I'm ready now!!")
    print("---------------")


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    elif message.content.startswith('$'):

        cmd = message.content.split()[0].replace("$", "")
        if len(message.content.split()) > 1:
            parameters = message.content.split()[1:]

        # Bot Commands

        if cmd == 'collect':  # collect message

            data = pd.DataFrame(columns=['content'])

            # Acquiring the channel via the bot command
            if len(message.channel_mentions) > 0:
                channel = message.channel_mentions[0]
            else:
                channel = message.channel

            # check number of song to collect
            if (len(message.content.split()) > 1):
                limit = int(parameters[0])
            else:  # set default at 100
                limit = 100

            answer = discord.Embed(title="Creating Sasa's song History Dataframe",
                                   description="Please Wait. The data will be sent to you privately once it's finished.",
                                   colour=0x1a7794)

            await message.channel.send(embed=answer)

            def is_rythm_command(msg):
                if msg.content[:2] == '!p':
                    return True

            def is_sasa_command(msg):
                if msg.author.name == 'Nalinsa':
                    return True

            # The added 1000 is so in case it skips messages for being
            async for msg in channel.history(limit=limit + 1000):
                # collect songs that open from Sasa
                if msg.author != client.user and is_rythm_command(msg) and is_sasa_command(msg):
                    data = data.append(
                        {'content': msg.content, }, ignore_index=True)
                    if len(data) == limit:
                        break

            # Turning the pandas dataframe into a .csv file and sending it to the user
            # Determining file name and location
            if message.author.name == '𝓧𝔂𝓷𝔃':
                file_location = "./data/{}_data.csv".format(
                    time.asctime().replace(' ', '_')).replace(':', '.')
            else:
                file_location = "data.csv"

            data.to_csv(file_location)  # Saving the file as a .csv via pandas

            answer = discord.Embed(title="Here is your .CSV File",
                                   description=f"""It might have taken a while, but here is what you asked for.\n\n`Server` : **{message.guild.name}**\n`Channel` : **{channel.name}**\n`Messages Read` : **{limit}**""",
                                   colour=0x1a7794)

            await message.author.send(embed=answer)
            # Sending the file
            await message.author.send(file=discord.File(file_location, filename='data.csv'))

            if message.author.name != '𝓧𝔂𝓷𝔃':  # if message from me dont delete
                os.remove(file_location)  # Deleting the file

        elif cmd == 'pick':  # pick random song
            return

    await client.process_commands(message)  # allow to use client.command


client.run(TOKEN)
