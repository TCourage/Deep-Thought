import discord, sys, traceback, os, asyncio, sqlite3
from discord.ext import commands, tasks
from discord.ext.commands import Bot, has_permissions, CheckFailure

## So this is our database management module. It handles updating the database and keeping
# it updated when new users join.

class dbLaunch(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    #The update command. This handles when the user runs '|setup' or another alias and updates everything
    @commands.command(name="setup", aliases=["setupdb", "dbupdate", "update", "updatedb"], pass_context=True)
    @commands.has_permissions(administrator=True)
    async def setupdb(self, ctx):
        adds = 0
        changes = 0
        x = ctx.guild.members

        #Open our DB
        server_db = sqlite3.connect('server.db')
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

    #This code automatically updates the database when new users join.
    @commands.Cog.listener("on_member_join")
    async def member_join_update(self, member: discord.Member):
        channel = member.guild.system_channel
        #await channel.send(f'Member {member.mention} has joined!')
        print("New user {} has joined! Updating database...\n".format(member))
        adds = 0
        changes = 0

        #Open our DB
        server_db = sqlite3.connect('server.db')
        c = server_db.cursor()
        print("Users added:")
        print("--------------------------------\n")
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
            server_db = sqlite3.connect('server.db')
            c = server_db.cursor()
            try: #Do the update
                c.execute('''UPDATE users SET nick = (?) WHERE id = (?);''', (after.nick, after.id))
                print (f"User {before.name}#{before.discriminator} ({before.nick}) changed their nick to {after.name}#{after.discriminator} ({after.nick}). Database updated.")
            except:
                print (f"User {before.name} changed their profile in some way, but there was an error and the DB was not updated.")
        elif (before.name != after.name): #If their Discord name changed
            server_db = sqlite3.connect('server.db')
            c = server_db.cursor()
            try: #Do the update
                c.execute('''UPDATE users SET name = (?) WHERE id = (?);''', (after.name, after.id))
                print (f"User {before.name}#{before.discriminator} ({before.nick}) changed their name to {after.name}#{after.discriminator} ({after.nick}). Database updated.")
            except:
                print (f"User {before.name} changed their profile in some way, but there was an error and the DB was not updated.")
        elif (before.discriminator != after.discriminator): #If they changed their discriminator
            server_db = sqlite3.connect('server.db')
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

        

def setup(bot): #setup and launch bot
    bot.add_cog(dbLaunch(bot))