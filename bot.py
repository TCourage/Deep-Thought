################    DEEP THOUGHT    ################
#                                                  #
# Deep Thought - the modular, open-source, self-   #
# hosted Discord bot that does what you need it to #
# do. Please ensure you have discord.py installed  #
# for the bot to operate correctly.                #
#                                                  #
# This code and all so-called "main extensions"    #
# remain the sole property of the owner of the     #
# original GitHub repository, and are free for use #
# and modification, so long as said repository is  #
# linked back to with your final product.          #
#                                                  #
#                                                  #
#                                                  #
# Version 0.4.1                                    #
####################################################


import discord, sys, traceback, os, sqlite3
from discord.ext import commands
from discord.ext.commands import Bot

server_db = sqlite3.connect('server.db')
c = server_db.cursor()

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

intents = discord.Intents().all()
bot = commands.Bot(command_prefix='|', intents=intents)

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
    print("--------------------\nChecking db status...\n")
    try:
        c.execute('''SELECT * FROM users;''')
        print("Using existing database")
        print("Ready.")
    except:
        print("Creating new DB, please run the 'setup' command on the server to populate.")
        c.execute('''CREATE TABLE users(id int, name text, discriminator text, nick text, top_role text);''')
        c.execute('''CREATE TABLE discipline(strikes int, kicks int, banned int, bans int);''')
    server_db.commit()
    server_db.close()
        


#This reads our token from the token file. This is ideal for security purposes when open-
#sourcing a project like this and keeping modularity.
with open ("token", "r") as tokenFile:
    token = tokenFile.read()
bot.run(token)
