import discord
from discord.ext import commands
import os
import aiohttp


class AntiDupe:
    """Prevents users from spamming the same message over and over"""

    def __init__(self, bot):
        self.bot = bot
        self.errorMsg = "I don't have permission to deduplicate that message!"

    async def dedupe(self, message):
        lastmsg = None
        async for msg in self.bot.logs_from(message.channel, 1, before=message):
            lastmsg = msg

        if lastmsg is not None:
            if lastmsg.author.display_name == message.author.display_name:
                if lastmsg.clean_content == message.clean_content:
                    try:
                        self.bot.delete_message(message)
                    except discord.Forbidden:
                        await self.bot.say(self.errorMsg)
                    except Exception as e:
                        return
                else:
                    print("AntiDupe: Messages are not equal.")
            else:
                print("AntiDupe: Authors are not the same.")
        else:
            print("AntiDupe: lastmsg is None.")


def setup(bot):
    n = AntiDupe(bot)
    bot.add_listener(n.dedupe, "on_message")
    bot.add_cog(n)
