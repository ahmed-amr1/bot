import time
from nextcord import emoji
from nextcord.components import SelectOption
from nextcord.ext.commands.errors import BadArgument
from nextcord.ui.select import Select
begin = time.time()
import nextcord
from nextcord.ext import commands,tasks
from nextcord.ui import button,View,Button
from nextcord.interactions import Interaction
from nextcord.ext import menus
import os
#os.system("mode 50,20 & title Schtabtag")
import wikipedia as wiki_module
import datetime
import platform
import random
import urllib.request
import re
import discord
from fractions import Fraction
import math
from io import BytesIO
from typing import Union, Optional
from petpetgif import petpet as petpetgif
import sys
import translators as ts
from itertools import cycle
from colorama import Fore, Back, Style
import dislash
from dislash import InteractionClient, Option, OptionChoice
#import json

def cls():
    if platform.system() == "Linux" or platform.system() == "Darwin":
        os.system("clear")
    if platform.system() == "Windows":
        os.system("cls")

ownerID = 819652262993461279
official_guild_id = 888211482184134778

token = "ODIzMjMxODY4MzI4NzM4ODI2.YFd0bA.RDDz2YW4MRs4pikkiSMgh31U_nw"
color = 0xAC27FA
intents = nextcord.Intents.all()

client = commands.Bot(command_prefix=".",intents=intents)
slash = InteractionClient(client,test_guilds=[official_guild_id],modify_send=False)

statuses = cycle(["with {member_count} members","in {server_count} servers",".help","with Ahmed Amr#5544"])

@tasks.loop(seconds=12)
async def change_status():
    await client.wait_until_ready()
    status = next(statuses)
    if status.startswith("with ") and status.endswith("members"):
        status = status.format(member_count=len(client.users))
    if status.startswith("in ") and status.endswith("servers"):
        status = status.format(server_count=len(client.guilds))
    await client.change_presence(status=nextcord.Status.idle,activity=nextcord.Game(status))

@client.event
async def on_ready():
    channel = client.get_channel(916091369787899924)
    em = nextcord.Embed(title="Schtabtag has just started!",description=f"You can now interact freely with {client.user.mention}!",timestamp=datetime.datetime.utcnow(),color=0xAC27FA)
    em.timestamp = datetime.datetime.utcnow()
    em.set_thumbnail(url=client.user.display_avatar.url)
    await channel.send(embed=em)
    cls()
    print(f'{Fore.MAGENTA}{client.user} is ready!')
    response = time.time() - begin
    print(f'{Fore.CYAN}Took {"{:.2f}".format(response)}sec to start.{Style.RESET_ALL}\n...\n')
    if not change_status.is_running():
        change_status.start()

class view(View):
    def __init__(self):
        super().__init__(timeout=None)
    
    @button(label="0",custom_id="counter button",style=nextcord.ButtonStyle.primary)
    async def counter(self,button : Button,interaction : Interaction):
        label = int(button.label)
        label += 1

        button.label = str(label)

        await interaction.response.edit_message(view = self)

class selfrole(View):
    def __init__(self):
        super().__init__(timeout=None)
    @button(label="Annoncements role",custom_id="ann button",style=nextcord.ButtonStyle.primary)
    async def ann(self,button : Button,interaction : Interaction):
        role = interaction.guild.get_role(916100172000399481)
        if role in interaction.user.roles:
            await interaction.user.remove_roles(role)
            await interaction.response.send_message(f"The {role.mention} role has been removed from your roles",ephemeral=True)
        else:
            await interaction.user.add_roles(role)
            await interaction.response.send_message(f"The {role.mention} role has been added to your roles",ephemeral=True)


role_dict = {
    "role":"",
    "emoji":"",
    "label":"",
}

@client.command()
async def react_role(ctx,label,emoji,roles,*,message:str):
    em = nextcord.Embed(title="React to get roles",description=message,color=color,timestamp=datetime.datetime.utcnow())
    role_dict = {
        "role":roles,
        "emoji":emoji,
        "label":label
    }
    await ctx.send(embed=em,view = role())

@client.command()
async def self_roles(ctx):
    if ctx.guild.id == official_guild_id and ctx.channel.id == 908780161040805888:
        await ctx.send("Select your roles:",view=selfrole())
    elif ctx.guild.id == official_guild_id and ctx.channel.id != 908780161040805888:
        channel = ctx.guild.get_channel(908780161040805888)
        await ctx.send(f"Please use this command in {channel.mention}")
    elif ctx.guild.id != official_guild_id:
        await ctx.send("Sorry but this command is exclusive for Schtabtag's bot server")

@client.command()
async def count(ctx):
    await ctx.send("Count",view = view())

@slash.slash_command(name="test",description="this is a test command")
async def hi(ctx):
    await ctx.send("yep slash commands are working",ephemeral=True,view=view())

