import os
import random
import discord
from discord.ext import commands
import pandas as pd
from TOKEN import TOKEN

client = commands.Bot(command_prefix='$')


@client.event
async def on_ready():
    print("I'm online now!!")
    print(" --------------")


@client.command()
async def hello(ctx):
    await ctx.send('Hello!')


@client.command(pass_context=True)
async def join(ctx):
    if (ctx.author.voice):
        channel = ctx.message.author.voice.channel
        await channel.connect()
    else:
        await ctx.send('You are not in the channel!')


@client.command(pass_context=True)
async def leave(ctx):
    if (ctx.voice_client):
        await ctx.guild.voice_client.disconnect()
    else:
        await ctx.send("I'm not in the channel!!")

# collect messages


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    elif message.content.startswith('_'):

        cmd = message.content.split()[0].replace("_", "")
        if len(message.content.split()) > 1:
            parameters = message.content.split()[1:]

        # Bot Commands

        if cmd == 'scan':

            data = pd.DataFrame(columns=['content', 'time', 'author'])

            # Acquiring the channel via the bot command
            if len(message.channel_mentions) > 0:
                channel = message.channel_mentions[0]
            else:
                channel = message.channel

            # Aquiring the number of messages to be scraped via the bot command
            if (len(message.content.split()) > 1 and len(message.channel_mentions) == 0) or len(message.content.split()) > 2:
                for parameter in parameters:
                    if parameter == "help":
                        answer = discord.Embed(title="Command Format",
                                               description="""`_scan <channel> <number_of_messages>`\n\n`<channel>` : **the channel you wish to scan**\n`<number_of_messages>` : **the number of messages you wish to scan**\n\n*The order of the parameters does not matter.*""",
                                               colour=0x1a7794)
                        await message.channel.send(embed=answer)
                        return
                    elif parameter[0] != "<":  # Channels are enveloped by "<>" as strings
                        limit = int(parameter)
            else:
                limit = 100

            answer = discord.Embed(title="Creating your Message History Dataframe",
                                   description="Please Wait. The data will be sent to you privately once it's finished.",
                                   colour=0x1a7794)

            await message.channel.send(embed=answer)

            def is_command(message):
                if len(msg.content) == 0:
                    return False
                elif msg.content.split()[0] == '_scan':
                    return True
                else:
                    return False

            # The added 1000 is so in case it skips messages for being
            async for msg in channel.history(limit=limit + 1000):
                # a command or a message it sent, it will still read the
                if msg.author != client.user:
                    # the total amount originally specified by the user.
                    if not is_command(msg):
                        data = data.append({'content': msg.content,
                                            'time': msg.created_at,
                                            'author': msg.author.name}, ignore_index=True)
                    if len(data) == limit:
                        break

            # Turning the pandas dataframe into a .csv file and sending it to the user

            # Determining file name and location
            file_location = f"{str(channel.guild.id) + '_' + str(channel.id)}.csv"
            data.to_csv(file_location)  # Saving the file as a .csv via pandas

            answer = discord.Embed(title="Here is your .CSV File",
                                   description=f"""It might have taken a while, but here is what you asked for.\n\n`Server` : **{message.guild.name}**\n`Channel` : **{channel.name}**\n`Messages Read` : **{limit}**""",
                                   colour=0x1a7794)

            await message.author.send(embed=answer)
            # Sending the file
            await message.author.send(file=discord.File(file_location, filename='data.csv'))
            os.remove(file_location)  # Deleting the file
    await client.process_commands(message)  # allow to use client.command

client.run(TOKEN)
