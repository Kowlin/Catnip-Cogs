#Imported Stuffios
import asyncio
import functools
import io
import os
import unicodedata
import aiohttp
import json
import random
import discord
import datetime
import time

from discord.ext import commands
from __main__ import send_cmd_help
from asyncio import sleep
from cogs.utils.dataIO import dataIO
from random import randint
from random import choice
from .utils import checks
from datetime import datetime, timedelta

class analytics:
    #Defining Stuffios
    def __init__(self, bot):
        self.bot = bot
        self.database_file = 'data/analytics/Database.json'
        self.database = dataIO.load_json(self.database_file)
        self.vcKeeper = {}
        self.timeHours = 0
        self.timeDays = 0
        self.timeMinutes = 0
        self.timeSeconds = 0
        self.formmatedTime = ""

    #Checkios
    async def save_database(self):
        dataIO.save_json(self.database_file, self.database)

    async def timeFormat(self, seconds):
        #Day
        if seconds > 86400:
            dayTuple = divmod(seconds, 86400)
            self.timeDays = dayTuple[0]
            seconds = dayTuple[1]
        #Hour
        if seconds > 3600:
            hourTuple = divmod(seconds, 3600)
            self.timeHours = hourTuple[0]
            seconds = hourTuple[1]
        #Minute
        if seconds > 60:
            minuteTuple = divmod(seconds, 60)
            self.timeMinutes = minuteTuple[0]
            seconds = minuteTuple[1]
        #Seconds
        self.timeSeconds = seconds
        if self.timeDays > 0:
            self.formmatedTime = str(self.timeDays) + " days, " + str(self.timeHours) + " hours, " + str(self.timeMinutes) + " minutes, " + str(self.timeSeconds) + " seconds."
        elif self.timeHours > 0:
            self.formmatedTime = str(self.timeHours) + " hours, " + str(self.timeMinutes) + " minutes, " + str(self.timeSeconds) + " seconds."
        elif self.timeMinutes > 0:
            self.formmatedTime = str(self.timeMinutes) + " minutes, " + str(self.timeSeconds) + " seconds."
        else:
            self.formmatedTime = str(self.timeSeconds) + " seconds."


    #Commandios
    @commands.command(pass_context = True)
    async def ustats(self, ctx, user: discord.Member):
        """"Get stats on a person!"""
        server = ctx.message.server

        #Setupio
        if server.id not in self.database:
            self.database[server.id] = {}
        if user.id not in self.database[server.id]:
            self.database[server.id][user.id] = {}

        #Checkios
        if "rAdded" not in self.database[server.id][user.id]:
            self.database[server.id][user.id]["rAdded"] = 0
        if "mSent" not in self.database[server.id][user.id]:
            self.database[server.id][user.id]["mSent"] = 0
        if "cSent" not in self.database[server.id][user.id]:
            self.database[server.id][user.id]["cSent"] = 0
        if "mDeleted" not in self.database[server.id][user.id]:
            self.database[server.id][user.id]["mDeleted"] = 0
        if "ceSent" not in self.database[server.id][user.id]:
            self.database[server.id][user.id]["ceSent"] = 0
        if "vcJoins" not in self.database[server.id][user.id]:
            self.database[server.id][user.id]["vcJoins"] = 0
        if "vcTime" not in self.database[server.id][user.id]:
            self.database[server.id][user.id]["vcTime"] = 0
        if "tPinged" not in self.database[server.id][user.id]:
            self.database[server.id][user.id]["tPinged"] = 0
        await self.save_database()
        await self.timeFormat(int(self.database[server.id][user.id]["vcTime"]))

        #Actual Embedio
        ustatembed = discord.Embed(color = 0x546e7a)
        ustatembed.add_field(name = " ❯ General Stats", value = "Times Pinged Others: " + str(self.database[server.id][user.id]["tPinged"]), inline = False)
        ustatembed.add_field(name = " ❯ Emote Stats", value = "Custom Emotes Sent: " + str(self.database[server.id][user.id]["ceSent"]) + "\n" + "Reactions Added: " + str(self.database[server.id][user.id]["rAdded"]), inline = False)
        ustatembed.add_field(name = " ❯ Message Stats", value = "Messages Sent: " + str(self.database[server.id][user.id]["mSent"]) + "\n" + "Characters Sent: " + str(self.database[server.id][user.id]["cSent"]) + "\n" + "Messages Deleted: " + str(self.database[server.id][user.id]["mDeleted"]), inline = False)
        ustatembed.add_field(name = " ❯ VC Stats", value = "VC Sessions: " + str(self.database[server.id][user.id]["vcJoins"]) + "\n" + "Time Spent: " + str(self.formmatedTime), inline = False)
        await self.bot.send_message(ctx.message.channel, embed = ustatembed)

    @commands.command(pass_context = True)
    async def sstats(self, ctx):
        """Get stats on the server!"""
        server = ctx.message.server
        online = len([m.status for m in server.members if m.status == discord.Status.online or m.status == discord.Status.invisible])
        idle = len([m.status for m in server.members if m.status == discord.Status.idle])
        dnd = len([m.status for m in server.members if m.status == discord.Status.dnd])
        offline = len([m.status for m in server.members if m.status == discord.Status.offline])
        total_users = len(server.members)
        text_channels = len([x for x in server.channels
                             if x.type == discord.ChannelType.text])
        voice_channels = len(server.channels) - text_channels
        passed = (ctx.message.timestamp - server.created_at).days
        created_at = ("Since {}. That's over {} days ago!"
                      "".format(server.created_at.strftime("%d %b %Y %H:%M"),
                                passed))

        #Actual Embedio
        sstatembed = discord.Embed(color = 0x546e7a)
        sstatembed.add_field(name = " ❯ Server Info", value = "Created: " + str(passed) + " days ago" + "\n" + "Members: " + str(total_users), inline = False)
        sstatembed.add_field(name = " ❯ Count Stats", value = "Text Channels: " + str(text_channels) + "\n" + "Voice Channels: " + str(voice_channels), inline = False)
        sstatembed.add_field(name = " ❯ Member Stats", value = "Online: " + str(online) + "\n" + "Idle: " + str(idle) + "\n" + "DND: " + str(dnd) + "\n" + "Offline: " + str(offline), inline = False)
        await self.bot.send_message(ctx.message.channel, embed = sstatembed)

    #Sent Message Dectectorio
    async def on_message(self, message):
        #Setupio Up Server
        server = message.server
        if server.id not in self.database:
            self.database[server.id] = {}

        server = message.server
        author = message.author
        if not author.id in self.database[server.id]:
            self.database[server.id][author.id] = {}
            if "rAdded" not in self.database[server.id][author.id]:
                self.database[server.id][author.id]["rAdded"] = 0
            if "mSent" not in self.database[server.id][author.id]:
                self.database[server.id][author.id]["mSent"] = 0
            if "cSent" not in self.database[server.id][author.id]:
                self.database[server.id][author.id]["cSent"] = 0
            if "mDeleted" not in self.database[server.id][author.id]:
                self.database[server.id][author.id]["mDeleted"] = 0
            if "ceSent" not in self.database[server.id][author.id]:
                self.database[server.id][author.id]["ceSent"] = 0
            if "vcJoins" not in self.database[server.id][author.id]:
                self.database[server.id][author.id]["vcJoins"] = 0
            if "vcTime" not in self.database[server.id][author.id]:
                self.database[server.id][author.id]["vcTime"] = 0
            if "tPinged" not in self.database[server.id][author.id]:
                self.database[server.id][author.id]["tPinged"] = 0
            self.database[server.id][author.id]["mSent"] = self.database[server.id][author.id]["mSent"] + 1
            await self.save_database()
        else:
            self.database[server.id][author.id]["mSent"] += 1
            await self.save_database()

        #Character Count
        messagelen = len(message.content)
        if not "cSent" in self.database[server.id][author.id]:
            self.database[server.id][author.id]["cSent"] = 0
            self.database[server.id][author.id]["cSent"] += messagelen
            await self.save_database()
        else:
            self.database[server.id][author.id]["cSent"] += messagelen
            await self.save_database()

        #Custom Emotes Count
        sentMessage = str(message.content)
        splitMessages = sentMessage.split()
        emotesDetected = 0
        for temp in splitMessages:
            if temp[0] == "<":
                try:
                    name = temp.split(':')[1]
                    emotesDetected = emotesDetected + 1
                except:
                    emotesDetected = emotesDetected
            else:
                emotesDetected = emotesDetected

        if not "ceSent" in self.database[server.id][author.id]:
            self.database[server.id][author.id]["ceSent"] = 0
            self.database[server.id][author.id]["ceSent"] += emotesDetected
            await self.save_database()
        else:
            self.database[server.id][author.id]["ceSent"] += emotesDetected
            await self.save_database()

        #Mention Detectionio
        tmp = {}
        for mention in message.mentions:
                tmp[mention] = True
        if message.author.id != self.bot.user.id:
            for taggedPerson in tmp:
                self.database[server.id][author.id]["tPinged"] += 1
                await self.save_database()

    #Deleted Message Dectectorio
    async def on_message_delete(self, message):
        server = message.server
        author = message.author
        if "mDeleted" not in self.database[server.id][author.id]:
            self.database[server.id][author.id]["mDeleted"] = 0
            self.database[server.id][author.id]["mDeleted"] = 1
            await self.save_database()
        else:
            self.database[server.id][author.id]["mDeleted"] += 1
            await self.save_database()

    #Reaction Detectionio
    # IDEA: Track most used emote
    async def on_reaction_add(self, reaction, user):
        server = user.server
        author = user
        if "rAdded" not in self.database[server.id][author.id]:
            self.database[server.id][author.id]["rAdded"] = 0
            self.database[server.id][author.id]["rAdded"] += 1
            await self.save_database()
        else:
            self.database[server.id][author.id]["rAdded"] = self.database[server.id][author.id]["rAdded"] + 1
            await self.save_database()

    #Voice Chat Detectionio
    async def on_voice_state_update(self, before, after):
        server = after.server
        member = after
        if server.id not in self.database:
            self.database[server.id] = {}

        if not member.id in self.database[server.id]:
            self.database[server.id][member.id] = {}
            if "rAdded" not in self.database[server.id][member.id]:
                self.database[server.id][member.id]["rAdded"] = 0
            if "mSent" not in self.database[server.id][member.id]:
                self.database[server.id][member.id]["mSent"] = 0
            if "cSent" not in self.database[server.id][member.id]:
                self.database[server.id][member.id]["cSent"] = 0
            if "mDeleted" not in self.database[server.id][member.id]:
                self.database[server.id][member.id]["mDeleted"] = 0
            if "ceSent" not in self.database[server.id][member.id]:
                self.database[server.id][member.id]["ceSent"] = 0
            if "vcJoins" not in self.database[server.id][member.id]:
                self.database[server.id][member.id]["vcJoins"] = 0
            if "vcTime" not in self.database[server.id][member.id]:
                self.database[server.id][member.id]["vcTime"] = 0
            await self.save_database()


        if not before.voice.voice_channel and after.voice.voice_channel:
            self.database[server.id][member.id]["vcJoins"] += 1
            timeNow = datetime.now()
            self.vcKeeper[member.id] = timeNow
            await self.save_database()
        elif before.voice.voice_channel and not after.voice.voice_channel:
            timeNow = datetime.now()
            timeSpent = timeNow - self.vcKeeper[member.id]
            self.database[server.id][member.id]["vcTime"] += int(timeSpent.total_seconds())
            await self.save_database()

            if member.id in self.vcKeeper:
                del self.vcKeeper[member.id]


#Check Folderio
def check_folder():
    if not os.path.exists("data/analytics"):
        print("Creating data/analytics folder...")
        os.makedirs("data/analytics")

#Check Fileio
def check_file():
    data = {}
    f = "data/analytics/Database.json"
    if not dataIO.is_valid_json(f):
        print("Creating default Database.json...")
        dataIO.save_json(f, data)

#Setupio
def setup(bot):
    check_folder()
    check_file()
    cog = analytics(bot)
    bot.add_cog(cog)
