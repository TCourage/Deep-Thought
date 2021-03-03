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
####################################################


import discord, sys, traceback, os, sqlite3
from discord.ext import commands
from discord.ext.commands import Bot

print("|----------------------------------------------------------------------------------------|")
print("| Welcome to Deep Thought! The modular, self-hosted, open-source Discord bot alternative |")
print("| Please take your time to read about the project on GitHub, where you likely downloaded |")
print("| this software, to learn more about its operation. Have fun!                            |")
print("|----------------------------------------------------------------------------------------|\n")

server_db = sqlite3.connect('users.db')  #Access our users database
server_settings = sqlite3.connect('server.db')  #Access our server settings database
c = server_db.cursor()
s = server_settings.cursor()

#Checks for databases, creates them if necessary

print("Checking Server Settings Database status...\n")
try:
    s.execute('''SELECT * FROM server;''')
    print("Using existing database\n----------------------------------------")
except:
    s.execute('''CREATE TABLE server(token text, prefix text);''') 

try:
    print ("Reading token file from DB...\n")
    s.execute('''SELECT * FROM server;''')
    row = s.fetchone()
    token = row[0]
    prefix = row[1]
    print (f"Token found! Using. Server prefix is {prefix}\n----------------------------------------")
except:
    token = input("No token found! Please paste your bot token here: ")
    prefix = input("Please select a command prefix. i.e. if you want your commands to be '!kick' you would enter '!'")
    s.execute('''INSERT INTO server (token, prefix) VALUES (?,?);''', (token, prefix))
    print ("Token and prefix successfully added to DB, will attempt login\n----------------------------------------")


print("Checking User Database status...\n")
try:
    c.execute('''SELECT * FROM users;''')
    print("Using existing database\n----------------------------------------")
except:
    print("Creating new DB, please run the 'setup' command on the server to populate.")
    c.execute('''CREATE TABLE users(id int, name text, discriminator text, nick text, top_role text);''')
    c.execute('''CREATE TABLE discipline(id int, strikes int, kicks int, banned int, bans int);''')

server_db.commit()
server_db.close()
server_settings.commit()
server_settings.close()

intents = discord.Intents().all()
bot = commands.Bot(command_prefix=prefix, intents=intents)


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


#Load our extensions
if __name__ == "__main__":
    print ("Loading main bot extensions...\n")
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
        
    print ("----------------------------------------\nLoading extra bot extensions...\n")
    if extra_extensions:
        for extension in extra_extensions:
            try:
                bot.load_extension(extension)
                print(f"Loaded extention {extension}")
            except Exception as e:
                print(f"Failed to load extension {extension}.", file=sys.stderr)
                traceback.print_exc()
    else:
        print("No extra extensions found, skipping")


#What the bot runs when it's loaded and ready
@bot.event
async def on_ready():
    print('We have logged in as {0.user}\n----------------------------------------\n'.format(bot))

print("----------------------------------------\nlogging in...\n")

#Reads bot token from the database
bot.run(token)
