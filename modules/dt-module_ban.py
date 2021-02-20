import discord
from discord import User
from discord.ext import commands
from discord.ext.commands import Bot, has_permissions, CheckFailure

class banModule(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context = True)
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, user_name: discord.Member, days = 1, reason = "reasons"):
        if user_name == None or user_name == ctx.message.author:
            await ctx.send("You cannot ban yourself")
            return
        try:
            await ctx.guild.ban(user_name, reason = reason)
            if days > 1:
                await ctx.send(f"{user_name} is now banned for {days} days for {reason}")
            else:
                await ctx.send(f"{user_name} is now banned for {days} day for {reason}")
        except discord.Forbidden:
            messageAuthor = ctx.author.mention
            await ctx.send(f"Sorry {messageAuthor}, you are not allowed to do that")

    @ban.error
    async def ban_error(error, ctx, user_name: discord.Member):
        if isinstance(error, CheckFailure):
            await ctx.send(f"Sorry {messageAuthor}, you are not allowed to do that")
#####    UNBAN CURRENTLY BROKEN -- DOES NOT WORK   #####
#####  Likely will require SQL Server to function  #####
'''
    @commands.command(pass_context = True)
    async def unban(self, ctx, id: int):
        userID = bot.get_user(id)
        try:
            await ctx.guild.unban(userID)
            await ctx.send(f"{user_name} is now unbanned")
        except discord.Forbidden:
            messageAuthor = ctx.author.mention
            await ctx.send(f"Sorry {messageAuthor}, you are not allowed to do that")
'''

def setup(bot):
    bot.add_cog(banModule(bot))
