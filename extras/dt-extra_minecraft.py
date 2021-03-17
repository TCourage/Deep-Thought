import discord, random, array, sqlite3, math
from discord import User
from discord.ext import commands
from discord.ext.commands import Bot, has_permissions, CheckFailure
from mcstatus import MinecraftServer

#####################################################
#  Minecraft module. This is optional. Allows       #
#  Discord server admins to set a Minecraft server  #
#  (which saves to the users database), and allows  #
#  users to check the server's status (among other  #
#  details).                                        #
#                                                   #
# Version 1.0.1                                     #
#####################################################

class MineCraft_Module(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["mcserver", "mc", "server"], pass_context = True, description = "Shows the info for the current Minecraft server", help = "Shows the current Minecraft server info.", brief = "Minecraft Server Status")
    async def minecraft(self, ctx, args = None):
        #Open our DB
        server_db = sqlite3.connect('users.db')
        c = server_db.cursor()
        try: #Check our DB to see if a server is set, get the details if yes
            c.execute('''SELECT server_address FROM minecraft;''')
            row = c.fetchone()
            server_address = row[0]
        except:
            embed = discord.Embed(title = "Error!")
            embed.add_field(name = "No server found in database, or there was an error getting data", value = "Please run `minecraft_server [address]` to set your server's details (must have Discord server admin priviliges)")
            c.execute('''CREATE TABLE minecraft(server_address text, op1 text DEFAULT "None", op2 text DEFAULT "None", op0 text DEFAULT "None", op3 text DEFAULT "None", op4 text DEFAULT "None", op5 text DEFAULT "None");''') 
            await ctx.channel.send (embed = embed)
        if args == None or args == "status" or args == "stat":
            try:
                server = MinecraftServer.lookup(server_address)  #grab server details
                status = server.status()
                ping = server.ping()
                ping = math.trunc(ping)
                players = []
                if status.players.online != 0:
                    for i in status.players.sample:
                        players.append(i.name)
                    player_list = "`\n`".join(players)

                if status.players.online != 0:
                    embed = discord.Embed(title="Minecraft Server Status:", color = 0x00ff00)
                    embed.add_field(name = "Server Address:", value = f"`{server_address}`", inline = False)
                    embed.add_field(name = "Online Status:", value = "`Online`", inline = False)
                    embed.add_field(name = "Minecraft Version:", value = f"`{status.version.name}`", inline = False)
                    embed.add_field(name = "Ping:", value = f"`{ping} ms`", inline = False)
                    embed.add_field(name = f"Playing now ({status.players.online}/{status.players.max}):", value = f"`{player_list}`", inline = False)
                    await ctx.channel.send(embed=embed)
                else:
                    embed = discord.Embed(title="Minecraft Server Status:", color = 0x00ff00)
                    embed.add_field(name = "Server Address:", value = f"`{server_address}`", inline = False)
                    embed.add_field(name = "Online Status:", value = "`Online`", inline = False)
                    embed.add_field(name = "Minecraft Version:", value = f"`{status.version.name}`", inline = False)
                    embed.add_field(name = "Ping:", value = f"`{ping} ms`", inline = False)
                    embed.add_field(name = f"Playing now ({status.players.online}/{status.players.max}):", value = "`None`", inline = False)
                    await ctx.channel.send(embed=embed)
                    

            except:
                embed = discord.Embed(title="Minecraft Server Status:", color = 0xff0000)
                embed.add_field(name = "Server Address:", value = f"`{server_address}`", inline = False)
                embed.add_field(name = "Status:", value = "`Offline`", inline = False)
                embed.add_field(name = "Minecraft Version", value = "`N/A`", inline = False)
                embed.add_field(name = "Ping:", value = "`N/A`", inline = False)
                embed.add_field(name = f"Playing now (0/0):", value = "`None`", inline = False)
                await ctx.channel.send(embed=embed)

        elif args == "whitelist":
            opcount = 0
            c.execute ('''SELECT op0, op1, op2, op3, op4, op5 FROM minecraft''')
            row = c.fetchone()
            ops = []
            await ctx.send ("Pinging Minecraft ops - User needs added to whitelist!")
            for i in row:
                if i != "None":
                    user = await ctx.guild.fetch_member(i)
                    await ctx.send (f"{user.mention}")
                    opcount += 1
            if opcount == 0:
                await ctx.send ("Hmm, looks like nobody setup ops yet. Ask a Discord server admin for assistance")




        
        #Write changes and close the DB
        server_db.commit()
        server_db.close()

        
    @commands.command(aliases=["mc_server_setup", "mcserversetup", "minecraftserver", "mcadmin", "mc_admin"], pass_context = True, description = "Sets the current Minecraft server in the database", help = "Set Minecraft server address", brief = "Setup Minecraft Server")
    @commands.has_permissions(administrator = True)
    async def minecraft_server(self, ctx, args = None, member: discord.Member = None):
        #Open our DB
        server_db = sqlite3.connect('users.db')
        c = server_db.cursor()
        if args == None:
            await ctx.send ("You must enter a server address to update the database with!")
        elif args == "op":  
            if member == None: #gotta tag someone
                await ctx.send("Please tag a user to log their op powers")
            else:
                y = 0
                g = 0
                c.execute ('''SELECT op0, op1, op2, op3, op4, op5 FROM minecraft''')  #grab our list of OPs
                row = c.fetchone()
                for i in row:
                    if i != "None":
                        g = int(i)  #convert the string to int to compare to SQL data
                    
                    if g == member.id:
                        if g == member.id:
                            await ctx.send("User is already an op!")
                            #Write changes and close the DB
                            server_db.commit()
                            server_db.close()
                            return
                    elif i != "None":
                        y += 1
                    elif i == "None":
                        if y == 0:
                            c.execute ('''UPDATE minecraft SET op0 = (?)''', (member.id,))
                            await ctx.send (f"{member.mention} successfully added as op!")
                            #Write changes and close the DB
                            server_db.commit()
                            server_db.close()
                            return
                        elif y == 1:
                            c.execute ('''UPDATE minecraft SET op1 = (?)''', (member.id,))
                            await ctx.send (f"{member.mention} successfully added as op!")
                            #Write changes and close the DB
                            server_db.commit()
                            server_db.close()
                            return
                        elif y == 2:
                            c.execute ('''UPDATE minecraft SET op2 = (?)''', (member.id,))
                            await ctx.send (f"{member.mention} successfully added as op!")
                            #Write changes and close the DB
                            server_db.commit()
                            server_db.close()
                            return
                        elif y == 3:
                            c.execute ('''UPDATE minecraft SET op3 = (?)''', (member.id,))
                            await ctx.send (f"{member.mention} successfully added as op!")
                            #Write changes and close the DB
                            server_db.commit()
                            server_db.close()
                            return
                        elif y == 4:
                            c.execute ('''UPDATE minecraft SET op4 = (?)''', (member.id,))
                            await ctx.send (f"{member.mention} successfully added as op!")
                            #Write changes and close the DB
                            server_db.commit()
                            server_db.close()
                            return
                        elif y == 5:
                            c.execute ('''UPDATE minecraft SET op5 = (?)''', (member.id,))
                            await ctx.send (f"{member.mention} successfully added as op!")
                            #Write changes and close the DB
                            server_db.commit()
                            server_db.close()
                            return
                        else:
                            await ctx.send ("Too many ops already! Submit a ticket to GitHub and we can look into this issue with you.")

            #Write changes and close the DB
            server_db.commit()
            server_db.close()

        elif args == "deop":  ################################  DEOP SECTION DISABLED FOR NOW
            trigger = 0  # a delete trigger
            #Open our DB
            server_db = sqlite3.connect('users.db')
            c = server_db.cursor()

            if member == None: #gotta tag someone
                await ctx.send("Please tag a user to log their removed op powers")
            else:
                y = 0
                c.execute ('''SELECT op0, op1, op2, op3, op4, op5 FROM minecraft''')  #grab our list of OPs
                row = c.fetchone()
                for i in row:
                    if i != "None":
                        g = int(i)  #convert the string to int to compare to SQL data
                        if g == member.id:
                            c.execute ('''UPDATE minecraft SET op0 = "None"''',)
                            await ctx.send (f"{member.mention} had their op powers removed.")
                            trigger = 1
                if trigger == 0:
                    await ctx.send (f"{member.mention} was never an op!")
            #Write changes and close the DB
            server_db.commit()
            server_db.close()
            return
  
        else:
            c.execute ('''SELECT server_address FROM minecraft;''')
            row = c.fetchone()
            if row == None:
                c.execute ('''INSERT INTO minecraft (server_address) VALUES (?);''', (args,))
                await ctx.send (f"Confirmed - new Minecraft server address is {args}")
            else:
                c.execute('''UPDATE minecraft SET server_address = (?)''', (args,))
                await ctx.send (f"Confirmed - new Minecraft server address is {args}")


        #Write changes and close the DB
        server_db.commit()
        server_db.close()

    @minecraft_server.error
    async def minecraft_server_error(self, ctx, error):
        if isinstance(error, CheckFailure):
            messageAuthor = ctx.author.mention
            await ctx.send(f"Sorry {messageAuthor}, you are not allowed to do that. Only administrators may change the Minecraft server.")


def setup(bot):
    bot.add_cog(MineCraft_Module(bot))
