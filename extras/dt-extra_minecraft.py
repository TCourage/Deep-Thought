import discord, random, array, sqlite3
from discord import User
from discord.ext import commands
from discord.ext.commands import Bot, has_permissions, CheckFailure
from mcstatus import MinecraftServer

'''
Our Dice rolling module

Currently allows for up to 99 virutal dice of any size to be rolled
'''

class MineCraft_Module(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["mcserver", "mc", "server"], pass_context = True, description = "Shows the info for the current Minecraft server", help = "Shows the current Minecraft server info.", brief = "Minecraft Server Status")
    async def minecraft(self, ctx):
        ONLINE = str("""```css\nThis is some colored Text```""")
        OFFLINE = str("""```css\nThis is some colored Text```""")
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
            await ctx.channel.send (embed = embed)

        try:
            server = MinecraftServer.lookup(server_address)  #grab server details
            status = server.status()
            ping = server.ping()
            print (status.raw)
            players = []
            for i in status.players.sample:
                players.append(i.name)
            print (players)
            player_list = "\n".join(players)

            embed = discord.Embed(title="Minecraft Server Status:", color = 0x00ff00)
            embed.add_field(name = "Server Address:", value = f"`{server_address}`", inline = False)
            embed.add_field(name = "Online Status:", value = "Online", inline = False)
            embed.add_field(name = "Minecraft Version:", value = f"{status.version.name}", inline = False)
            embed.add_field(name = "Ping:", value = f"{ping}", inline = False)
            embed.add_field(name = f"Playing now ({status.players.online}/{status.players.max}):", value = f"{player_list}", inline = False)
            await ctx.channel.send(embed=embed)

        except:
            embed = discord.Embed(title="Minecraft Server Status:", color = 0xff0000)
            embed.add_field(name = "Server Address:", value = f"`{server_address}`", inline = False)
            embed.add_field(name = "Status:", value = "Offline", inline = False)
            embed.add_field(name = "Minecraft Version", value = "N/A", inline = False)
            embed.add_field(name = "Ping:", value = "N/A", inline = False)
            embed.add_field(name = f"Playing now (0/0):", value = "None", inline = False)
            await ctx.channel.send(embed=embed)



        
        #Write changes and close the DB
        server_db.commit()
        server_db.close()

        
    @commands.command(alises=["mc_server_setup", "mc_server_setup", "mcserversetup", "minecraftserver"], pass_context = True, description = "Sets the current Minecraft server in the database", help = "Set Minecraft server address", brief = "Setup Minecraft Server")
    @commands.has_permissions(administrator = True)
    async def minecraft_server(self, ctx, args = None):
        #Open our DB
        server_db = sqlite3.connect('users.db')
        c = server_db.cursor()
        print (args)

        if args == None:
            await ctx.send ("You must enter a server address to update the database with!")
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
        print ("hello world")


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
