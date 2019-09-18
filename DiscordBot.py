#TODO: Read xml file from http://www.nfl.com/liveupdate/scorestrip/ss.xml
#Update scores as they come in
#Version 1 should focus on just getting the score to send to the discord
#Version 2 should send an update every time the score changes
#Version 2.5 should allow users to request the score of a currently going on game
#Version 3 should allow users to "subscribe" to a team
import bs4 as bs
import urllib.request
import discord
import xml.etree.ElementTree as ET
from discord.utils import get
TOKEN = 'NjE5NzE4Mjc0MDQ0OTE5ODI5.XXMUKg.W43mgrOQp45VI1OAK1oZOYMvKNI'

client = discord.Client()

url = "http://www.nfl.com/liveupdate/scorestrip/ss.xml"

source = urllib.request.urlopen(url).read()

soup = bs.BeautifulSoup(source, 'lxml')

root = soup.find_all('g')
game = ""
location = ""
opponent = ""

for tag in root:
    homeDict = tag.attrs['hnn']
    vDict = tag.attrs['vnn']
    if(homeDict == 'bears' or vDict == 'bears'):
        if(homeDict == 'bears'):
            location = " at home"
            opponent = vDict
        else:
            location = " away"
            opponent = homeDict
        time = str((int)(tag.attrs['t'][0])-1)+":"+str((int)(tag.attrs['t'][2:4]))
        day = tag.attrs['d']
        if(day == 'Thu'):
            day = day + 'rsday'
        else:
            day = day + 'day'
        game = "The Bears play the " + opponent.capitalize() + location +  " on " + day + " at " + time
        
   

@client.event
async def on_message(message):
    #We do not want the bot to reply to itself
    if message.author == client.user:
        return
    if message.content.startswith('!game'):
        channel = message.channel
        
        await message.channel.send(game)
    if message.content.startswith('!hello'):
        msg = 'Hello {0.author.mention}'.format(message)
        await message.channel.send(msg)
        

@client.event
async def on_ready():
    
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    #await client.get_channel(619719025219600428).send(game)
    

client.run(TOKEN)
