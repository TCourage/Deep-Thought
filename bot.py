import discord
import sys, traceback
import os
from discord.ext import commands
from discord.ext.commands import Bot

#Our list of extensions. Ideally this would be pulled from a file
initial_extensions = ["modules.dt-module_kick",
                        "modules.dt-module_ban",
                        "modules.dt-module_roll"
                    ]

bot = commands.Bot(command_prefix='!')

#Load our extensions
if __name__ == "__main__":
    for extension in initial_extensions:
        try:
            bot.load_extension(extension)
            print(f"Loaded extention {extension}")
        except Exception as e:
            print(f"Failed to load extension {extension}.", file=sys.stderr)
            traceback.print_exc()

print("logging in....")

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))

bot.run('NzA4MDI1NTAwMTYxMDE1ODI4.XrRWkg.A00ICCxcVZVTtf_BftUcqLfTJOg')
