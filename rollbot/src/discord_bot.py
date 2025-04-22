from rollbot.src.system.dnd5e import Dnd5e
from collections import namedtuple

import discord
import logging


Command = namedtuple('Command', ['description', 'function'])


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
        self._commands = {
            'prefix': Command(f'Changes rollbot\'s assigned prefix. default is {self.DEFAULT_PREFIX}', self.set_prefix),
            'help': Command('Get available commands.', self.help_str),
            'system': None
        }
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
            try:
                await self._handle_message(message)
            except ValueError as e:
                self._logger.info(f'Couldn\'t handle message {message.content}: {e}')
                await message.channel.send(f'Sorry, ran into an error: {e}')

        self._client = client

    async def _handle_message(self, message):
        message_metadata = message.to_message_reference_dict()
        guild_id, channel_id = message_metadata['guild_id'], message_metadata['channel_id']

        # Ensure the message comes from a known channel
        if guild_id not in self._guilds.keys():
            # Handle joining a guild
            self.join_guild(guild_id, channel_id)
        elif channel_id not in self._guilds[guild_id].keys():
            # Handle joining a new channel in an existing server
            self.join_channel(guild_id, channel_id)

        # Handle message
        channel_settings = self._guilds[guild_id][channel_id]
        if message.content.startswith(channel_settings['prefix']):
            parsed_message = message.content[len(channel_settings['prefix']):].split(' ')
            command_key = parsed_message.pop(0)
            command = self._commands.get(command_key)
            if not command:
                raise ValueError(f'Unknown command \"{command_key}\"')
            await command.function(guild_id, channel_id, parsed_message, message)

    def join_guild(self, guild_id, channel_id):
        self._logger.info(f'Entered new guild with id {guild_id}')
        self._guilds[guild_id] = dict()
        self.join_channel(guild_id, channel_id)

    def join_channel(self, guild_id, channel_id):
        self._logger.info(f'Entered new channel in guild {guild_id} with id {channel_id}')
        self._guilds[guild_id][channel_id] = self._default_settings()

    def _default_settings(self) -> dict:
        settings = dict()
        settings['prefix'] = self.DEFAULT_PREFIX
        settings['system'] = Dnd5e()
        settings['characters'] = dict()
        return settings

    def run(self, token):
        self._client.run(token)

    async def set_prefix(self, guild_id, channel_id, parsed_message: list[str], message):
        self._logger.info(f'Changing prefix of channel {channel_id} in guild {guild_id} to {parsed_message[0]}')
        self._guilds[guild_id][channel_id]['prefix'] = parsed_message[0]
        await message.channel.send(f'Changed prefix to {parsed_message[0]}')

    async def help_str(self, guild_id, channel_id, parsed_message, message):
        help_str = "List of available commands:\n"
        for command, details in self._commands.items():
            if details:
                help_str += f'{command}: {details.description}\n'
        await message.channel.send(help_str)
