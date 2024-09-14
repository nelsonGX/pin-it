import discord
import os
from dotenv import load_dotenv

load_dotenv()

token = os.getenv("TOKEN")
confirm_cap = int(os.getenv("CONFIRM_CAP"))
message_vote_count = {}
message_to_pin = {}

if confirm_cap > 10 or confirm_cap < 0:
    print("CONFIRM_CAP must be between 0 and 10")
    exit()

async def translate_number(num: int):
    emojis = ["<:pixel1:942438227380408350>", "<:pixel2:942438227258785802>", "<:pixel3:942438227585957968>", "<:pixel4:942438227107786804>", "<:pixel5:942438227623702589>", "<:pixel6:942438227330089060>", "<:pixel7:942438227476901958>", "<:pixel8:942438227002949652>", "<:pixel9:942438227405602906>", "<:pixel10:942438227825029160>"]
    return emojis[num-1]

client = discord.Client(intents=discord.Intents.all())

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    global message_voute_count

    if message.author == client.user:
        return
    
    if message.content.startswith(f"<@{client.user.id}>"):
        message_pin = await client.get_channel(message.channel.id).fetch_message(message.reference.message_id)
        if  confirm_cap == 0:
            await message_pin.pin()
            return
        else:
            message_vote_count[str(message.id)] = 0
            message_to_pin[str(message.id)] = message_pin
            await message.add_reaction("✅")
            await message.add_reaction("<:slash:1284496769551568927>")
            count = await translate_number(confirm_cap)
            await message.add_reaction(count)

@client.event
async def on_reaction_add(reaction, user):
    global message_vote_count
    global message_to_pin

    if user == client.user:
        return
    
    if str(reaction.emoji) == "✅":
        message_vote_count[str(reaction.message.id)] += 1
        if message_vote_count[str(reaction.message.id)] >= confirm_cap:
            await message_to_pin[str(reaction.message.id)].pin()

client.run(token)