@client.command()
async def pet(ctx, image: Optional[Union[nextcord.PartialEmoji, nextcord.member.Member]]):
    if type(image) == nextcord.PartialEmoji:
        image = await image.read() # retrieve the image bytes
    elif type(image) == nextcord.member.Member:
        image = await image.display_avatar.with_format('png').read() # retrieve the image bytes
    else:
        await ctx.reply('Please use a custom emoji or mention a member to petpet their avatar.')
        return

    source = BytesIO(image) # file-like container to hold the emoji in memory
    dest = BytesIO() # container to store the petpet gif in memory
    petpetgif.make(source, dest)
    dest.seek(0) # set the file pointer back to the beginning so it doesn't upload a blank file.
    await ctx.send(file=nextcord.File(dest, filename=f"{image[0]}-petpet.gif"))
    await ctx.send(embed=nextcord.Embed(title="hehe").set_image(url=dest))

@client.event
async def on_message(msg):
    if msg.content == "<@!823231868328738826>" or msg.content == "<@823231868328738826>" or msg.content == "@Schtabtag#4097" or msg.content == "@Schtabtag":
        respond = ["Yes?","What?","Don't mention me again","I'm here"]
        await msg.reply(random.choice(respond))
    if msg.content == "CLS" and msg.author.id == ownerID:
        cls()
    if msg.content.startswith("code:\n```py") and msg.content.endswith("```"):
        mssg = msg.content[12:-4].replace("\n",",")
        await msg.channel.send(mssg)
        try:
            try:
                await eval(mssg)
            except Exception as e:
                await msg.channel.send(e)
        except:
            try:
                eval()
            except Exception as e:
                await msg.channel.send(e)
    await client.process_commands(msg)

@client.command()
async def ping(ctx):
    await ctx.send(f"Pong! in {round(client.latency * 1000)}ms.")
    print(client.user.mention)

@client.command(aliases=['wiki'])
async def wikipedia(ctx,amount_of_sentences_to_search_for,*,search_query : str):
    wiki_module.set_lang("en")

    search = nextcord.Embed(title="Wikpedia",description="Searching...",color=0xAC27FA,timestamp=datetime.datetime.utcnow())

    msg = await ctx.send(embed=search)

    try:
        em = nextcord.Embed(title="Wikipedia",description=f"{wiki_module.summary(search_query,sentences=amount_of_sentences_to_search_for)}",color=0xAC27FA,timestamp=datetime.datetime.utcnow())
        em.set_thumbnail(url="https://media.discordapp.net/attachments/893417057541050368/913832653927616562/2244px-Wikipedia-logo-v2.svg.png")
    except:
        em = nextcord.Embed(title="Wikipedia",description=f"Couldn't find any result of that.",color=0xAC27FA,timestamp=datetime.datetime.utcnow())
    em.set_footer(text=f"Requested by {ctx.author}",icon_url=ctx.author.display_avatar.url)
    await msg.edit(embed=em)

@client.command(aliases=['av','pf'])
async def avatar(ctx,*,member : commands.MemberConverter=None):
    avatar = None
    username = None
    if member == None:
        avatar = ctx.author.display_avatar.url
        username = ctx.author.name
    else:
        avatar = member.display_avatar.url
        username = member.name
    em = nextcord.Embed(title=f'{username}\'s avatar',timestamp=datetime.datetime.utcnow(),color=0xAC27FA,url=avatar)
    em.set_image(url=avatar)
    em.set_footer(text=f"Requested by {ctx.author}",icon_url=ctx.author.display_avatar.url)
    await ctx.send(embed=em)

responds = ['It is certain.','It is decidedly so.','Without a doubt.','Yes definitely.','You may rely on it.','As I see it, yes.','Most likely.','Outlook good.','Yes.','Signs point to yes.','Reply hazy, try again.','Ask again later.','Better not tell you now.','Cannot predict now.','Concentrate and ask again.','Don\'t count on it.','My reply is no.','My sources say no.','Outlook not so good.','Very doubtful.']

@client.command(aliases=['8ball','eightBall'])
async def eightball(ctx,*,question : str=None):
    if question == None:
        await ctx.send("Please specify a question.")
    else:
        await ctx.send(f"{random.choice(responds)}")

@client.command(aliases=['math','maths','calc'])
async def calculate(ctx,*,equation:str):
    try:
        dict = {
                "pi":math.pi,
                "root":math.sqrt,
                "squareroot":math.sqrt,
                "sqrt":math.sqrt,
                "degrees":math.degrees,
                "radians":math.radians,
                "sin":math.sin,
                "cos":math.cos,
                "tan":math.tan,
                "asin":math.asin,
                "acos":math.acos,
                "atan":math.atan,
                "pow":math.pow,
                "power":math.pow,
                "fract":Fraction,
                "ratio":Fraction,
                "fraction":Fraction
              }
        problem = equation
        problem = problem.replace("^","**")
        problem = problem.replace(":","/")
        solve = str(eval(problem,dict))
        em = nextcord.Embed(title="Problem",description=f"```py\n{equation}\n```",color=0xAC27FA,timestamp=datetime.datetime.utcnow())
        em.add_field(name="Solve",value=f" ```py\n{solve}\n```")
    except Exception as e:
        print(e)
        em = nextcord.Embed(title="Calculator",description=f"Couldn't solve that.",color=0xAC27FA,timestamp=datetime.datetime.utcnow())
        em.add_field(name="Error",value=f"```py\n{e}\n```")
    em.set_footer(text=f"Requested by {ctx.author}",icon_url=ctx.author.display_avatar.url)
    await ctx.send(embed=em)

@client.command()
async def say(ctx,*,text):
    await ctx.send(text)

