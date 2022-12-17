import discord
from discord.ext import commands
import random
import os


import Sigurd_the_Holy_Knight

with open("metal_gear_quote_list.txt", "r") as file:
    metal_gear_quote_list = file.read().split("\n")

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix=commands.when_mentioned_or('!'), intents=intents)


Sigurd_the_Holy_Knight.setup(bot)


@bot.event
async def on_ready():
    print("We have logged in as {0.user}".format(bot))
    for guild in bot.guilds:
        for channel in guild.text_channels:
            if str(channel) == "bot-activation-logs":
                await channel.send("Sigurd the Holy Knight, Lord of Chalphy, has been summoned and awakened. Hereby formally launching crusade against all dastards.")
        print("Active in {}\n Member Count : {}".format(guild.name, guild.member_count))


@bot.event
async def on_member_join(member):
    for channel in member.guild.text_channels:
        if str(channel) == "general":
            on_mobile = False
            if member.is_on_mobile():
                on_mobile = True
            await channel.send(f"Welcome to the Server {member.name}!!\nOn Mobile : {on_mobile}")
            await bot.process_commands(member)
            return

with open("swearing_filter.txt", "r") as file:
    words = file.readline()
    badwords = words.strip().split(",")

#os.chdir("C:/Users/bluet/Downloads/Sigurd_the_Holy_Knight/images_or_gifs")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    for word in badwords:
        if word in message.content.lower():
            await message.delete()
            await message.channel.send("Please don't use profanity, my lord/lady. :angry:")
            # await message.channel.send("", file=discord.File("Sigurds_random_censoring.png"))
            return

    username = str(message.author).split("#")[0]
    print(f"{username}:{message.content}({message.channel.name})")

    if message.content.startswith("!slap"):
        await message.channel.send(f"{message.content[6:]} was slapped by {username}")
        return
    if message.content.lower() == "hello":
        await message.channel.send(f"Hello {username}!")
        input("How are you?" )
        if input() == ["good", "fantastic", "awesome", "great", "ok", "okay", "wonderful", "fine",
                                       "marvelous", "magnificent"]:
            responses = [
                "That's great to hear!",
                "Well then, I hope that your days will always be like so!",
                "I see. I wish you the best of luck!",
                "May fortune smile upon you!"
            ]
            await message.channel.send(random.choices(responses))
            return
        else:
            alternative_responses = [
                                        "A pity. I pray for your health and fortune.",
                                        "If it would comfort you, I will always be here to listen.",
                                        "There is always two sides to everything. Therefore, as you have had bad fortune, there is surely good fortune waiting for you somewhere."
                                        "You have my sympathies. Please take care."
                                    ]
            await message.channel.send(random.choices(alternative_responses))
        return
    elif message.content.lower() == "bye":
        await message.channel.send(f"See you later {username}!")
        return
    elif message.content.lower() == "thank you sigurd":
        await message.channel.send(f"It is my honour to serve you, Lord/Lady {username}.")
        return
    elif message.content.lower() == '!randommetalgearquote':
        random_index = random.randrange(len(metal_gear_quote_list))
        response = metal_gear_quote_list[random_index]
        await message.channel.send(response)
        return
    elif message.content.lower() == '!random':
        response = f'This is your random number: {random.randrange(100)}'
        await message.channel.send(response)
        return
    elif "barbecue" in message.content.lower():
        message_choices = [
                            f"{username}, you dastard!",
                            f"Damn you, {username}!",
                            "AHHHH!!! Damn it!",
                            "I'm sorry, my lord/lady, but please refrain from mentioning barbecues. I may lose my composure."
                           ]
        await message.channel.send(random.choices(message_choices))
        return
    elif "birthday" in message.content.lower():
        await message.channel.send("Happy Birthday!")
        return
    elif message.content.lower() == "eat like snake":
        await message.channel.send("https://www.youtube.com/watch?v=VYn4GE2M_ss")
        return
    await bot.process_commands(message)


@bot.command(help="Prints name of Author")
async def whats_my_name(ctx):
    await ctx.send('Greetings, my lord/lady {}'.format(ctx.author.name))


@bot.command()
async def info(ctx):
    await ctx.send('I am Sigurd, a bot created by bluefire to act as this server\'s administrator. \nCurrently, my performable duties and actions are limited, but bluefire is working hard on developing more features for me. I look forward to serving you, my lords and ladies.')

@bot.command(help="Prints details of Server")
async def where_am_i(ctx):
    owner = str(ctx.guild.owner)
    region = str(ctx.guild.region)
    guild_id = str(ctx.guild.id)
    memberCount = str(ctx.guild.member_count)
    icon = str(ctx.guild.icon_url)
    desc = ctx.guild.description

    embed = discord.Embed(
        title=ctx.guild.name + " Server Information",
        description=desc,
        color=discord.Color.blue()
    )
    embed.set_thumbnail(url=icon)
    embed.add_field(name="Owner", value=owner, inline=True)
    embed.add_field(name="Server ID", value=guild_id, inline=True)
    embed.add_field(name="Region", value=region, inline=True)
    embed.add_field(name="Member Count", value=memberCount, inline=True)

    await ctx.send(embed=embed)

    members = []
    async for member in ctx.guild.fetch_members(limit=150):
        await ctx.send('Name : {}\t Status : {}\n Joined at {}'.format(member.display_name, str(member.status),
                                                                       str(member.joined_at)))


token = ""
bot.run(token)
