#####   USER MANAGEMENT MODULE   ####
##  Includes the ban, unban, kick, ##
## and strike commands. This is a  ##
## vital part of Deep Thought and  ##
## should only be edited if you    ##
## what you are doing.             ##
#####################################


import discord, string, sqlite3
from discord import User
from discord.ext import commands
from discord.ext.commands import Bot, has_permissions, CheckFailure

class UserManagement_Module(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    #Ban module. Code is pretty self-explanitory
    @commands.command(nam = "ban", pass_context = True, description = "Allows you to ban users from the server. Also updates the server database, if applicable.", brief = "BAN PEOPLE")
    @commands.has_permissions(ban_members=True) #This ensures only people who are allowed to ban others can use this command
    async def ban(self, ctx, user_name: discord.Member, *, reason = None):

        #All the DB part of this was moved to the DB module
        
        if user_name == ctx.message.author:  #Prevent user from banning themself
            await ctx.send("You cannot ban yourself")
            return
        elif user_name == None: #Forces you to tag someone
            await ctx.send("Please tag someone to ban")
            return
        elif reason != None: #If a reason is given
            await ctx.send(f"{user_name.mention} is now banned, reason(s); {reason}")
            await ctx.guild.ban(user_name)
        else: #If a reason is not given
            await ctx.send(f"{user_name.mention} is now banned")
            await ctx.guild.ban(user_name)

    #If the user doesn't have the permissions to ban people, they're told they can't
    @ban.error
    async def ban_error(self, ctx, error):
        if isinstance(error, CheckFailure):
            messageAuthor = ctx.author.mention
            await ctx.send(f"Sorry {messageAuthor}, you are not allowed to do that")
    


    #Kick module. Also pretty self-explanitory
    @commands.command(name="kick", aliases=["boot", "toss"], description = "Allows you to kick users from the server. Also updates the server database, if applicable.", brief = "KICK PEOPLE")
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, user_name: discord.Member, *, reason = None):
        #Open our DB
        server_db = sqlite3.connect('users.db')
        c = server_db.cursor()
        c.execute('''SELECT kicks FROM discipline WHERE id = (?);''', (user_name.id,)) #Gets the number of times they've been kicked before
        num_kicks = c.fetchone()  #fetches the SQL row
        kicks = num_kicks[0] #create a variable to hold the number of kicks

        if reason != None: #If a reason is given
            kicks += 1 #add to the kick counter
            c.execute('''UPDATE discipline SET kicks = (?) WHERE id = (?);''', (kicks, user_name.id,)) #apply kick count
            await ctx.send(f"{user_name.mention} has been kicked, reason(s); {reason}")
            await ctx.guild.kick(user_name)
        else: #If a reason is not given
            kicks += 1
            c.execute('''UPDATE discipline SET kicks = (?) WHERE id = (?);''', (kicks, user_name.id,))
            await ctx.send(f"{user_name} has been kicked")
            await ctx.guild.kick(user_name)

        #Write changes and close the DB
        server_db.commit()
        server_db.close()
    
    #Similar to the ban error above
    @kick.error
    async def kick_error(self, ctx, error):
        if isinstance(error, CheckFailure):
            messageAuthor = ctx.author.mention
            await ctx.send(f"Sorry {messageAuthor}, you are not allowed to do that")



    #Strike module. Gives strikes. Can only be used by people who are allowed to ban
    @commands.command(name = "strike", aliases = ["warn", "warning"], pass_context = True, description = "Gives users strikes. At 3 strikes, the user is banned from the server.", brief = "GIVE PEOPLE STRIKES")
    @commands.has_permissions(ban_members=True) #This ensures only people who are allowed to ban others can use this command
    async def strike(self, ctx, user_name: discord.Member, reason = None):

        #Open our DB
        server_db = sqlite3.connect('users.db')
        c = server_db.cursor()
        c.execute('''SELECT strikes, bans FROM discipline WHERE id = (?);''', (user_name.id,)) #Gets the number of strikes they've gotten before
        num_strikes = c.fetchone()  #fetches the SQL row
        strikes = num_strikes[0] #create a variable to hold the number of strikes
        bans = num_strikes[1] #variable to hold number of bans
        
        if user_name == ctx.message.author:  #Prevent user from giving themself strikes
            await ctx.send("You cannot give yourself strikes")
            return
        elif user_name == None: #Forces you to tag someone
            await ctx.send("Please tag someone to give them a strike")
            return
        elif reason != None: #If a reason is given
            strikes += 1 #add to the strike counter
            if strikes == 3:
                await ctx.send(f"{user_name.mention} has received three strikes, and is now banned. (Strike reason: {reason}")
                await ctx.guild.ban(user_name)
            else:
                c.execute('''UPDATE discipline SET strikes = (?) WHERE id = (?);''', (strikes, user_name.id,)) #apply strike count
                await ctx.send(f"{user_name.mention} has been given a strike, reason(s); {reason}. This is strike #{strikes}")

        else: #If a reason is not given
            strikes += 1 #add to the strike counter
            if strikes == 3:
                await ctx.send(f"{user_name.mention} has received three strikes, and is now banned.")
                await ctx.guild.ban(user_name)
            else:
                c.execute('''UPDATE discipline SET strikes = (?) WHERE id = (?);''', (strikes, user_name.id,)) #apply strike count
                await ctx.send(f"{user_name.mention} has been given a strike. This is strike #{strikes}")

        #Write changes and close the DB
        server_db.commit()
        server_db.close()

    #If the user doesn't have the permissions to ban people, they're told they can't give strikes either
    @strike.error
    async def strike_error(self, ctx, error):
        if isinstance(error, CheckFailure):
            messageAuthor = ctx.author.mention
            await ctx.send(f"Sorry {messageAuthor}, you are not allowed to do that")


def setup(bot):
    bot.add_cog(UserManagement_Module(bot))