class CustomEmojiButtonMenuPages(menus.ButtonMenuPages,inherit_buttons=False):
    def __init__(self, source, timeout=60):
        super().__init__(source, timeout=timeout)

        self.add_item(menus.MenuPaginationButton(emoji=self.FIRST_PAGE, label="First"))
        self.add_item(menus.MenuPaginationButton(emoji=self.PREVIOUS_PAGE, label="Prev"))
        self.add_item(menus.MenuPaginationButton(emoji=self.NEXT_PAGE, label="Next"))
        self.add_item(menus.MenuPaginationButton(emoji=self.LAST_PAGE, label="Last"))

        self.children = [self.children[1] , self.children[2] , self.children[0] , self.children[3] , self.children[4]]

        self._disable_unavailable_buttons()

    @nextcord.ui.button(label="stop",emoji='⏹')
    async def on_stop(self, button, interaction):
        self.stop()

class MySource(menus.ListPageSource):
    def __init__(self, data):
        super().__init__(data, per_page=1)
        self.total = 0
    async def format_page(self, menu, entries):
        if menu.current_page == 0:
            self.total = len(entries) + 1
        offset = menu.current_page * self.per_page
        export = ''.join(f"{entries}")
        page = f"`{menu.current_page+1}/{self.get_max_pages()}`"
        return f"`{page}`\n{export}"


@client.command(aliases=['yt'])
async def youtube(ctx,*,search_query:str=None):
    html = urllib.request.urlopen(f"https://www.youtube.com/results?search_query={search_query}".replace(" ","%20"))
    video_ids = re.findall(r"watch\?v=(\S{11})",html.read().decode())
    videos = []
    for id in video_ids:
        videos.append(f'https://www.youtube.com/watch?v={id}')
    pages = CustomEmojiButtonMenuPages(source=MySource(list(videos)))
    await pages.start(ctx)

class inv(View):
    def __init__(self):
        super().__init__(timeout=None)
        url = "https://bit.ly/schtabtag"
        self.add_item(nextcord.ui.Button(label='Invite', url=url))

@client.command(aliases=['inv'])
async def invite(ctx):
    em = nextcord.Embed(title="Invite Schtabtag",url="https://bit.ly/schtabtag",description="**`Invite Schtabtag to your Discord server and enjoy all the bot features!`**",color=0xAC27FA,timestamp=datetime.datetime.utcnow())
    em.set_thumbnail(url=client.user.display_avatar.url)
    em.set_footer(text=f"Requested by {ctx.author}",icon_url=ctx.author.display_avatar.url)
    await ctx.send(embed=em,view = inv())

class Dropdown(Select):
    def __init__(self):
        SelectOptions = [
            SelectOption(label = "Egypt",description="Africa",emoji="🇪🇬"),
            SelectOption(label = "Spain",description="Europe",emoji="🇪🇸"),
            SelectOption(label = "Germany",description="Europe",emoji="🇩🇪")
        ]
        super().__init__(placeholder="Select your country",min_values=1,max_values=1,options=SelectOptions)
    async def callback(self,interaction:nextcord.Interaction):
        if self.values[0] == "Egypt":
            return await interaction.response.send_message("You are now Egyptian",ephemeral=True)
        if self.values[0] == "Spain":
            return await interaction.response.send_message("You are now Spanish",ephemeral=True)
        if self.values[0] == "Germany":
            return await interaction.response.send_message("You are now German",ephemeral=True)

class DropdownView(View):
    def __init__(self):
        super().__init__()
        self.add_item(Dropdown())

@client.command()
async def country(ctx):
    view = DropdownView()
    await ctx.send("Choose your country ",view=view)

@client.command(aliases=["length","len"])
async def measure(ctx,*,text_to_be_measured=None):
    if text_to_be_measured==None:
        await ctx.send("Please provide text to be measured")
    else:
        await ctx.reply(f"Text : `{text_to_be_measured}`\nThe number of characters in the text : `{len(text_to_be_measured)}`")

@client.command(aliases=['cl','purge','delete','remove'])
@commands.has_permissions(manage_messages=True)
async def clear(ctx,amount_of_messages_to_be_deleted:int=1):
    await ctx.channel.purge(limit=amount_of_messages_to_be_deleted+1)

@clear.error
async def clear_error(ctx: commands.Context, error: commands.CommandError):
    """Handle errors for the clear command."""

    if isinstance(error, commands.CommandOnCooldown):
        message = f"This command is on cooldown. Please try again after {round(error.retry_after, 1)} seconds."
    elif isinstance(error, commands.MissingPermissions):
        message = "You are missing the required permissions to run this command!"
    elif isinstance(error, commands.MissingRequiredArgument):
        message = f"Missing a required argument: {error.param}"
    elif isinstance(error, commands.ConversionError):
        message = str(error)
    else:
        message = "Oh no! Something went wrong while running the command!"

    await ctx.reply(message, delete_after=6)
    await ctx.message.delete(delay=6)

