#Currently Working on making code look better
#Next should be automatic score updating for Da Bears
import bs4 as bs
import requests
import discord
import xml.etree.ElementTree as ET
from discord.utils import get

#initiliazes Discord API
TOKEN = 'insert pin here'
client = discord.Client()

#Reads the xml file found at the link
url = "https://static.nfl.com/liveupdate/scorestrip/ss.xml"
session = requests.Session()
headers = {'Connection': ''}
r = session.get(url,headers = headers)
source = r.text
#Utilizes BS to find all 'g' (game) tags
#soup = bs.BeautifulSoup(source, 'lxml')
#root = soup.find_all('g')
root = ''
#Testing reading the file while the program is running
#readFile() works as of now, still of to implement live scoring
def readFile():
    soup = bs.BeautifulSoup(source, 'lxml')
    root = soup.find_all('g')

#create variables location and opponent
location = ""
opponent = ""
timeDiff = -1 #Time difference from Eastern Time (-1 is the default as it is Central Time)
#getGameStats(team)
#Input: The team name after the command !game in a Discord voice channel
#Output: The message depending on the status of the game
#
#The different types of messages:
#1:[team] won against/lost to [opponent] , (score)
#2:[team] plays [opponent] (away/home) on Thursday, Sunday, Monday) at (time in Central Time)
#3:[team] is losing to [opponent], (score)
def getGameStats(team):
    url = "https://static.nfl.com/liveupdate/scorestrip/ss.xml"
    session = requests.Session()
    headers = {'Connection': ''}
    r = session.get(url,headers = headers)
    source = r.text
    soup = bs.BeautifulSoup(source, 'lxml')
    root = soup.find_all('g')

    #runs through each tag in the root directory
    for tag in root:
        #sets 2 dictionaries: one for the home teams, one for the away teams 
        homeDict = tag.attrs['hnn']
        vDict = tag.attrs['vnn']
        #if the team is found in the dictionaries
        if(homeDict == team or vDict == team):
            #Sets variables gameStatus, vScore, and homeScore from the tag attributes in the file
            gameStatus = tag.attrs['q']
            vScore = tag.attrs['vs'] #Visiting team's score
            homeScore = tag.attrs['hs']

            #Sets the location, team and opponent score, and whether the requested team is the visitor or home team
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
            #If the game status is pending (the game has not happened yet)
            #Prints the 2nd message
            if(gameStatus == 'P'):
                    #gets the hour from the the first element of tag attribute t
                    hour = str((int)(tag.attrs['t'][0])+timeDiff) #The hour of the game, subtracted by the time difference from Eastern Time
                    #the hour is given in a string, hence the convergence from string to int back to string

                    #Hours, like arrays start at 0, so if its 0, the time is actually 12
                    if(hour == "0"):
                        hour = "12"
                    #gets the minute from the 2nd through 4th elements of tag attribute t
                    #minute is a string
                    minute = str((int)(tag.attrs['t'][2:4]))
                    #If the minute length is 1, it is a game at at hour (i.e. 12:00) so an extra zero is needed to get proper time
                    if(len(minute)==1):
                        minute += "0"
                    
                    time = hour+":"+minute
                    #Sets the day of the game
                    #Day is given as Thu, Sun, or Mon
                    day = tag.attrs['d']
                    #If the day is Thursday, since its given as Thu, a 'rs' is required before 'day'
                    if(day == 'Thu'):
                        day = day + 'rsday'
                    else:
                        day = day + 'day'
                    #The completed message 2
                    return "The " + team.capitalize() + " play the " + opponent.capitalize() + location +  " on " + day + " at " + time
            #If the game has finished
            #Prints 1st message
            if(gameStatus == 'F'):
                    win = "tied"
                    if(teamScore > oppScore):
                        win = " won against "
                    if(teamScore < oppScore):
                        win = " lost to "
                    return "The " + team.capitalize() + win + "the " + opponent.capitalize() + ", " + str(teamScore) + "-" + str(oppScore)
            #Otherwise, the game is ongoing
            #Prints 3rd message
            else:
                quarter = tag.attrs['q']
                if(quarter == 'H'):
                    endString = "at halftime."
                else:
                    timeLeft = tag.attrs['k']
                    endings = ['st','nd','rd','th']
                    quarter = quarter + endings[int(quarter)-1] + " quarter"
                    endString = " with " + timeLeft + " left in the " + quarter
                status = " are tied to the "
                if(teamScore>oppScore):
                    status = " are winning against the "
                if(teamScore<oppScore):
                    status = " are losing to the "
                return "The " + team.capitalize() + status + opponent.capitalize() + ", " + str(teamScore) + "-" + str(oppScore) + endString
            
#The following is code specifically for the bot in Discord
@client.event

#When a message is sent in a Discord channel
async def on_message(message):
    #We do not want the bot to reply to itself
    if message.author == client.user:
        return
    #If the message starts with the command !game, send the string after !game (the team) to getGameStats
    if message.content.startswith('!game'):

        channel = message.channel

        await message.channel.send(getGameStats(message.content[6:]))
    


@client.event
async def on_ready():

    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    


client.run(TOKEN)
