from rollbot.src.system.dnd5e import Dnd5e

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
        self._guilds = dict()
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
            await self._handle_message(message)

        self._client = client

    async def _handle_message(self, message):
        message_metadata = message.to_message_reference_dict()
        guild_id, channel_id = message_metadata['guild_id'], message_metadata['channel_id']
        if guild_id not in self._guilds.keys():
            # Handle joining a guild
            self.join_guild(guild_id, channel_id)
        elif channel_id not in self._guilds[guild_id].keys():
            # Handle joining a new channel in an existing server
            self.join_channel(guild_id, channel_id)

        # Handle message
        channel_settings = self._guilds[guild_id][channel_id]
        if message.content.startswith(channel_settings['prefix']):
            await message.channel.send(f'This is a {channel_settings['system']} channel! Let\'s try a check:'
                                       f' {channel_settings['system'].check()}')

    def join_guild(self, guild_id, channel_id):
        self._logger.info(f'Added to new guild with id {guild_id}')
        self._guilds[guild_id] = dict()
        self.join_channel(guild_id, channel_id)

    def join_channel(self, guild_id, channel_id):
        self._logger.info(f'Entered a new channel in guild {guild_id} with id {channel_id}')
        self._guilds[guild_id][channel_id] = self._default_settings()

    def _default_settings(self) -> dict:
        settings = dict()
        settings['prefix'] = self.DEFAULT_PREFIX
        settings['system'] = Dnd5e()
        settings['characters'] = dict()
        return settings

    def run(self, token):
        self._client.run(token)