@wikipedia.error
async def wikipedia_error(ctx: commands.Context, error: commands.CommandError):
    """Handle errors for the wikipedia command."""

    if isinstance(error, commands.CommandOnCooldown):
        message = f"This command is on cooldown. Please try again after {round(error.retry_after, 1)} seconds."
    elif isinstance(error, commands.MissingPermissions):
        message = "You are missing the required permissions to run this command!"
    elif isinstance(error, commands.MissingRequiredArgument):
        message = f"Missing a required argument: {error.param}"
    elif isinstance(error, commands.ConversionError):
        message = str(error)
    else:
        message = "Oh no! Something went wrong while running the command!"

    await ctx.reply(message, delete_after=6)
    await ctx.message.delete(delay=6)


@slash.slash_command(name="wikipedia",description="Searches for a specific argument in wikipedia",options=[Option(name="argument",description="The argument which will be searched for in wikipedia",required=True),Option(name="sentences",description="The number of sentences to search for",required=False),Option(name="language",description="The language to search in",required=False,choices=[
                OptionChoice(
                    name="English - English",
                    value="en"
                ),
                OptionChoice(
                    name="German - Deutsch",
                    value="de"
                ),
                OptionChoice(
                    name="Arabic - عربي",
                    value="ar"
                ),
                OptionChoice(
                    name="Spanish - español, castellano",
                    value="es"
                ),
                OptionChoice(
                    name="Russian - русский",
                    value="ru"
                ),
                OptionChoice(
                    name="Polish - Polski",
                    value="pl"
                ),
                OptionChoice(
                    name="Italian - Italiano",
                    value="it"
                ),
                OptionChoice(
                    name="Japanese - 日本語",
                    value="ja"
                ),
                OptionChoice(
                    name="Irish - Gaeilge",
                    value="ga"
                ),
                OptionChoice(
                    name="Hindi - हिन्दी, हिंदी",
                    value="hi"
                ),
                OptionChoice(
                    name="Hebrew - עברית",
                    value="he"
                ),
                OptionChoice(
                    name="French - Français",
                    value="fr"
                ),
                OptionChoice(
                    name="Dutch - Nederlands",
                    value="nl"
                ),
                OptionChoice(
                    name="Czech - česky, čeština",
                    value="cs"
                ),
                OptionChoice(
                    name="Danish - Dansk",
                    value="da"
                ),
                OptionChoice(
                    name="Chinese - 中文, Zhōngwén",
                    value="zh"
                ),
                OptionChoice(
                    name="Persian - فارسی",
                    value="fa"
                )
            ]
        )
    ])

async def wiki(ctx,argument,sentences=1,language="en"):
    wiki_module.set_lang(language)
    search = discord.Embed(title="Wikpedia",description="Searching...",color=0xAC27FA,timestamp=datetime.datetime.utcnow())

    msg = await ctx.send(embed=search)

    try:
        em = discord.Embed(title="Wikipedia",description=f"{wiki_module.summary(argument,sentences=sentences)}",color=0xAC27FA,timestamp=datetime.datetime.utcnow())
        em.set_thumbnail(url="https://media.discordapp.net/attachments/893417057541050368/913832653927616562/2244px-Wikipedia-logo-v2.svg.png")
    except:
        em = discord.Embed(title="Wikipedia",description=f"Couldn't find any result of that.",color=0xAC27FA,timestamp=datetime.datetime.utcnow())
    em.set_footer(text=f"Requested by {ctx.author.name}",icon_url=ctx.author.avatar.url)
    await msg.edit(embed=em)

@slash.slash_command(name="translate",description="Translates the passed argument into the passed language (Default:English)",options=[Option(name="argument",description="The argument which will be translated",required=True),Option(name="source",description="The language which the argument will be translated from",required=False,choices=[
                OptionChoice(
                    name="Auto detect language",
                    value="auto"
                ),
                OptionChoice(
                    name="English - English",
                    value="en"
                ),
                OptionChoice(
                    name="German - Deutsch",
                    value="de"
                ),
                OptionChoice(
                    name="Arabic - عربي",
                    value="ar"
                ),
                OptionChoice(
                    name="Spanish - español, castellano",
                    value="es"
                ),
                OptionChoice(
                    name="Russian - русский",
                    value="ru"
                ),
                OptionChoice(
                    name="Polish - Polski",
                    value="pl"
                ),
                OptionChoice(
                    name="Italian - Italiano",
                    value="it"
                ),
                OptionChoice(
                    name="Japanese - 日本語",
                    value="ja"
                ),
                OptionChoice(
                    name="Irish - Gaeilge",
                    value="ga"
                ),
                OptionChoice(
                    name="Hindi - हिन्दी, हिंदी",
                    value="hi"
                ),
                OptionChoice(
                    name="Hebrew - עברית",
                    value="he"
                ),
                OptionChoice(
                    name="French - Français",
                    value="fr"
                ),
                OptionChoice(
                    name="Dutch - Nederlands",
                    value="nl"
                ),
                OptionChoice(
                    name="Czech - česky, čeština",
                    value="cs"
                ),
                OptionChoice(
                    name="Danish - Dansk",
                    value="da"
                ),
                OptionChoice(
                    name="Chinese - 中文, Zhōngwén",
                    value="zh"
                ),
                OptionChoice(
                    name="Persian - فارسی",
                    value="fa"
                )
            ]),Option(name="dest",description="The language which the argument will be translated to",required=False,choices=[
                OptionChoice(
                    name="English - English",
                    value="en"
                ),
                OptionChoice(
                    name="German - Deutsch",
                    value="de"
                ),
                OptionChoice(
                    name="Arabic - عربي",
                    value="ar"
                ),
                OptionChoice(
                    name="Spanish - español, castellano",
                    value="es"
                ),
                OptionChoice(
                    name="Russian - русский",
                    value="ru"
                ),
                OptionChoice(
                    name="Polish - Polski",
                    value="pl"
                ),
                OptionChoice(
                    name="Italian - Italiano",
                    value="it"
                ),
                OptionChoice(
                    name="Japanese - 日本語",
                    value="ja"
                ),
                OptionChoice(
                    name="Irish - Gaeilge",
                    value="ga"
                ),
                OptionChoice(
                    name="Hindi - हिन्दी, हिंदी",
                    value="hi"
                ),
                OptionChoice(
                    name="Hebrew - עברית",
                    value="he"
                ),
                OptionChoice(
                    name="French - Français",
                    value="fr"
                ),
                OptionChoice(
                    name="Dutch - Nederlands",
                    value="nl"
                ),
                OptionChoice(
                    name="Czech - česky, čeština",
                    value="cs"
                ),
                OptionChoice(
                    name="Danish - Dansk",
                    value="da"
                ),
                OptionChoice(
                    name="Chinese - 中文, Zhōngwén",
                    value="zh"
                ),
                OptionChoice(
                    name="Persian - فارسی",
                    value="fa"
                )
            ]
        )
    ])

