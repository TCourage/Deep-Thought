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


import discord, sys, traceback, os, re, sqlite3
from discord.ext import commands
from discord.ext.commands import Bot

print("|-----------------------------------------------------------------------------------------|")
print("| Welcome to Deep Thought! The modular, self-hosted, open-source Discord bot alternative. |")
print("| Please take your time to read about the project on GitHub, where you likely downloaded  |")
print("| this software, to learn more about its operation. Have fun!                             |")
print("|-----------------------------------------------------------------------------------------|\n")

server_settings = sqlite3.connect('server.db')  #Access our server settings database
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
    print (f"Token found! Using. Server prefix is: {prefix}\n----------------------------------------")
except:
    token = input("No token found! Please paste your bot token here: ")
    prefix = input("Please select a command prefix. Default is '!'  ")
    if not prefix:
        prefix = '!'
    s.execute('''INSERT INTO server (token, prefix) VALUES (?,?);''', (token, prefix))
    print ("Token and prefix successfully added to DB, will attempt login\n----------------------------------------")


server_settings.commit()
server_settings.close()

intents = discord.Intents().all() #This signals our intents, ensuring we can grab full access to server data
bot = commands.Bot(command_prefix=prefix, intents=intents) 






####  This section pulls a list of files from the 'modules' and 'extras' directories, and
##   now automatically tries to load any .py file in those folders as modules.
print ("Checking for modules...\n")

regex_dir = re.compile('[./]') #strip the leading directory info
regex_file = re.compile('[.py]') #strips the file extension off
num_extensions = 0
initial_extensions = []
extra_extensions = []

for dirName, subdirList, fileList in os.walk("./"):  #os.walk conveniently splits files from directories, and even lists subdirectories
    for x in fileList:  #Check all the files, dirty way of doing this probably but it works
        dir = regex_dir.sub('', dirName)
        fileName = x.strip('.[]')
        fileName = regex_file.sub('', fileName)
        if dir == 'modules':  #Check the primary modules directory
            if ".py" in x: #Ensure we are actually loading python files
                fileName = regex_file.sub('', fileName)
                extension_path = dir + "." + fileName
                initial_extensions.append(extension_path)
                num_extensions += 1
                print(f"Found {extension_path}, adding to extensions list.")
            else:
                extension_path = dir + "." + fileName
                print(f"Error! {dir}/{fileName} is not a valid python file, and will not attempt to be loaded.")
        if dir == 'extras':  #Check the extras folder for modules
            if ".py" in x: #Ensure we are actually trying to load python files
                fileName = regex_file.sub('', fileName)
                extension_path = dir + "." + fileName
                extra_extensions.append(extension_path)
                num_extensions += 1
                print(f"Found {extension_path}, adding to extensions list.")
            else:
                extension_path = dir + "." + fileName
                print(f"Error! {dirName}/{fileName} is not a valid python file, and will not attempt to be loaded.")


print (f"\nNumber of base extensions loaded: {len(initial_extensions)} - {initial_extensions}")
print (f"Number of extra extensions loaded: {len(extra_extensions)} - {extra_extensions}")
print ("----------------------------------------")



#Load our extensions
if __name__ == "__main__":
    print ("Loading main bot extensions...\n")
    if initial_extensions:
        for extension in initial_extensions:
            try:
                if extension:
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
                if extension:
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
