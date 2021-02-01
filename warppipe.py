import discord, json, slack, os, threading, time, asyncio, requests, sys, shutil, io, gc, traceback, re, urlmarker, webpreview
from discord.ext import commands, tasks
from os.path import splitext
from urllib.parse import urlparse
from webpreview import web_preview

config = {}
configfile = "./config.json"

state = {}
stateFile = './state.json'

intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)

with open(configfile, 'rb') as j:
    config = json.load(j)

with open(stateFile, 'rb') as s:
        state = json.load(s)

def saveState(stateObject):
    save = json.dumps(stateObject)
    with open(stateFile, 'w') as j:
        j.write(save)

slack_client = slack.WebClient(config['slackToken'])

@client.event
async def on_ready():
    await startSlackBot(client)

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    for m in config['mirrors']:
        if m['discord'] == message.channel.id:
            text = message.author.name + ": " + message.content
            if len(message.attachments) == 0:
                slack_client.chat_postMessage(text = text, channel= m['slack'])
            else:
                url = message.attachments[0].url
                print('downloading ' + url)
                img = requests.get(url, stream=True)
                parsed = urlparse(url)
                root, ext = splitext(parsed.path)
                if img.status_code == 200:
                    img.raw.decode_content = True
                    with open('./input' + ext, 'wb') as file:
                        shutil.copyfileobj(img.raw, file)
                    
                    with open('./input' + ext, 'rb') as file:
                        slack_client.chat_postMessage(text = text, channel= m['slack'])
                        slack_client.files_upload(channels = m['slack'], file=io.BytesIO(file.read()))

def getSort(r):
    return r['ts']

def is_url_image(image_url):
   image_formats = ("image/png", "image/jpeg", "image/jpg")
   r = requests.head(image_url)
   if r.headers["content-type"] in image_formats:
      return True
   return False

async def startSlackBot(discordClient):
    print('starting slack')
    await asyncio.sleep(1)
    while client is None:
        await asyncio.sleep(1)

    print('ready')
    while True:
        try:
            response = slack_client.conversations_history(
                channel = config['mirrors'][0]['slack'],
                oldest = state['lastMessage']
            )

            response['messages'].sort(key=getSort)

            for r in response['messages']:
                for x in config['mirrors']:
                    state['lastMessage'] = r['ts']
                    saveState(state)
                    user = slack_client.users_info(user = r['user'])
                    if user['user']['is_bot'] == False:
                        message_channel = client.get_channel(x['discord'])
                        url = re.findall(urlmarker.URL_REGEX, r['text'])
                        text = user['user']['real_name'] + ': ' + r['text']

                        if len(url) != 0:
                            try:
                                if is_url_image(url[0]) == False:
                                    title, description, image = web_preview(url[0])
                                    embed = discord.Embed(title=title, description=description, url=url[0])
                                    if image != None:
                                        embed.set_image(url=image)
                                else:
                                    embed = discord.Embed(url=url[0])
                                    embed.set_image(url=url[0])
                            except Exception as e:
                                traceback.print_exc()
                        else:
                            embed = None

                        if 'files' in r:
                            url = r['files'][0]['url_private_download']
                            img = requests.get(url, stream=True, headers={'Authorization':'Bearer ' + config['slackToken']})
                            parsed = urlparse(url)
                            root, ext = splitext(parsed.path)
                            if img.status_code == 200:
                                img.raw.decode_content = True
                                with open('./input' + ext, 'wb') as file:
                                    shutil.copyfileobj(img.raw, file)
                                
                                discordFile = discord.File(fp='./input' + ext)
                                await message_channel.send(str(text), file=discordFile, embed=embed)
                        else:                                
                            await message_channel.send(text, embed=embed)

                        await asyncio.sleep(1)
        except Exception as e:
            traceback.print_exc()

        gc.collect()

        await asyncio.sleep(1)

print('starting bots')

print('starting discord')
client.run(config['discordToken'])