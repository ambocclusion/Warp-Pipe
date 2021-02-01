# WARP PIPE

This is a bot that mirrors chat messages from a Discord channel over to a Slack channel and vice versa.

## Dependencies

This requires Python 3 to run.
This uses the following pip packages:

discord.py
slackclient
webpreview

## How to use

Install the above libraries using pip install.

Create a Slack bot by going to https://api.slack.com/apps and clicking "Create new app", going to OAuth and Permissions and giving your bot the following permissions:<br />
![Slackbot required permissions](/images/slackperms.png)<br />
Copy the key from the OAuth & Permissions page into your config.json
After you do this, install the bot and add it to a channel by @-mentioning it inside the chat, then inside the Slack app/browser window, right click on the channel and copy link. You'll get something that looks like this: https://mySlackServer.slack.com/archives/C123456 copy the last portion of the URL into your config.json under "mirrors" then "slack".

On Discord, go to https://discord.com/developers/applications and create a New Application. Turn this application into a bot and copy your bot token into config.json. Afterwards, go to the OAuth2 page and tick "bot" under scopes, and give it "Send Messages" and "Read Message History" permissions. Copy the link into your address bar and grant the bot permission to your Discord server. Inside of your Discord server, right click on the channel you want the bot to mirror and click "Copy ID" and paste that into the "mirrors" then "discord" section.

Run using python3 warppipe.py.