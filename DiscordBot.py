#Reads from an xml site and uses Discord API to create a bot that gives the 
#next upcoming game/score of a finished game of a requested team
#Currently Working on making code look better
#Next up is if !game is called when a game is going on
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
location = ""
opponent = ""
def getGameStats(team):
    for tag in root:
        if(homeDict == team or vDict == team):
            gameStatus = tag.attrs['q']
            homeDict = tag.attrs['hnn']
            vDict = tag.attrs['vnn']
            vScore = tag.attrs['vs']
            homeScore = tag.attrs['hs']            
            if(homeDict == team):
                location = " at home"
                opponent = vDict
                teamScore = (int)(homeScore)
                oppScore = (int)(vScore)
            else:
                location = " away"
                opponent = homeDict
                teamScore = (int)(vScore)
                oppScore = (int)(homeScore)
            if(gameStatus == 'P'):
                    hour = str((int)(tag.attrs['t'][0])-1)
                    if(hour == "0"):
                        hour = "12"
                    minute = str((int)(tag.attrs['t'][2:4]))
                    if(len(minute)==1):
                        minute += "0"
                    time = hour+":"+minute
                    day = tag.attrs['d']
                    if(day == 'Thu'):
                        day = day + 'rsday'
                    else:
                        day = day + 'day'
                    return "The " + team.capitalize() + " play the " + opponent.capitalize() + location +  " on " + day + " at " + time
            if(gameStatus == 'F'):
                    win = "tied"
                    if(teamScore > oppScore):
                        win = " won against "
                    if(teamScore < oppScore):
                        win = " lost to "
                    return "The " + team.capitalize() + win + "the " + opponent.capitalize() + ", " + str(teamScore) + "-" + str(oppScore)
            else:
@client.event
async def on_message(message):
    #We do not want the bot to reply to itself
    if message.author == client.user:
        return
    if message.content.startswith('!game'):

        channel = message.channel

        await message.channel.send(getGameStats(message.content[6:]))
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
