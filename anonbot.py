"""
Copyright (c) 2018–2019 ArgentSileo, supchppt

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
import datetime
import io
from os import getenv

import discord
from discord.ext import commands

# Initialization
game = discord.Game('Shhhhh...')
bot = commands.Bot(command_prefix='a_',
                   description='Keeping it quiet.', activity=game)
token = getenv('ANONBOT_TOKEN')


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

bot.remove_command('help')

# When receive DM, forward message to designated channel


@bot.event
async def on_message(message):
    channel = bot.get_channel("""your channel id here""")
    log_channel = bot.get_channel("""your channel id here""")

    # If message is DM, log and forward message.
    if message.guild is None and message.author != bot.user:
        # Creates a log entry in case of hooliganism.
        log_message = f'Used by {message.author.name} on {datetime.datetime.now()}:'
        has_attachments = message.attachments != []
        # Sends message.
        await log_channel.send(log_message)
        if has_attachments:
            async with channel.typing():
                files = [await pull_attachment(attachment) for attachment in message.attachments]
        else:
            files = None
        sent_message = await channel.send('Someone said: {}'.format(message.content), files=files)
        await log_channel.send(message.content if message.content != '' else '<no text>')
        if has_attachments:
            await log_channel.send('Attachments: {}'.format('\n'.join([attachment.proxy_url for attachment in sent_message.attachments])))
    await bot.process_commands(message)


async def pull_attachment(attachment):
    file = io.BytesIO()
    await attachment.save(file)
    return discord.File(file, filename=attachment.filename)


bot.run(token)
