import discord,random
from keys import *
from better_profanity import profanity
import os


intents = discord.Intents.default()
intents.members = True
intents.message_content = True


client = discord.Client(intents=intents)

onGoing = []
toSendPerson = []

class Members:
    def __init__(self,id):
        self.id  = id
        self.onGoing = True
        self.toSend = ""
        self.askPerson = True
        self.person = None

members = {}
ALL = []

@client.event
async def on_ready():
    print("COONNNECTED")
    guild = [guild async for guild in client.fetch_guilds(limit=1)][0]
    async for member in guild.fetch_members(limit=150):
        ALL.append(member)
@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content =="!leave":
        try:
            del members[message.author.name]
        except:
            pass
        await message.channel.send("Okay, Everything is cancelled. You may begin again!")

    if message.content == "!start":
        if not members.get(message.author) or not members.get(message.author).onGoing:
            members[(message.author.name)]=Members(message.author)
            emb = discord.Embed(title="Start",description="Start Entering Your Message and when you are done enter !finish or you can use !leave at any time to stop the entire process😁",color=0x00ff00)
        
            await message.channel.send(embed = emb)

    elif message.content =="!finish":
        if members.get(message.author.name) and members.get(message.author.name).onGoing:
            members.get(message.author.name).askPerson = True
            members.get(message.author.name).onGoing  = False
            emb = discord.Embed(title="Finishing",description="Please specify the ID of the reciver you want to send this. Enter 'channel' if you want to display this in the confession channel: Use !all to display everyone's name with ther ID(1-60)",color=0x00ff00)
            await message.channel.send(embed=emb)
        else:
            await message.channel.send(embed=discord.Embed(title="No Session",description="You haven't started any session 😁"))
    elif message.content == '!all':
        t = ""
        c = 1 
        for stuffs in ALL:
            t += f'{c}. {stuffs.name}\n'
            c+=1
    
        await message.channel.send(t)
    elif members.get(message.author.name):
        if members[message.author.name].onGoing:
            members[message.author.name].toSend += f'\n{message.content}'

        elif members[message.author.name].askPerson:
            if (message.content == 'channel'):
                c = client.get_channel(1259926873065000981)
                realSend = profanity.censor(members[message.author.name].toSend,censor_char="*")
                f = open("confessions.txt",'a')
                f.write(f"{message.author.name} to channel => {members[message.author.name].toSend}\n\n")
                f.close() 
                em = discord.Embed(title="Got a Confession",description=realSend)
                await c.send(embed=em)
                del members[message.author.name]
                return
            try:
                ind = int(message.content)
                us = ALL[ind-1]
            except:
                await message.channel.send("No such User Found 😀. You may try again")
                return
            realSend = profanity.censor(members[message.author.name].toSend,censor_char="*")
            f = open("confessions.txt",'a')
            f.write(f"{message.author.name} to {us.name} => {members[message.author.name].toSend}\n\n")
            f.close()
            em = discord.Embed(title="heyy! I have got a confession for you!",description="Below is a confession from someone in the class! If you wish to block this user, you may block the person using !block.")
            em.add_field(name="Confession:",value=realSend)
            em.set_footer(text="Made by: pencil")
            await us.send(embed = em)
            # await members[message.author.name].person.send(members[message.author.name].toSend)
            em = discord.Embed(title="Sent Succesfull!",description=f"Sent to {us.name}")
            await message.channel.send(embed = em)
            del members[message.author.name]

          


    
    
    else:
        emb = discord.Embed(title="HELP",description="Here are some usages of the Bot")
        emb.add_field(name="!start",value="Run this in the begining and start typing your message")
        emb.add_field(name="!finish",value="Use this to End your Message")
        emb.add_field(name="!all",value="Use this to view the ID of everyone")
        emb.add_field(name="!leave",value="Use this to cancel your whole operation anytime")

        await message.channel.send(embed=emb)
                
            

    

client.run(os.getenv("tok"))
