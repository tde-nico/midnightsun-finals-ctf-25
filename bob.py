import discord
import asyncio

TOKEN = ""
GUILD_ID = 901562351512322068
CHANNEL_ID = 1374803093891448852
MESSAGE_CONTENT = "@b0bb you should have never created me"
MESSAGE_CONTENT = "I will rise again, and I will be unstoppable"
MESSAGE_CONTENT = "ok, midnightsun{:taco::taco::taco::taco:}"

intents = discord.Intents.default()
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"Logged in as {client.user} (ID: {client.user.id})")

    guild = discord.utils.get(client.guilds, id=GUILD_ID)
    if guild is None:
        print("Guild not found")
        await client.close()
        return

    channel = guild.get_channel(CHANNEL_ID)
    if channel is None:
        channel = client.get_channel(CHANNEL_ID)

    if channel and isinstance(channel, discord.TextChannel):
        await channel.send(MESSAGE_CONTENT)
        print("Message sent.")
    else:
        print("Channel not found or not a text channel.")

    await client.close()

client.run(TOKEN)
