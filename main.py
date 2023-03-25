import os
from dotenv import load_dotenv
from telethon import TelegramClient
from telethon.sync import events
from chat_api import get_response, get_messages
import asyncio
import requests
import random

load_dotenv()
BOT_TOKEN = os.environ.get('BOT_TOKEN')
USER_PASSWORD = os.environ.get('USER_PASSWORD')
MASTER_PASSWORD = os.environ.get('MASTER_PASSWORD')
API_ID = os.environ.get('API_ID')
API_HASH = os.environ.get('API_HASH')
SH_API_KEY = os.environ.get('SH_API_KEY')
url = "https://stablehorde.net/api/"
payload = {
  "prompt": "Horde of robots",
  "params": {
    "sampler_name": "k_lms",
    "cfg_scale": 5,
    "denoising_strength": 0.60,
    "seed": "string",
    "height": 1024,
    "width": 1024,
    "seed_variation": 1,
    "post_processing": [
      "GFPGAN"
    ],
    "karras": True,
    "tiling": False,
    "hires_fix": True,
    "clip_skip": 1,
    "image_is_control": False,
    "facefixer_strength": 0.75,
    "steps": 50,
    "n": 1
  },
  "nsfw": True,
  "trusted_workers": False,
  "slow_workers": True,
  "censor_nsfw": False,
  "models": [
    'Dreamshaper'
  ],
}

bot = TelegramClient('bot',API_ID,API_HASH).start(bot_token=BOT_TOKEN)

chat_messages = [
    {"role": "system", "content": "You are a helpful friend who always gives short and concise single sentence answers to questions!"}
]

def trim_chat(messages):
    if len(messages) > 4:
        messages.pop(1)
    return messages

async def get_finished_image(id:str, chat):
    returned_img=requests.get(url=url+f"v2/generate/status/{id}").json()
    #await bot.send_message(chat,"image done")
    await bot.send_message(chat, returned_img['generations'][0]['img'])


    return
    imgdata = requests.get(returned_img['generations'][0]['img'], allow_redirects=True)
    
    with open(id + '.png','wb') as file:
        file.write(imgdata.content)

async def poll(id:str, chat):
    response = requests.get(url=url+f"v2/generate/check/{id}").json()
    if(response['finished']==1):
        await get_finished_image(id, chat)
    else:
        await poll(id, chat)

async def generate(prompts:list, chat):
    ids = []
    await bot.send_message(chat, f"generating {len(prompts)} images with prompts: {str(prompts)}")
    for prompt in prompts:
        payload["prompt"] = prompt
        payload["params"]["seed"] = prompt
        ids.append(requests.post(url=url+"v2/generate/async", json= payload, headers= {"apikey": SH_API_KEY}).json()['id'])
    for id in ids:
        await poll(id, chat)

@bot.on(events.NewMessage)
async def any_message_arrived(event):
    chat = await event.get_chat()
    message = event.message.message
    sender = await event.get_sender()
    if(sender.id!=5868798835):
        return
    if message[0:2] == '-i':
        await generate(get_messages(message[2:]), chat)
        #await bot.send_message(chat, "downloaded")
        return

    tokens = 500 if '??' in message else 100
    global chat_messages
    chat_messages.append({'role':'user', 'content': message})
    chat_messages = trim_chat(chat_messages)
    #print(chat_messages)
    response = get_response(chat_messages, Max_tokens=tokens)
    print(response)
    chat_messages.append(response)
    chat_messages = trim_chat(chat_messages)
    await bot.send_message(chat, response['content'])

    return


print("ready")
bot.run_until_disconnected()