async def translate(ctx,argument,source="auto",dest="en"):
    try:
        src = source
        dst = dest
        search = discord.Embed(title="Translating...",description="```py\n\"Please wait...\"```",color=0xAC27FA,timestamp=datetime.datetime.utcnow())
        msg = await ctx.send(embed=search)
        if src == "auto":
            src = "Auto detect language"
        if src == "en":
            src = "English - English"
        if src == "de":
            src = "German - Deutsch"
        if src == "ar":
            src = "Arabic - عربي"
        if src == "es":
            src = "Spanish - español, castellano"
        if src == "ru":
            src = "Russian - русский"
        if src == "pl":
            src = "Polish - Polski"
        if src == "it":
            src = "Italian - Italiano"
        if src == "ja":
            src = "Japanese - 日本語"
        if src == "ga":
            src = "Irish - Gaeilge"
        if src == "hi":
            src = "Hindi - हिन्दी, हिंदी"
        if src == "he":
            src = "Hebrew - עברית"
        if src == "fr":
            src = "French - Français"
        if src == "nl":
            src = "Dutch - Nederlands"
        if src == "cs":
            src = "Czech - česky, čeština"
        if src == "da":
            src = "Danish - Dansk"
        if src == "zh":
            src = "Chinese - 中文, Zhōngwén"
        if src == "fa":
            src = "Persian - فارسی"
        if dst == "en":
            dst = "English - English"
        if dst == "de":
            dst = "German - Deutsch"
        if dst == "ar":
            dst = "Arabic - عربي"
        if dst == "es":
            dst = "Spanish - español, castellano"
        if dst == "ru":
            dst = "Russian - русский"
        if dst == "pl":
            dst = "Polish - Polski"
        if dst == "it":
            dst = "Italian - Italiano"
        if dst == "ja":
            dst = "Japanese - 日本語"
        if dst == "ga":
            dst = "Irish - Gaeilge"
        if dst == "hi":
            dst = "Hindi - हिन्दी, हिंदी"
        if dst == "he":
            dst = "Hebrew - עברית"
        if dst == "fr":
            dst = "French - Français"
        if dst == "nl":
            dst = "Dutch - Nederlands"
        if dst == "cs":
            dst = "Czech - česky, čeština"
        if dst == "da":
            dst = "Danish - Dansk"
        if dst == "zh":
            dst = "Chinese - 中文, Zhōngwén"
        if dst == "fa":
            dst = "Persian - فارسی"
        em = discord.Embed(title="Translator",
        description=f"From ({src}) To ({dst})",color=0xAC27FA,timestamp=datetime.datetime.utcnow())
        em.add_field(name="Source text",value=f"```py\n\"{argument}\"```",inline=False)
        em.set_thumbnail(url="https://media.discordapp.net/attachments/893417057541050368/916290939893448714/Google_Translate_Icon.png")
        em.add_field(inline=False,name="Translated text",value=f"```py\n\"{ts.google(argument,to_language=dest,from_language=source)}\"```")
        em.set_footer(text=f"Requested by {ctx.author.name}",icon_url=ctx.author.avatar.url)
        await msg.edit(embed=em)
    except:
        em = discord.Embed(description="Please check your arguments again.\nSyntax `trans src-lang dest-lang text`\nYou can read language abbreviations from [here](https://pastebin.com/PrxskfGq).",color=0xAC27FA,timestamp=datetime.datetime.utcnow())
        em.set_footer(text=f"Requested by {ctx.author.name}",icon_url=ctx.author.avatar.url)
        await msg.edit(embed=em)

