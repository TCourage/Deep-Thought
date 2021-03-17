#####   USER MANAGEMENT MODULE   ####
##  Includes the ban, unban, kick, ##
## and strike commands. This is a  ##
## vital part of Deep Thought and  ##
## should only be edited if you    ##
## what you are doing.             ##
##                                 ##
## Ver. 1.0.0                      ##
#####################################


import discord, string, sqlite3, datetime
from discord import User
from discord.ext import commands
from discord.ext.commands import Bot, has_permissions, CheckFailure

class UserManagement_Module(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    #Ban module. Code is pretty self-explanitory
    @commands.command(name = "ban", pass_context = True, description = "Allows you to ban users from the server. Also updates the server database, if applicable.", brief = "BAN PEOPLE")
    @commands.has_permissions(ban_members=True) #This ensures only people who are allowed to ban others can use this command
    async def ban(self, ctx, user_name: discord.Member = None, *, reason = None):

        #Most of the DB part of this was moved to the DB module

        reasons = ''.join(reason)
        
        if user_name == ctx.message.author:  #Prevent user from banning themself
            await ctx.send("You cannot ban yourself")
            return
        elif user_name == None: #Forces you to tag someone
            await ctx.send("Please tag someone to ban them")
            return
        elif reason != None: #If a reason is given
            server_db = sqlite3.connect('users.db')
            c = server_db.cursor()
            await ctx.send(f"{user_name.mention} is now banned, reason(s); {reasons}")
            c.execute('''UPDATE discipline SET ban_reason = (?) WHERE id = (?);''', (reasons, user_name.id,))
            server_db.commit()
            server_db.close()
            await ctx.guild.ban(user_name)
        else: #If a reason is not given
            await ctx.guild.ban(user_name)
            await ctx.send(f"{user_name.mention} is now banned")

    #If the user doesn't have the permissions to ban people, they're told they can't
    @ban.error
    async def ban_error(self, ctx, error):
        if isinstance(error, CheckFailure):
            messageAuthor = ctx.author.mention
            await ctx.send(f"Sorry {messageAuthor}, you are not allowed to do that")
    


    #Kick module. Also pretty self-explanitory
    @commands.command(name="kick", aliases=["boot", "toss"], description = "Allows you to kick users from the server. Also updates the server database, if applicable.", brief = "KICK PEOPLE")
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, user_name: discord.Member = None, *, reason = None):
        #Open our DB
        server_db = sqlite3.connect('users.db')
        c = server_db.cursor()

        if user_name == ctx.message.author:  #Prevent user from banning themself
            await ctx.send("You cannot kick yourself")
            return
        elif user_name == None: #Forces you to tag someone
            await ctx.send("Please tag someone to kick them")
            return
        elif reason != None: #If a reason is given
            c.execute('''SELECT kicks FROM discipline WHERE id = (?);''', (user_name.id,)) #Gets the number of times they've been kicked before
            num_kicks = c.fetchone()  #fetches the SQL row
            kicks = num_kicks[0] #create a variable to hold the number of kicks
            kicks += 1 #add to the kick counter
            c.execute('''UPDATE discipline SET kicks = (?) WHERE id = (?);''', (kicks, user_name.id,)) #apply kick count
            await ctx.send(f"{user_name.mention} has been kicked, reason(s); {reason}")
            await ctx.guild.kick(user_name)
        else: #If a reason is not given
            c.execute('''SELECT kicks FROM discipline WHERE id = (?);''', (user_name.id,)) #Gets the number of times they've been kicked before
            num_kicks = c.fetchone()  #fetches the SQL row
            kicks = num_kicks[0] #create a variable to hold the number of kicks
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
    async def strike(self, ctx, user_name: discord.Member = None, *, reason = None):

        #Open our DB
        server_db = sqlite3.connect('users.db')
        c = server_db.cursor()
        now = datetime.datetime.now()
        date = now.strftime("%Y %B %d, %H:%M:%S")
        author = ctx.message.author
        
        if user_name == author:  #Prevent user from giving themself strikes
            await ctx.send("You cannot give yourself strikes")
            return
        elif user_name == None: #Forces you to tag someone
            await ctx.send("Please tag someone to give them a strike")
            return
        elif reason != None: #If a reason is given
            c.execute('''SELECT strikes, bans FROM discipline WHERE id = (?);''', (user_name.id,)) #Gets the number of strikes they've gotten before
            num_strikes = c.fetchone()  #fetches the SQL row
            strikes = num_strikes[0] #create a variable to hold the number of strikes
            strikes += 1 #add to the strike counter
            reasons = ''.join(reason)

            if strikes == 3:
                embed = discord.Embed(title=f"Strike given to {user_name.name}:")
                embed.add_field(name=f"Strike #3", value=f"{user_name.name} has been banned. Reason(s): {reasons}", inline=False)
                embed.set_footer(text=f"Action performed by {author}")
                c.execute('''UPDATE discipline SET ban_reason = (?) WHERE id = (?);''', (reasons, user_name.id,))
                #Write changes and close the DB
                server_db.commit()
                server_db.close()
                await ctx.guild.ban(user_name)
                await ctx.send(embed = embed)
                return
            elif strikes == 1:
                c.execute('''UPDATE discipline SET strikes = (?), strike1_reason = (?), strike1_date = (?), strike1_givenby = (?) WHERE id = (?);''', (strikes, reasons, date, author.name, user_name.id,)) #apply strike count
                embed = discord.Embed(title=f"Strike given to {user_name.name}:")
                embed.add_field(name=f"Strike #1", value=f"{user_name.name} now has 1 strike. Reason(s): {reasons}", inline=False)
                embed.set_footer(text=f"Action performed by {author}")
                await ctx.send(embed = embed)
            elif strikes == 2:
                c.execute('''UPDATE discipline SET strikes = (?), strike2_reason = (?), strike2_date = (?), strike2_givenby = (?) WHERE id = (?);''', (strikes, reasons, date, author.name, user_name.id,)) #apply strike count
                embed = discord.Embed(title=f"Strike given to {user_name.name}:")
                embed.add_field(name=f"Strike #2", value=f"{user_name.name} now has 2 strikes. Reason(s): {reasons}  -  Careful! One more strike and you'll be banned!", inline=False)
                embed.set_footer(text=f"Action performed by {author}")
                await ctx.send(embed = embed)
        else: #If a reason is not given
            c.execute('''SELECT strikes FROM discipline WHERE id = (?);''', (user_name.id,)) #Gets the number of strikes they've gotten before
            num_strikes = c.fetchone()  #fetches the SQL row
            strikes = num_strikes[0] #create a variable to hold the number of strikes
            strikes += 1 #add to the strike counter
            if strikes == 3:
                embed = discord.Embed(title=f"Strike given to {user_name.name}:")
                embed.add_field(name=f"Strike #3", value=f"{user_name.name} has been banned.", inline=False)
                embed.set_footer(text=f"Action performed by {author}")
                await ctx.guild.ban(user_name)
                await ctx.send(embed = embed)
            elif strikes == 1:
                c.execute('''UPDATE discipline SET strikes = (?), strike1_date = (?), strike1_givenby = (?) WHERE id = (?);''', (strikes, date, author.name, user_name.id,)) #apply strike count
                embed = discord.Embed(title=f"Strike given to {user_name.name}:")
                embed.add_field(name=f"Strike #1", value=f"{user_name.name} now has 1 strike.", inline=False)
                embed.set_footer(text=f"Action performed by {author}")
                await ctx.send(embed = embed)
            elif strikes == 2:
                c.execute('''UPDATE discipline SET strikes = (?), strike2_date = (?), strike2_givenby = (?) WHERE id = (?);''', (strikes, date, author.name, user_name.id,)) #apply strike count
                embed = discord.Embed(title=f"Strike given to {user_name.name}:")
                embed.add_field(name=f"Strike #2", value=f"{user_name.name} now has 2 strikes. One more and you'll be banned!", inline=False)
                #embed.set_footer(text=f"Action performed by {author}")
                await ctx.send(embed = embed)
        #Write changes and close the DB
        server_db.commit()
        server_db.close()

    #If the user doesn't have the permissions to ban people, they're told they can't give strikes either
    @strike.error
    async def strike_error(self, ctx, error):
        if isinstance(error, CheckFailure):
            messageAuthor = ctx.author.mention
            await ctx.send(f"Sorry {messageAuthor}, you are not allowed to do that")
        print(error)

    #Strike REMOVAL module. REMOVES strikes. Can only be used by people who are allowed to ban
    @commands.command(name = "removestrike", aliases = ["removewarning"], pass_context = True, description = "Removes users strikes.", brief = "REMOVE STRIKES")
    @commands.has_permissions(ban_members=True) #This ensures only people who are allowed to ban others can use this command
    async def removestrike(self, ctx, user_name: discord.Member = None):

        #Open our DB
        server_db = sqlite3.connect('users.db')
        c = server_db.cursor()
        
        if user_name == ctx.message.author:  #Prevent user from removing their own strikes
            await ctx.send("You cannot remove your own strikes")
            return
        elif user_name == None: #Forces you to tag someone
            await ctx.send("Please tag someone to remove one of their strikes")
            return
        else: 
            c.execute('''SELECT strikes FROM discipline WHERE id = (?);''', (user_name.id,)) #Gets the number of strikes they've gotten before
            num_strikes = c.fetchone()  #fetches the SQL row
            strikes = num_strikes[0] #create a variable to hold the number of strikes

            if strikes == 0:
                await ctx.send(f"{user_name.mention} has no strikes! Nothing to remove!")
            else:
                strikes -= 1
                if strikes == 1:
                    c.execute('''UPDATE discipline SET strikes = (?), strike2_date = "None", strike2_reason = "None", strike2_givenby = "None" WHERE id = (?);''', (strikes, user_name.id,)) #apply new lower strike count
                    embed = discord.Embed(title=f"Strike removed from {user_name.name}:")
                    embed.add_field(name=f"Strike {strikes + 1} removed.", value=f"{user_name.name} now has {strikes} strike.", inline=False)
                    embed.set_footer(text=f"Action performed by {ctx.message.author}")
                    await ctx.send(embed = embed)
                elif strikes == 0:
                    c.execute('''UPDATE discipline SET strikes = (?), strike1_date = "None", strike1_reason = "None", strike1_givenby = "None" WHERE id = (?);''', (strikes, user_name.id,)) #apply new lower strike count
                    embed = discord.Embed(title=f"Strike removed from {user_name.name}:")
                    embed.add_field(name=f"Strike {strikes + 1} removed.", value=f"{user_name.name} now has {strikes} strikes.", inline=False)
                    embed.set_footer(text=f"Action performed by {ctx.message.author}")
                    await ctx.send(embed = embed)


        #Write changes and close the DB
        server_db.commit()
        server_db.close()

    #If the user doesn't have the permissions to ban people, they're told they can't give strikes either
    @strike.error
    async def removestrike_error(self, ctx, error):
        if isinstance(error, CheckFailure):
            messageAuthor = ctx.author.mention
            await ctx.send(f"Sorry {messageAuthor}, you are not allowed to do that")


    @commands.command(name = "strikes", aliases = ["warns", "warnings"], pass_context = True, description = "Check how many strikes you have. At 3 strikes, you are banned from the server.", brief = "CHECK YOUR STRIKES")
    async def strikes(self, ctx, user_name: discord.Member = None):

        #Open our DB
        server_db = sqlite3.connect('users.db')
        c = server_db.cursor()

        if user_name == ctx.message.author:  #Check your own strikes
            c.execute('''SELECT strikes, strike1_reason, strike1_date, strike1_givenby, strike2_reason, strike2_date, strike2_givenby FROM discipline WHERE id = (?);''', (user_name.id,)) #Gets their number of strikes
            num_strikes = c.fetchone()  #fetches the SQL row
            strikes = num_strikes[0] #create a variable to hold the number of strikes

            if strikes == 0:
                embed = discord.Embed(title=f"{user_name.name}'s strikes:")
                embed.add_field(name=f"Strikes: {strikes}", value=f"{user_name.name} has {strikes} strikes.", inline=False)
                embed.set_footer(text=f"Strikes checked by {ctx.message.author}")
                await ctx.send(embed = embed)
            elif strikes == 1:
                strike1_reason = num_strikes[1]
                strike1_date = num_strikes[2]
                strike1_givenby = num_strikes[3]
                embed = discord.Embed(title=f"{user_name.name}'s strikes:")
                embed.add_field(name=f"Strikes: {strikes}", value=f"{user_name.name} has {strikes} strike.", inline=False)
                embed.add_field(name=f"Strike 1 ({strike1_date}):", value=f"Given by: {strike1_givenby}\nReason: {strike1_reason}", inline=False)
                embed.set_footer(text=f"Strikes checked by {ctx.message.author}")
                await ctx.send(embed = embed)
            else:
                strike1_reason = num_strikes[1]
                strike1_date = num_strikes[2]
                strike1_givenby = num_strikes[3]
                strike2_reason = num_strikes[4]
                strike2_date = num_strikes[5]
                strike2_givenby = num_strikes[6]
                embed = discord.Embed(title=f"{user_name.name}'s strikes:")
                embed.add_field(name=f"Strikes: {strikes}", value=f"{user_name.name} has {strikes} strikes.", inline=False)
                embed.add_field(name=f"Strike 1 ({strike1_date}):", value=f"Given by: {strike1_givenby}\nReason: {strike1_reason}", inline=False)
                embed.add_field(name=f"Strike 2 ({strike2_date}):", value=f"Given by: {strike2_givenby}\nReason: {strike2_reason}", inline=False)
                embed.set_footer(text=f"Strikes checked by {ctx.message.author}")
                await ctx.send(embed = embed)

        elif user_name == None: #Again, checks your own
            c.execute('''SELECT strikes, strike1_reason, strike1_date, strike1_givenby, strike2_reason, strike2_date, strike2_givenby FROM discipline WHERE id = (?);''', (ctx.message.author.id,)) #Gets their number of strikes
            num_strikes = c.fetchone()  #fetches the SQL row
            strikes = num_strikes[0] #create a variable to hold the number of strikes
            user_name = ctx.message.author
            if strikes == 0:
                embed = discord.Embed(title=f"{user_name.name}'s strikes:")
                embed.add_field(name=f"Strikes: {strikes}", value=f"{user_name.name} has {strikes} strikes.", inline=False)
                embed.set_footer(text=f"Strikes checked by {ctx.message.author}")
                await ctx.send(embed = embed)
            elif strikes == 1:
                strike1_reason = num_strikes[1]
                strike1_date = num_strikes[2]
                strike1_givenby = num_strikes[3]
                embed = discord.Embed(title=f"{user_name.name}'s strikes:")
                embed.add_field(name=f"Strikes: {strikes}", value=f"{user_name.name} has {strikes} strike.", inline=False)
                embed.add_field(name=f"Strike 1 ({strike1_date}):", value=f"Given by: {strike1_givenby}\nReason: {strike1_reason}", inline=False)
                embed.set_footer(text=f"Strikes checked by {ctx.message.author}")
                await ctx.send(embed = embed)
            else:
                strike1_reason = num_strikes[1]
                strike1_date = num_strikes[2]
                strike1_givenby = num_strikes[3]
                strike2_reason = num_strikes[4]
                strike2_date = num_strikes[5]
                strike2_givenby = num_strikes[6]
                embed = discord.Embed(title=f"{user_name.name}'s strikes:")
                embed.add_field(name=f"Strikes: {strikes}", value=f"{user_name.name} has {strikes} strikes.", inline=False)
                embed.add_field(name=f"Strike 1 ({strike1_date}):", value=f"Given by: {strike1_givenby}\nReason: {strike1_reason}", inline=False)
                embed.add_field(name=f"Strike 2 ({strike2_date}):", value=f"Given by: {strike2_givenby}\nReason: {strike2_reason}", inline=False)
                embed.set_footer(text=f"Strikes checked by {ctx.message.author}")
                await ctx.send(embed = embed)
        else: #otherwise if a username was supplied;
            c.execute('''SELECT strikes, strike1_reason, strike1_date, strike1_givenby, strike2_reason, strike2_date, strike2_givenby FROM discipline WHERE id = (?);''', (user_name.id,)) #Gets their number of strikes
            num_strikes = c.fetchone()  #fetches the SQL row
            strikes = num_strikes[0] #create a variable to hold the number of strikes
            if not (user_name.nick): #if the users real discord username was supplied
                if strikes == 0:
                    embed = discord.Embed(title=f"{user_name.name}'s strikes:")
                    embed.add_field(name=f"Strikes: {strikes}", value=f"{user_name.name} has {strikes} strikes.", inline=False)
                    embed.set_footer(text=f"Strikes checked by {ctx.message.author}")
                    await ctx.send(embed = embed)
                elif strikes == 1:
                    strike1_reason = num_strikes[1]
                    strike1_date = num_strikes[2]
                    strike1_givenby = num_strikes[3]
                    embed = discord.Embed(title=f"{user_name.name}'s strikes:")
                    embed.add_field(name=f"Strikes: {strikes}", value=f"{user_name.name} has {strikes} strike.", inline=False)
                    embed.add_field(name=f"Strike 1 ({strike1_date}):", value=f"Given by: {strike1_givenby}\nReason: {strike1_reason}", inline=False)
                    embed.set_footer(text=f"Strikes checked by {ctx.message.author}")
                    await ctx.send(embed = embed)
                else:
                    strike1_reason = num_strikes[1]
                    strike1_date = num_strikes[2]
                    strike1_givenby = num_strikes[3]
                    strike2_reason = num_strikes[4]
                    strike2_date = num_strikes[5]
                    strike2_givenby = num_strikes[6]
                    embed = discord.Embed(title=f"{user_name.name}'s strikes:")
                    embed.add_field(name=f"Strikes: {strikes}", value=f"{user_name.name} has {strikes} strikes.", inline=False)
                    embed.add_field(name=f"Strike 1 ({strike1_date}):", value=f"Given by: {strike1_givenby}\nReason: {strike1_reason}", inline=False)
                    embed.add_field(name=f"Strike 2 ({strike2_date}):", value=f"Given by: {strike2_givenby}\nReason: {strike2_reason}", inline=False)
                    embed.set_footer(text=f"Strikes checked by {ctx.message.author}")
                    await ctx.send(embed = embed)
            else:  #if the users server nickname was supplied instead
                if strikes == 0:
                    embed = discord.Embed(title=f"{user_name.name}'s strikes:")
                    embed.add_field(name=f"Strikes: {strikes}", value=f"{user_name.name} has {strikes} strikes.", inline=False)
                    embed.set_footer(text=f"Strikes checked by {ctx.message.author}")
                    await ctx.send(embed = embed)
                elif strikes == 1:
                    strike1_reason = num_strikes[1]
                    strike1_date = num_strikes[2]
                    strike1_givenby = num_strikes[3]
                    embed = discord.Embed(title=f"{user_name.name}'s strikes:")
                    embed.add_field(name=f"Strikes: {strikes}", value=f"{user_name.name} has {strikes} strike.", inline=False)
                    embed.add_field(name=f"Strike 1 ({strike1_date}):", value=f"Given by: {strike1_givenby}\nReason: {strike1_reason}", inline=False)
                    embed.set_footer(text=f"Strikes checked by {ctx.message.author}")
                    await ctx.send(embed = embed)
                else:
                    strike1_reason = num_strikes[1]
                    strike1_date = num_strikes[2]
                    strike1_givenby = num_strikes[3]
                    strike2_reason = num_strikes[4]
                    strike2_date = num_strikes[5]
                    strike2_givenby = num_strikes[6]
                    embed = discord.Embed(title=f"{user_name.name}'s strikes:")
                    embed.add_field(name=f"Strikes: {strikes}", value=f"{user_name.name} has {strikes} strikes.", inline=False)
                    embed.add_field(name=f"Strike 1 ({strike1_date}):", value=f"Given by: {strike1_givenby}\nReason: {strike1_reason}", inline=False)
                    embed.add_field(name=f"Strike 2 ({strike2_date}):", value=f"Given by: {strike2_givenby}\nReason: {strike2_reason}", inline=False)
                    embed.set_footer(text=f"Strikes checked by {ctx.message.author}")
                    await ctx.send(embed = embed)
                

def setup(bot):
    bot.add_cog(UserManagement_Module(bot))
