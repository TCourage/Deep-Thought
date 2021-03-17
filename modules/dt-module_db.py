import discord, sys, traceback, os, asyncio, sqlite3, datetime
from discord.ext import commands, tasks
from discord.ext.commands import Bot, has_permissions, CheckFailure

## So this is our database management module. It handles updating the database and keeping
# it updated when new users join.

## I'm trying to keep the bulk of the database operations in this file, if possible.
# Commands like 'on_join' or 'on_ban' etc. really help.

## I'm also trying to keep commands in the top section of the file, and listeners at the bottom.
# Keeps things organized better IMO.

## Version 1.0

#First let's check that the database exists. If not, create the tables.
#Open our DB
server_db = sqlite3.connect('users.db')
c = server_db.cursor()
print("Checking User Database status...\n")
try:
    c.execute('''SELECT * FROM users;''')
    print("Using existing database\n----------------------------------------")
except:
    print("Creating new DB, please run the 'setup' command on the server to populate.\n----------------------------------------")
    c.execute('''CREATE TABLE users(id int, name text, discriminator text, nick text, top_role text);''')
    c.execute('''CREATE TABLE discipline(id int, strikes int, kicks int, banned int, bans int, strike1_reason text DEFAULT "None", strike1_date text DEFAULT "None", strike1_givenby text DEFAULT "None", strike2_reason text DEFAULT "None", strike2_date text DEFAULT "None", strike2_givenby text DEFAULT "None", ban_reason text DEFAULT "None", ban_date text DEFAULT "None");''')

#Write changes and close the DB
server_db.commit()
server_db.close()