@slash.slash_command(
    name="embed",
    description="Returns an embed",
    options=[
        Option(
            name="title",
            description="The title of the embed",
            required=True,
        ),
        Option(
            name="description",
            description="The description of the embed",
            required=False,
        ),
        Option(
            name="url",
            description="The url of the embed",
            required=False,
        ),
        Option(
            name="footer",
            description="The footer of the embed",
            required=False,
        ),
        Option(
            name="color",
            description="The color of the embed",
            required=False,
            choices=[
                OptionChoice(
                    name="red",
                    value=0xFF0000
                ),
                OptionChoice(
                    name="green",
                    value=0x00FF00
                ),
                OptionChoice(
                    name="blue",
                    value=0x0000FF
                ),
                OptionChoice(
                    name="yellow",
                    value=0xFFFF00
                ),
                OptionChoice(
                    name="cyan",
                    value=0x00FFFF
                ),
                OptionChoice(
                    name="magenta",
                    value=0xFF00FF
                ),
                OptionChoice(
                    name="lime",
                    value=0x2EF429
                ),
                OptionChoice(
                    name="black",
                    value=0x000000
                ),
                OptionChoice(
                    name="white",
                    value=0xFFFFFF
                ),
                OptionChoice(
                    name="defaulf purple color",
                    value=0xAC27FA
                ),
                OptionChoice(
                    name="orange",
                    value=0xFF5E13
                ),
                OptionChoice(
                    name="gold",
                    value=0xCC9900
                ),
                OptionChoice(
                    name="pink",
                    value=0xFF007F
                ),
                OptionChoice(
                    name="purple",
                    value=0x663399
                )
                ]
        )
    ]
)

async def embed(ctx, title,description="",color=0x000000,url="",footer=""):
    em = discord.Embed(colour=color,title=title,description=description,url=url)
    em.set_footer(text=footer)
    await ctx.send(embed=em)


@client.command()
async def emojify(ctx,text_to_be_converted_to_emojis):
    if len(text_to_be_converted_to_emojis) < 120:
        real = text_to_be_converted_to_emojis.lower()
        alphabet = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]
        nums = {
        "1" : "one",
        "2" : "two",
        "3" : "three",
        "4" : "four",
        "5" : "five",
        "6" : "six",
        "7" : "seven",
        "8" : "eight",
        "9" : "nine",
        "0" : "zero",
        "*" : "asterisk",
        "#" : "hash"
        }

        result = ''
        for each in real:
            if each == " ":
                result += "    "
            if each in alphabet:
                result += f":regional_indicator_{each}:"
            if each in nums:
                result += f":{nums[each]}:"
                
        await ctx.send(result)
    else:
        await ctx.send("Please make your argument less than 120 characters")


@client.command()
async def userinfo(ctx, user_to_display_information_about:commands.MemberConverter=None):
    member = user_to_display_information_about
    if member == None:
        member = ctx.author
    roles = [role.mention for role in member.roles[1:]]
    role = ' '.join(roles)
    if len(roles) == 0:
        role="No roles"
    date_format = "%a, %b %d, %Y %I:%M %p"
    av = member.display_avatar.url
    em = nextcord.Embed(title="User Info:",timestamp=datetime.datetime.utcnow(),description=f"{member.name}\'s information:",colour=0xAC27FA)
    em.add_field(name="ID",value=f"```py\n{member.id}```",inline=False)
    em.add_field(name="USERNAME",value=f"```py\n{member.name}#{member.discriminator}```",inline=False)
    em.add_field(name="JOINED SERVER ON",value=f"```\n{member.joined_at.strftime(date_format)}```",inline=False)
    em.add_field(name="CREATED ACCOUNT ON",value=f"```\n{member.created_at.strftime(date_format)}```",inline=False)
    em.add_field(name="ROLES",value=f"{role}",inline=False)
    em.add_field(name="STROGEST ROLE",value=f"{member.top_role.mention}",inline=False)
    bot = "No"
    if member.bot:
        bot = "Yes"
    nick = "No nickname for this user"
    if member.nick != None:
        nick = member.nick
    em.add_field(name="BOT",value=f"```py\n{bot}```",inline=False)
    status = "Can't access the status"
    if member.status == nextcord.Status.online:
        status = "Online"
    if member.status == nextcord.Status.offline:
        status = "Offline"
    if member.status == nextcord.Status.dnd or member.status == nextcord.Status.do_not_disturb:
        status = "Do not disturb"
    if member.status == nextcord.Status.idle:
        status = "Idle"
    if member.status == nextcord.Status.invisible:
        status = "Invisible"
    em.add_field(name="NICKNAME",value=f"```\n{nick}```",inline=False)
    #em.add_field(name="CURRENT STATUS",value=f"```\n{member.status}```",inline=False)
    em.add_field(name="CURRENT ACTIVITY",value=f"```\n{member.activity}```",inline=False)
    em.set_footer(text=f"Requested by {ctx.author.name}.",icon_url=ctx.author.display_avatar.url)
    em.set_thumbnail(url=av)
    await ctx.send(embed=em)


