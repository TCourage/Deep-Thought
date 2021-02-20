import discord, sys, traceback, os
from discord.ext import commands
from discord.ext.commands import Bot

#Our list of extensions - now pulled from files!
try:
    with open('main-extensions.txt', 'r') as f:
        initial_extensions = f.readlines()
    initial_extensions = [x.strip() for x in initial_extensions]  #strip any unnecessary whitespace
except FileNotFoundError:
    initial_extensions = []
try:
    with open('extra-extensions.txt', 'r') as fd:
        extra_extensions = fd.readlines()
    extra_extensions = [x.strip() for x in extra_extensions]
except FileNotFoundError:
    extra_extensions = []


bot = commands.Bot(command_prefix='^')

#Load our extensions
if __name__ == "__main__":
    print("|---------------------------------------------|")
    print("| Welcome to Deep Thought! The modular, self- |")
    print("| hosted, open-source Discord bot alternative |")
    print("| Please take your time to read about the pr- |")
    print("| oject on GitHub, where you likely download- |")
    print("| ed this software, to learn more about its   |")
    print("| operation. Have fun!                        |")
    print("|---------------------------------------------|")
    print ("----------------------------------------------\nLoading main bot extensions...\n")
    if initial_extensions:
        for extension in initial_extensions:
            try:
                bot.load_extension(extension)
                print(f"Loaded extention {extension}")
            except Exception as e:
                print(f"Failed to load extension {extension}.", file=sys.stderr)
                traceback.print_exc()
    else:
        print("No Main extensions found! Caution, may cause error. Skipping...")
        
    print ("--------------------\nLoading extra bot extensions...\n")
    if extra_extensions:
        for extension in extra_extensions:
            try:
                bot.load_extension(extension)
                print(f"Loaded extention {extension}")
            except Exception as e:
                print(f"Failed to load extension {extension}.", file=sys.stderr)
                traceback.print_exc()
    else:
        print("No extra extensions found, skipping...")

print("--------------------\nlogging in....\n--------------------")

@bot.event
async def on_ready():
    print('We have logged in as {0.user}\n--------------------\n'.format(bot))

#This reads our token from the token file. This is ideal for security purposes when open-
#sourcing a project like this and keeping modularity.
with open ("token", "r") as tokenFile:
    token = tokenFile.read()
bot.run(token)
