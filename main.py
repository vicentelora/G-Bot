import discord
from discord.ext import tasks
from helpfoos import cycle

# Related to bot's life
from KEEPMEALIVE import keep_alive
from botlife import wake_bot

# Bot's functionalities
from quotes import get_quote
from eventsgdsc import get_last_GDSCevent

client = discord.Client()

@client.event
async def on_ready():
  change_status.start()
  print('I\'m Alive')

status = cycle(['Beep','Boop'])

@tasks.loop(seconds=10)
async def change_status():
  await client.change_presence(activity=discord.Game(next(status)))

@client.event
async def on_message(message):
  if message.author == client.user:
    return

  if message.content.startswith("heyo g"):
    await message.channel.send("Heyo g")

  if message.content.startswith("hey g hype me up"):
    quote = get_quote()
    await message.channel.send(quote)

  if message.content.startswith("hey g go sleep"):
    await message.channel.send("Going to bedorama")
    await client.close()

  if message.content.startswith("event"):
    url = "https://gdsc.community.dev/university-of-warwick/"
    event_message = get_last_GDSCevent(url)

    await message.channel.send(event_message)

keep_alive()
wake_bot(client)