import discord, sys, traceback, os
from discord.ext import commands
from discord.ext.commands import Bot

#Our list of extensions - now pulled from files!
with open('main-extensions.txt', 'r') as fd:
    initial_extensions = fd.readlines()
initial_extensions = [x.strip() for x in initial_extensions]

with open('extra-extensions.txt', 'r') as fd:
    extra_extensions = fd.readlines()
extra_extensions = [x.strip() for x in extra_extensions]


bot = commands.Bot(command_prefix='|')

#Load our extensions
if __name__ == "__main__":
    for extension in initial_extensions:
        try:
            bot.load_extension(extension)
            print(f"Loaded extention {extension}")
        except Exception as e:
            print(f"Failed to load extension {extension}.", file=sys.stderr)
            traceback.print_exc()
    
    for extension in extra_extensions:
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

#This reads our token from the token file. This is ideal for security purposes when open-
#sourcing a project like this and keeping modularity.
with open ("token", "r") as tokenFile:
    token = tokenFile.read()
bot.run(token)
