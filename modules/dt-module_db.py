import discord, sys, traceback, os, asyncio, sqlite3
from discord.ext import commands, tasks
from discord.ext.commands import Bot, has_permissions, CheckFailure



class dbLaunch(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="setup", aliases=["setupdb", "dbupdate", "update", "updatedb"], pass_context=True)
    @commands.has_permissions(administrator=True)
    async def setupdb(self, ctx):
        adds = 0
        changes = 0
        #Open our DB, create if doesn't exist.

        server_db = sqlite3.connect('server.db')
        c = server_db.cursor()
        print("\n--------------------------------")
        #try:
        print("Writing users to database...\n")
        print("Users added:\n")
        x = ctx.guild.members
        #If server perms are setup right, this grabs a list of every user on the server
        for member in x:
            #Create a list for the current users' info
            users = [member.id, member.name, member.discriminator, member.nick, member.top_role.name]
            
            #This checks the database to see if the user already as an entry,
            #and skips adding them if they do.            
            c.execute('''SELECT * FROM users WHERE id=?''', (member.id,))
            row = c.fetchone()
            # If the user does not exist, we'll create them and add to the database
            if row == None:
                #If the member has no nickname, we'll set it as N/A
                if member.nick == None:
                    try:
                        users = [member.id, member.name, member.discriminator, 'N/A', member.top_role.name]
                        c.execute('''INSERT INTO users (id, name, discriminator, nick, top_role) VALUES (?,?,?,?,?);''', users)
                        c.execute('''INSERT INTO discipline (strikes, kicks, banned, bans) VALUES (?,?,?,?);''', 0, 0, 0, 0)
                        print("User {} successfully added to the database;".format(users[1]))
                        print(users)
                        print("--------------------------------")
                        adds += 1
                    except:
                        print("Error inserting user {} in database".format(users[1]))
                else:
                    #try:
                        c.execute('''INSERT INTO users (id, name, discriminator, nick, top_role) VALUES (?,?,?,?,?);''', users)
                        c.execute('''INSERT INTO discipline (strikes, kicks, banned, bans) VALUES (?,?,?,?);''', 0, 0, 0, 0)
                        print("User {} successfully added to the database;".format(users[1]))
                        print(users)
                        print("--------------------------------")
                        adds += 1
                    except:
                        print("Error inserting user {} in database".format(users[1]))
      


            else:
                if users[3] == row[3]:
                    print("User {} already in database and no changes to be made, skipping...".format(users[1]))
                elif users[3] != row[3] and users[3] != None:
                    try:
                        c.execute('''INSERT INTO users (nick) VALUES (?);''', users[3])
                        print("User {} updated successfully".format(users[1]))
                        changes += 1
                    except:
                        print("Error editing user {}".format(users[1]))
                elif users[3] == None and row[3] != "N/A":
                    print(row[3])
                    try:
                        c.execute('''INSERT INTO users (nick) VALUES ('N/A');''')
                        print("User {} updated successfully".format(users[1]))
                        changes += 1
                    except:
                        print("Error editing user {}".format(users[1]))
                else:
                    print("User {} already in database and no changes to be made, skipping...".format(users[1]))
        print("--------------------------------")
        if (changes > 0) or (adds > 0):
            await ctx.send("Database updated with {} new and {} modified entries - please see server log for more details".format(adds, changes))
            print("\nDatabase updated with {} new and {} modified entries - please see server log for more details".format(adds, changes))
        else:
            await ctx.send("No changes were made to the database - up to date!")
            print("\nNo changes were made to the database - up to date!")
        print("\n--------------------------------\n")

        server_db.commit()
        server_db.close()

    @setupdb.error
    async def db_perms_error(self, ctx, error):
        if isinstance(error, CheckFailure):
            messageAuthor = ctx.author.mention
            await ctx.send(f"Sorry {messageAuthor}, you are not allowed to do that. Only administrators may update the database")

    @commands.Cog.listener("on_member_join")
    async def member_join_update(self, member: discord.Member):
        channel = member.guild.system_channel
        await channel.send(f'Member {member.mention} has joined!')
        print("New user {} has joined! Updating database...\n".format(member))
        adds = 0
        changes = 0
        #Open our DB, create if doesn't exist.

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
            c.execute('''SELECT * FROM users WHERE id=?''', (member.id,))
            row = c.fetchone()
            # If the user does not exist, we'll create them and add to the database
            if row == None:
                #If the member has no nickname, we'll set it as N/A
                if member.nick == None:
                    try:
                        users = [member.id, member.name, member.discriminator, 'N/A', member.top_role.name]
                        c.execute('''INSERT INTO users (id, name, discriminator, nick, top_role) VALUES (?,?,?,?,?);''', users)
                        c.execute('''INSERT INTO discipline (strikes, kicks, banned, bans) VALUES (?,?,?,?);''', 0, 0, 0, 0)
                        print("User {} successfully added to the database;".format(users[1]))
                        print(users)
                        print("--------------------------------")
                        adds += 1
                    except:
                        print("Error inserting user {} in database".format(users[1]))
                else:
                    try:
                        c.execute('''INSERT INTO users (id, name, discriminator, nick, top_role) VALUES (?,?,?,?,?);''', users)
                        c.execute('''INSERT INTO discipline (strikes, kicks, banned, bans) VALUES (?,?,?,?);''', 0, 0, 0, 0)
                        print("User {} successfully added to the database;".format(users[1]))
                        print(users)
                        print("--------------------------------")
                        adds += 1
                    except:
                        print("Error inserting user {} in database".format(users[1]))
      


            else:
                if users[3] == row[3]:
                    print("User {} already in database and no changes to be made, skipping...".format(users[1]))
                elif users[3] != row[3] and users[3] != None:
                    try:
                        c.execute('''INSERT INTO users (nick) VALUES (?);''', users[3])
                        print("User {} updated successfully".format(users[1]))
                        changes += 1
                    except:
                        print("Error editing user {}".format(users[1]))
                elif users[3] == None and row[3] != "N/A":
                    print(row[3])
                    try:
                        c.execute('''INSERT INTO users (nick) VALUES ('N/A');''')
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

        server_db.commit()
        server_db.close()


def setup(bot):
    bot.add_cog(dbLaunch(bot))