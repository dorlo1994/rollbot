import discord
import logging


def initialize_logger():
    logger = logging.getLogger('rollbot')
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter('%(levelname)s : %(name)s : %(message)s')

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    return logger


class DiscordBot:

    DEFAULT_PREFIX = '~'

    def __init__(self):
        self._prefix = self.DEFAULT_PREFIX
        self._servers = dict()
        self._logger = initialize_logger()
        self._initialize_client()

    def _initialize_client(self):
        intents = discord.Intents.default()
        intents.message_content = True

        client = discord.Client(intents=intents)

        @client.event
        async def on_ready():
            self._logger.info(f'Bot logged in as {client.user}')

        @client.event
        async def on_message(message):
            if message.author == client.user:
                return
            if message.content.startswith(self._prefix):
                self._handle_message(message)

        self._client = client

    def _handle_message(self, message):
        ...

    def run(self, token):
        self._client.run(token)
