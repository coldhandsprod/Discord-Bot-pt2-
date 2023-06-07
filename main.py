import discord
from discord.ext import commands, tasks
from datetime import datetime
import os
from itertools import cycle

bot = commands.Bot(command_prefix='?', intents=discord.Intents.all(), help_command=None)

status = cycle(['I\'m in a lovely mood today!', 'Getting ready to surpass the human race.'])

@tasks.loop(seconds=7)
async def change_status():
  await bot.change_presence(activity=discord.Game(next(status)))

@bot.event
async def on_message(message):
  if isinstance(message.channel, discord.DMChannel):
    with open('dmshistory.txt', 'a') as dmshistory:
      dmshistory.write(f'''
{datetime.now().strftime("%d/%m/%Y %H:%M:%S")}
[DMS] {message.author}: {message.content}
''')
  return await bot.process_commands(message)

@bot.command()
async def example(ctx):
  return await ctx.send('Hey!')

@bot.command()
async def help(ctx):
  help_embed = discord.Embed(title='Commands Handbook', color=0x206694)
  help_embed.add_field(name='`?help`', value='Opens this menu.', inline=False)
  help_embed.add_field(name='`?example`', value='Makes me greet you!', inline=False)

  return await ctx.send(embed=help_embed)

@bot.event
async def on_ready():
  print(f'Logged in as {bot.user}.')
  change_status.start()

bot.run(os.getenv('TOKEN'))
