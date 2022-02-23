import os

def wake_bot(client):
  TOKEN = os.environ['Love']
  client.run(TOKEN)