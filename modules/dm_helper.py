import asyncio
from typing import Union, List

import discord
from discord.ext import commands

class DMSession:
    def __init__(self, bot: commands.Bot, user: Union[discord.User, discord.Member]):
        self.bot = bot
        self.user = user

    async def send_messages(self, messages: List[Union[str, discord.Embed]], **kwargs):
        """
        Kwargs will be applied to each message
        """
        for message in messages:
            await self.send_message(message=message, **kwargs)

    async def send_message(self, message: Union[str, discord.Embed], **kwargs):
        if type(message) == discord.Embed:
            await self.user.send(embed=message)
        else:
            await self.user.send(message)

    async def send_messages_get_response(self,
                                         messages: List[Union[str, discord.Embed]],
                                         wait_timeout: float = 10.0,
                                         **kwargs):
        """
        Kwargs will be applied to each message
        Await response to last message
        """
        for message in messages[:-1]:
            await self.send_message(message=message, **kwargs)
        return await self.send_message_get_response(message=messages[-1], wait_timeout=wait_timeout, **kwargs)

    async def send_message_get_response(self,
                                        message: Union[str, discord.Embed],
                                        wait_timeout: float = 10.0,
                                        **kwargs) -> discord.Message:

        if type(message) == discord.Embed:
            await self.user.send(embed=message)
        else:
            await self.user.send(message)

        def check(msg):
            return msg.channel == self.user.dm_channel and msg.author == self.user

        try:
            return await self.bot.wait_for("message", check=check, timeout=wait_timeout)
        except asyncio.TimeoutError:
            return None

    async def start_interactive_session(self, prompt_and_callbacks: list, starting_message = None, ending_message = None, **kwargs):
        if starting_message:
            await self.send_message(message=starting_message, **kwargs)

        for pair in prompt_and_callbacks:
            for prompt, callback in pair.items():
                move_on = False
                while not move_on:
                    response = await self.send_message_get_response(message=prompt, **kwargs)
                    if response:
                        move_on, reply = callback(response)  # callback needs to return [True, success_message] if everything is fine, [False, error_message] if not
                        if reply:
                            await self.send_message(message=reply)

        if ending_message:
            await self.send_message(message=ending_message, **kwargs)