@client.command(aliases=['hex'])
async def hexadecimal(ctx,hex_code=None):
    if hex_code == None:
        await ctx.send("Please specify a Hexadecimal color.")
    else:
        try:
            result = ''
            final = "#"
            if hex_code.startswith("#"):
                final += hex_code.replace("#","")
            if hex_code.startswith("#") == False:
                final += hex_code
            red = "0x" + final[1] + final[2]
            green = "0x" + final[3] + final[4]
            blue = "0x" + final[5] + final[6]
            red = int(red,base=0)
            green = int(green,base=0)
            blue = int(blue,base=0)
            link = f"https://singlecolorimage.com/get/{final[1:]}/900x900.png"
            em = nextcord.Embed(title=f"({red},{green},{blue})",description=f"{final.upper()}",color=nextcord.Color.from_rgb(red,green,blue),timestamp=datetime.datetime.utcnow())
            em.set_image(url=link)
        except:
            em = nextcord.Embed(title=f"Error",description=f"Please provide a valid hexadecimal code like #7378F",color=0xFFFFFF,timestamp=datetime.datetime.utcnow())
        em.set_footer(text=f"Requested by {ctx.author.name}",icon_url=ctx.author.display_avatar.url)
        await ctx.send(embed=em)


@client.command()
async def rgb(ctx,*,rgb_color=None):
    if rgb_color == None:
        await ctx.send("Please specify an RGB color.")
    else:
        try:
            result = ''
            show = ""
            if rgb_color.startswith("(") and rgb_color.endswith(")"):
                fin = rgb_color[1:-1].split(",")
                show =  rgb_color[1:-1]
            if rgb_color.startswith("(") == False and rgb_color.endswith(")") == False:
                fin = rgb_color.split(",")
                show = rgb_color
            fin = [int(n.strip()) for n in fin]
            
            for each in fin:
                hexadecimal = hex(each)[2:]
                if len(hexadecimal) == 1:
                    hexadecimal = "0" + hexadecimal
                result+=hexadecimal
            link = f"https://singlecolorimage.com/get/{result}/900x900.png"
            em = nextcord.Embed(title=f"#{result.upper()}",description=f"({show})",color=nextcord.Color.from_rgb(fin[0],fin[1],fin[2]),timestamp=datetime.datetime.utcnow())
            em.set_image(url=link)
        except:
            em = nextcord.Embed(title=f"Error",description=f"Please provide a valid RGB color like (12,34,56)",color=0xFFFFFF,timestamp=datetime.datetime.utcnow())
        em.set_footer(text=f"Requested by {ctx.author.name}",icon_url=ctx.author.display_avatar.url)
        await ctx.send(embed=em)


@client.command()
async def uwu(ctx,*,text_to_be_converted_to_uwu_case):
    real = text_to_be_converted_to_uwu_case.lower()
    for each in real:
        real = real.replace("thing","fing")
        real = real.replace("l","w")
        real = real.replace("r","w")
    await ctx.send(real+"~")

@client.command()
async def whereami(ctx):
    await ctx.send(f'You are in ({ctx.guild.name}) in {ctx.channel.mention} channel')

@client.command(aliases=['stats'])
async def statstics(ctx):
    username = client.user
    servers = len(client.guilds)
    nextcordV = nextcord.__version__
    #process = psutil.Process(os.getpid())
    #ram =  (process.memory_info().rss / 1000) / 1000
    #ram = "{:.2f}".format(ram)
    #ram = str(ram) + "mb"
    ver = sys.version_info
    em = nextcord.Embed(title=f'Bot\'s statstics',color=0xAC27FA,timestamp=datetime.datetime.utcnow())
    em.add_field(name=":crown:OWNER\'S ID:crown:",value=f"```py\n{ownerID}```",inline=True)
    em.add_field(name="<:py:893420197132771378>PYTHON VERSION<:py:893420197132771378>",value=f"```py\n{ver[0]}.{ver[1]}.{ver[2]}```",inline=True)
    ping = client.latency * 1000
    ping = round(ping)
    em.add_field(name=":zap:LATENCY:zap:",value=f"```py\n\"{ping}ms\"```",inline=True)
    em.add_field(name="FULL USERNAME",value=f"```py\n{username}```",inline=True)
    em.add_field(name=":school:SERVERS:school:",value=f"```py\n{servers}```",inline=True)
    #em.add_field(name=":bar_chart:RAM USAGE:bar_chart:",value=f"```py\n\"{ram}\"```",inline=True)
    em.add_field(name="<:nextcord:901845590663643147>DISCORD VERSION<:nextcord:901845590663643147>",value=f"```py\n{nextcordV}```",inline=True)
    em.add_field(name=":computer:HOST:computer:",value=f"```py\n\"Being hosted on my owner's Samsung Galaxy A51 using Termux.\"```",inline=False)
    em.add_field(name=":timer:ELAPSED TIME:timer:",value=f"```py\n{int((time.time() - begin) / 60)} minutes\n```")
    date_format = "%a, %b %d, %Y %I:%M %p"
    em.set_footer(text=f"Requested by {ctx.author.name}.",icon_url=ctx.author.display_avatar.url)
    await ctx.send(embed=em)