class Database_Module(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    #The update command. This handles when the user runs '|setup' or another alias and updates everything
    @commands.command(name="setup", aliases=["setupdb", "dbupdate", "update", "updatedb"], pass_context=True, description = "Manually update the server's database, MUST be run at first launch. Also a good idea if the server has been offline for some time. Otherwise, the server will automatically update as soon as someone new joins.", brief = "Manually update the database")
    @commands.has_permissions(administrator=True)
    async def setupdb(self, ctx):
        adds = 0
        changes = 0
        x = ctx.guild.members

        #Open our DB
        server_db = sqlite3.connect('users.db')
        c = server_db.cursor()

        print("\n--------------------------------")
        print("Updating database...\n")

        #If server perms are setup right, this grabs a list of every user on the server
        for member in x:
            #Create a list for the current users' info
            users = [member.id, member.name, member.discriminator, member.nick, member.top_role.name]
            print(member)
            
            #This checks the database to see if the user already as an entry,
            #and skips adding them if they do.            
            c.execute('''SELECT * FROM users WHERE id = (?);''', (member.id,))
            row = c.fetchone()
            # If the user does not exist, we'll create them and add to the database;
            if row == None:
                #If the member has no nickname, we'll set it as N/A
                if member.nick == None:
                    try:
                        users = [member.id, member.name, member.discriminator, 'N/A', member.top_role.name]
                        c.execute('''INSERT INTO users (id, name, discriminator, nick, top_role) VALUES (?,?,?,?,?);''', users)
                        c.execute('''INSERT INTO discipline (id, strikes, kicks, banned, bans) VALUES (?,?,?,?,?);''', [member.id, 0, 0, 0, 0])
                        print("User {} successfully added to the database;".format(users[1]))
                        print(users)
                        print("--------------------------------")
                        adds += 1
                    except:
                        print("Error inserting user {} in database".format(users[1]))
                #If they have a nick, we'll set it
                else:
                    try:
                        c.execute('''INSERT INTO users (id, name, discriminator, nick, top_role) VALUES (?,?,?,?,?);''', users)
                        c.execute('''INSERT INTO discipline (id, strikes, kicks, banned, bans) VALUES (?,?,?,?,?);''', [member.id, 0, 0, 0, 0])
                        print("User {} successfully added to the database;".format(users[1]))
                        print(users)
                        print("--------------------------------")
                        adds += 1
                    except:
                        print("Error inserting user {} in database".format(users[1]))
      
            # Otherwise if the user *does* exist, we'll check if they need anything updated and do it.
            else:
                if users[3] == row[3]: #If nothing is changed we skip
                    print("User {} already in database and no changes to be made, skipping...".format(users[1]))
                elif users[3] != row[3] and users[3] != None:  #If they change their nick we'll update
                    try:
                        c.execute('''INSERT INTO users (nick) VALUES (?);''', users[3])
                        print("User {} updated successfully".format(users[1]))
                        changes += 1
                    except:
                        print("Error editing user {}".format(users[1]))
                elif users[3] == None and row[3] != "N/A": #User removes nick we'll update that
                    print(row[3])
                    try:
                        c.execute('''INSERT INTO users (nick) VALUES ('N/A');''')
                        print("User {} updated successfully".format(users[1]))
                        changes += 1
                    except:
                        print("Error editing user {}".format(users[1]))
                elif users[1] != row[1] and users[1] != None: #If they change their actual Discord name (instead of server nick), we'll update that.
                    try:
                        c.execute('''INSERT INTO users (name) VALUES (?);''', users[1])
                        print("User {} updated successfully".format(users[1]))
                        changes += 1
                    except:
                        print("Error editing user {}".format(users[1]))
                else:
                    print("User {} already in database and no changes to be made, skipping...".format(users[1]))
        print("--------------------------------")

        #Lets the console user/server owner know if anything has been updated. Also sends results to the channel the update
        #was requested in to give a quick and dirty update on what happened.
        if (changes > 0) or (adds > 0):
            await ctx.send("Database updated with {} new and {} modified entries - please see server log for more details.".format(adds, changes))
            print("\nDatabase updated with {} new and {} modified entries - please see server log for more details.".format(adds, changes))
        else:
            await ctx.send("No changes were made to the database - up to date!")
            print("\nNo changes were made to the database - up to date!")
        print("\n--------------------------------\n")

        #Write changes and close the DB
        server_db.commit()
        server_db.close()

    #If a non-admin uses this command, tell the user they're not allowed to do that
    @setupdb.error
    async def db_perms_error(self, ctx, error):
        if isinstance(error, CheckFailure):
            messageAuthor = ctx.author.mention
            await ctx.send(f"Sorry {messageAuthor}, you are not allowed to do that. Only administrators may update the database.")


    @commands.command(name = "checkdb", aliases = ["querydb", "searchdb", "dbsearch", "dbcheck", "dbquery"], pass_context = True, description = "Check a user's detailed info currently stored in the database.", brief = "Check the database")
    @commands.has_permissions(administrator=True)
    async def checkdb(self, ctx, member: discord.Member = None):
        #Open our DB
        server_db = sqlite3.connect('users.db')
        c = server_db.cursor()
        now = datetime.datetime.now()
        date = now.strftime("%Y %B %d, %H:%M:%S")

        if member == ctx.message.author:  #Check your own data
            c.execute('''SELECT * FROM users WHERE id = (?)''', (member.id,))
            row = c.fetchone()
            print (row)
            embed=discord.Embed(title=f"Database info for {member.name}:")
            embed.add_field(name="Discord User ID", value=f"{row[0]}", inline=True)
            embed.add_field(name="Discord Username", value=f"{row[1]}", inline=True)
            embed.add_field(name="User Discriminator", value=f"{row[2]}", inline=True)
            embed.add_field(name="Server Nickname", value=f"{row[3]}", inline=True)
            embed.add_field(name="Server Top Role", value=f"{row[4]}", inline=True)
            c.execute('''SELECT * FROM discipline WHERE id = (?)''', (member.id,))
            row = c.fetchone()
            embed.add_field(name="Number of Strikes", value=f"{row[1]}", inline=True)
            embed.add_field(name="Times Kicked", value=f"{row[2]}", inline=True)
            if row[3] == 0:
                embed.add_field(name="Currently banned?", value="No", inline=True)
            else:
                embed.add_field(name="Currently banned?", value="Yes", inline=True)
            embed.add_field(name="Times Banned", value=f"{row[4]}", inline=True)
            embed.set_footer(text = f"Data requested: {date}, by user {ctx.message.author.name}")
            await ctx.channel.send(embed=embed)
        elif member == None: #Also checks your own data
            member = ctx.message.author
            c.execute('''SELECT * FROM users WHERE id = (?)''', (member.id,))
            row = c.fetchone()
            embed=discord.Embed(title=f"Database info for {member.name}:")
            embed.add_field(name="Discord User ID", value=f"{row[0]}", inline=True)
            embed.add_field(name="Discord Username", value=f"{row[1]}", inline=True)
            embed.add_field(name="User Discriminator", value=f"{row[2]}", inline=True)
            embed.add_field(name="Server Nickname", value=f"{row[3]}", inline=True)
            embed.add_field(name="Server Top Role", value=f"{row[4]}", inline=True)
            c.execute('''SELECT * FROM discipline WHERE id = (?)''', (member.id,))
            row = c.fetchone()
            embed.add_field(name="Number of Strikes", value=f"{row[1]}", inline=True)
            embed.add_field(name="Times Kicked", value=f"{row[2]}", inline=True)
            if row[3] == 0:
                embed.add_field(name="Currently banned?", value="No", inline=True)
            else:
                embed.add_field(name="Currently banned?", value="Yes", inline=True)
            embed.add_field(name="Times Banned", value=f"{row[4]}", inline=True)
            embed.set_footer(text = f"Data requested: {date}, by user {ctx.message.author.name}")
            await ctx.channel.send(embed = embed)
        else:
            c.execute('''SELECT * FROM users WHERE id = (?)''', (member.id,))
            row = c.fetchone()
            embed=discord.Embed(title=f"Database info for {member.name}:")
            embed.add_field(name="Discord User ID", value=f"{row[0]}", inline=True)
            embed.add_field(name="Discord Username", value=f"{row[1]}", inline=True)
            embed.add_field(name="User Discriminator", value=f"{row[2]}", inline=True)
            embed.add_field(name="Server Nickname", value=f"{row[3]}", inline=True)
            embed.add_field(name="Server Top Role", value=f"{row[4]}", inline=True)
            c.execute('''SELECT * FROM discipline WHERE id = (?)''', (member.id,))
            row = c.fetchone()
            embed.add_field(name="Number of Strikes", value=f"{row[1]}", inline=True)
            embed.add_field(name="Times Kicked", value=f"{row[2]}", inline=True)
            if row[3] == 0:
                embed.add_field(name="Currently banned?", value="No", inline=True)
            else:
                embed.add_field(name="Currently banned?", value="Yes", inline=True)
            embed.add_field(name="Times Banned", value=f"{row[4]}", inline=True)
            embed.set_footer(text = f"Data requested: {date}, by user {ctx.message.author.name}")
            await ctx.channel.send(embed = embed)

        #Write changes and close the DB
        server_db.commit()
        server_db.close()

    #If a non-admin uses this command, tell the user they're not allowed to do that
    @checkdb.error
    async def checkdb_error(self, ctx, error):
        if isinstance(error, CheckFailure):
            messageAuthor = ctx.author.mention
            await ctx.send(f"Sorry {messageAuthor}, you are not allowed to do that. Only administrators may check the database.")



    #######################################################################################################
    ########################################### LISTENER SECTION ##########################################
    #######################################################################################################

    #This code automatically updates the database when new users join.
    @commands.Cog.listener("on_member_join")
    async def member_join_update(self, member: discord.Member):
        channel = member.guild.system_channel
        #await channel.send(f'Member {member.mention} has joined!')
        print("New user {} has joined! Updating database...\n".format(member))
        adds = 0
        changes = 0

        #Open our DB
        server_db = sqlite3.connect('users.db')
        c = server_db.cursor()
        print("Users added:\n")
        x = member.guild.members
        #If server perms are setup right, this grabs a list of every user on the server
        for member in x:
            #Create a list for the current users' info
            users = [member.id, member.name, member.discriminator, member.nick, member.top_role.name]
            
            #This checks the database to see if the user already as an entry,
            #and skips adding them if they do.            
            c.execute('''SELECT * FROM users WHERE id = (?);''', (member.id,))
            row = c.fetchone()
            # If the user does not exist, we'll create them and add to the database
            if row == None:
                #If the member has no nickname, we'll set it as N/A
                if member.nick == None: #This is the same code as above, so just read the above to understand this better.
                    try:
                        users = [member.id, member.name, member.discriminator, 'N/A', member.top_role.name]
                        c.execute('''INSERT INTO users (id, name, discriminator, nick, top_role) VALUES (?,?,?,?,?);''', users)
                        c.execute('''INSERT INTO discipline (id, strikes, kicks, banned, bans) VALUES (?,?,?,?,?);''', [member.id, 0, 0, 0, 0])
                        print("User {} successfully added to the database;".format(users[1]))
                        print(users)
                        print("--------------------------------")
                        adds += 1
                    except:
                        print("Error inserting user {} in database".format(users[1]))
                else:
                    try:
                        c.execute('''INSERT INTO users (id, name, discriminator, nick, top_role) VALUES (?,?,?,?,?);''', users)
                        c.execute('''INSERT INTO discipline (id, strikes, kicks, banned, bans) VALUES (?,?,?,?,?);''', [member.id, 0, 0, 0, 0])
                        print("User {} successfully added to the database;".format(users[1]))
                        print(users)
                        print("--------------------------------")
                        adds += 1
                    except:
                        print("Error inserting user {} in database".format(users[1]))
      


            else:
                if users[3] == row[3]: #If the user exists, we skip them
                    print("User {} already in database and no changes to be made, skipping...".format(users[1]))
                elif users[3] != row[3] and users[3] != None: #If the new nickname doesn't match the old one, we'll update it
                    try:
                        c.execute('''INSERT INTO users (nick) VALUES (?);''', users[3])
                        print("User {} updated successfully".format(users[1]))
                        changes += 1
                    except:
                        print("Error editing user {}".format(users[1]))
                elif users[3] == None and row[3] != "N/A": #If they remove their nickname, update
                    print(row[3])
                    try:
                        c.execute('''INSERT INTO users (nick) VALUES ('N/A');''')
                        print("User {} updated successfully".format(users[1]))
                        changes += 1
                    except:
                        print("Error editing user {}".format(users[1]))
                elif users[1] != row[1] and users[1] != None: #If they change their actual Discord name (instead of server nick), we'll update that.
                    try:
                        c.execute('''INSERT INTO users (name) VALUES (?);''', users[1])
                        print("User {} updated successfully".format(users[1]))
                        changes += 1
                    except:
                        print("Error editing user {}".format(users[1]))
                else:
                    print("User {} already in database and no changes to be made, skipping...".format(users[1]))
        print("--------------------------------")
        if (changes > 0) or (adds > 0):
            #await channel.send("Database updated with {} new and {} modified entries - please see server log for more details".format(adds, changes))
            print("\nDatabase updated with {} new and {} modified entries - please see server log for more details".format(adds, changes))
        else:
            #await channel.send("No changes were made to the database - up to date!")
            print("\nNo changes were made to the database - up to date!")
        print("\n--------------------------------\n")

        # Write to and close the DB
        server_db.commit()
        server_db.close()
    
    # This subroutine automatically updates the DB when a user changes something
    @commands.Cog.listener("on_member_update")
    async def member_update(self, before, after):
        #Open DB
        if (before.nick != after.nick): #If the nickname changed
            server_db = sqlite3.connect('users.db')
            c = server_db.cursor()
            try: #Do the update
                c.execute('''UPDATE users SET nick = (?) WHERE id = (?);''', (after.nick, after.id))
                print (f"User {before.name}#{before.discriminator} ({before.nick}) changed their nick to {after.name}#{after.discriminator} ({after.nick}). Database updated.")
            except:
                print (f"User {before.name} changed their profile in some way, but there was an error and the DB was not updated.")
        elif (before.name != after.name): #If their Discord name changed
            server_db = sqlite3.connect('users.db')
            c = server_db.cursor()
            try: #Do the update
                c.execute('''UPDATE users SET name = (?) WHERE id = (?);''', (after.name, after.id))
                print (f"User {before.name}#{before.discriminator} ({before.nick}) changed their name to {after.name}#{after.discriminator} ({after.nick}). Database updated.")
            except:
                print (f"User {before.name} changed their profile in some way, but there was an error and the DB was not updated.")
        elif (before.discriminator != after.discriminator): #If they changed their discriminator
            server_db = sqlite3.connect('users.db')
            c = server_db.cursor()
            try: #Do the update
                c.execute('''UPDATE users SET discriminator = (?) WHERE id = (?);''', (after.discriminator, after.id))
                print (f"User {before.name}#{before.discriminator} ({before.nick}) changed their name to {after.name}#{after.discriminator} ({after.nick}). Database updated.")
            except:
                print (f"User {before.name} changed their profile in some way, but there was an error and the DB was not updated.")
        else:
            return

        
        # Write to and close the DB
        server_db.commit()
        server_db.close()

        
    #This section triggers when a user is unbanned and updated the database accordingly 
    @commands.Cog.listener("on_member_unban")
    async def member_unban(self, guild, member):
        #Open our DB and edit
        server_db = sqlite3.connect('users.db')
        c = server_db.cursor()
        c.execute('''UPDATE discipline SET banned = 0, ban_reason = (?), ban_date = "None", strikes = 0, strike1_date = "None", strike1_reason = "None", strike1_givenby = "None", strike2_date = "None", strike2_reason = "None", strike2_givenby = "None" WHERE id = (?);''', (None, member.id,))

        #Write changes and close the DB
        server_db.commit()
        server_db.close()

    #This section triggers when a user is banned
    @commands.Cog.listener("on_member_ban")
    async def member_ban(self, guild, member):
        #Open our DB
        server_db = sqlite3.connect('users.db')
        c = server_db.cursor()
        #Get current time and date for the database
        now = datetime.datetime.now()
        time = now.strftime("%Y %B %d, %H:%M:%S")
        
        #Get the current number of bans of this user
        c.execute('''SELECT bans FROM discipline WHERE id = (?);''', (member.id,))
        row = c.fetchone()
        bans = row[0]
        bans += 1 #Update the number of bans, then set
        c.execute('''UPDATE discipline SET bans = (?), banned = 1, ban_date = (?) WHERE id = (?);''', (bans, time, member.id,))

        #Write changes and close the DB
        server_db.commit()
        server_db.close()


def setup(bot): #setup and launch bot
    bot.add_cog(Database_Module(bot))