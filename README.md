# NFLScoresBot
This is a bot written for Discord in Python that provides the current score/status of an NFL game.
This program utilizes an xml file found on the NFL's website at http://static.nfl.com/liveupdate/scorestrip/ss.xml.
It reads the xml file using the Beautiful Soup package.

The command for this bot is !game [team], where [team] is any NFL team. For example, !game bears.
The bot will either return the score of the game of the current team if it is ongoing, the final score of the game, or when the requested 
team is playing and who they are playing.

This is still a work in progress, but is mostly functional.
My main planned additions to this program are more sports, the ability to "subscribe" and get notifications when the score changes for a team,
and (way farther into the future) predicting the winner of the game (or possibly using another web scrape to get the predicted winner from sports analysts)