@client.command()
async def serverinfo(ctx):
    date_format = "%a, %b %d, %Y %I:%M %p"
    server = ctx.guild
    name = server.name
    em = nextcord.Embed(title="Server info",description=f"Information about {name}",color=0xAC27FA,timestamp=datetime.datetime.utcnow())
    id =  server.id
    description = server.description
    icon = server.icon.url
    if ctx.guild.banner != None:
        banner = server.banner.url
        em.set_image(url=banner)
    else:
        banner = None
    humans = len(server.humans)
    bots = len(server.bots)
    owner = server.owner
    created = server.created_at
    em.add_field(name="ID",value=f"```\n{id}```",inline=False)
    em.add_field(name="NAME",value=f"```\n{name}```",inline=False)
    em.add_field(name="CREATED ON",value=f"```\n{created.strftime(date_format)}```",inline=False)
    em.add_field(name="HUMANS",value=f"```\n{humans}```",inline=False)
    em.add_field(name="DESCRIPTION",value=f"```\n{description}```",inline=False)
    em.add_field(name="BOTS",value=f"```\n{bots}```",inline=False)
    em.add_field(name="OWNER",value=f"```\n{owner}```",inline=False)
    em.set_thumbnail(url=icon)
    em.set_footer(icon_url=ctx.author.display_avatar.url,text=f"Requested by {ctx.author.name}")
    await ctx.send(embed=em)

@client.command(aliases=['trans','googletrans','googletranslate'])
async def translate(ctx,From=None,To=None,*,question : str=None):
    try:
        src = From
        dst = To
        if src == "auto":
            src = "Auto detect language"
        if src == "en":
            src = "English - English"
        if src == "de":
            src = "German - Deutsch"
        if src == "ar":
            src = "Arabic - عربي"
        if src == "es":
            src = "Spanish - español, castellano"
        if src == "ru":
            src = "Russian - русский"
        if src == "pl":
            src = "Polish - Polski"
        if src == "it":
            src = "Italian - Italiano"
        if src == "ja":
            src = "Japanese - 日本語"
        if src == "ga":
            src = "Irish - Gaeilge"
        if src == "hi":
            src = "Hindi - हिन्दी, हिंदी"
        if src == "he":
            src = "Hebrew - עברית"
        if src == "fr":
            src = "French - Français"
        if src == "nl":
            src = "Dutch - Nederlands"
        if src == "cs":
            src = "Czech - česky, čeština"
        if src == "da":
            src = "Danish - Dansk"
        if src == "zh":
            src = "Chinese - 中文, Zhōngwén"
        if src == "fa":
            src = "Persian - فارسی"
        if dst == "en":
            dst = "English - English"
        if dst == "de":
            dst = "German - Deutsch"
        if dst == "ar":
            dst = "Arabic - عربي"
        if dst == "es":
            dst = "Spanish - español, castellano"
        if dst == "ru":
            dst = "Russian - русский"
        if dst == "pl":
            dst = "Polish - Polski"
        if dst == "it":
            dst = "Italian - Italiano"
        if dst == "ja":
            dst = "Japanese - 日本語"
        if dst == "ga":
            dst = "Irish - Gaeilge"
        if dst == "hi":
            dst = "Hindi - हिन्दी, हिंदी"
        if dst == "he":
            dst = "Hebrew - עברית"
        if dst == "fr":
            dst = "French - Français"
        if dst == "nl":
            dst = "Dutch - Nederlands"
        if dst == "cs":
            dst = "Czech - česky, čeština"
        if dst == "da":
            dst = "Danish - Dansk"
        if dst == "zh":
            dst = "Chinese - 中文, Zhōngwén"
        if dst == "fa":
            dst = "Persian - فارسی"
        search = nextcord.Embed(title="Translating...",description="```py\n\"Please wait...\"```",color=0xAC27FA,timestamp=datetime.datetime.utcnow())
        msg = await ctx.send(embed=search)
        em = nextcord.Embed(title="Translator",description=f"From ({src}) To ({dst})",color=0xAC27FA,timestamp=datetime.datetime.utcnow())
        em.add_field(name="Source text",value=f"```py\n\"{question}\"```",inline=False)
        em.add_field(inline=False,name="Translated text",value=f"```py\n\"{ts.google(question,to_language=To,from_language=From)}\"```")
        em.set_footer(text=f"Requested by {ctx.author.name}",icon_url=ctx.author.display_avatar.url)
        await msg.edit(embed=em)
    except:
        em = nextcord.Embed(description="Please check your arguments again.\nSyntax `trans src-lang dest-lang text`\nYou can read language abbreviations from [here](https://pastebin.com/PrxskfGq).",color=0xAC27FA,timestamp=datetime.datetime.utcnow())
        em.set_footer(text=f"Requested by {ctx.author.name}",icon_url=ctx.author.display_avatar.url)
        await msg.edit(embed=em)

@client.command()
async def reverse(self,ctx,*,text : str):
    result = text [::-1]
    await ctx.send(result)

@client.command()
async def roles(ctx,member : commands.MemberConverter=None):
    user = member
    if user == None:
        user = ctx.author
    if len(user.roles[1:]) >= 1:
        role = [role.mention for role in user.roles[1:]]
        em = nextcord.Embed(title=f"Roles for {user.name}",description='\n'.join(role),color=0xAC27FA,timestamp=datetime.datetime.utcnow())
        em.set_thumbnail(url=user.display_avatar.url)
        em.set_footer(icon_url=ctx.author.display_avatar.url,text=f"Requested by {ctx.author.name}")
        await ctx.send(embed=em)
    else:
        role = ["No roles were found for this user."]
        await ctx.send(' '.join(role))

client.run(token)
