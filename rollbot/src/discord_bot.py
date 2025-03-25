import discord


def initialize_bot(token: str, prefix: str):
    intents = discord.Intents.default()
    intents.message_content = True

    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        # Todo: logging!
        print(f'Bot logged in as {client.user}')

    @client.event
    async def on_message(message):
        if message.author == client.user:
            return
        if message.content.startswith(prefix):
            await message.channel.send(f'Hi there, {message.author}!')

    client.run(token)
