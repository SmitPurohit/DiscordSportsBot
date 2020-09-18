# DiscordSportsBot
This is a bot written for Discord in Python that provides the current score/status of an NFL game.
This program utilizes an xml file found on the NFL's website at http://static.nfl.com/liveupdate/scorestrip/ss.xml.
It reads the xml file using the Beautiful Soup package.

In order to use this bot/add this bot to a server, you need a Discord authorization token, which is easy to acquire.
1) Go to discordapp.com/developers/applications/me and login/create a Discord bot
2) Press "New Application" and follow the instructions to make an application
3) Click "Bot" on the right hand menu and click "Add Bot"
4) In the Bot menu, look and click on "Token: Click to Reveal"
5) Copy and paste the token into the environment variable TOKEN
6) Add the bot to your server by going to https://discordapp.com/oauth2/authorize?&client_id=CLIENTID&scope=bot&permissions=8
   Replace CLIENTID with the CLIENTID found in "App Details"
7) Run the discordbot.py file

The command for this bot is !game [team], where team is any NFL team.
The bot will either return the score of the game of the current team if it is ongoing, the final score of the game, or when the requested 
team is playing and who they are playing.

This is still a work in progress, but is mostly functional.
My main planned additions to this program are more sports, the ability to "subscribe" and get notifications when the score changes for a team,
and (way farther into the future) predicting the winner of the game (or possibly using another web scrape to get the predicted winner from sports analysts)

