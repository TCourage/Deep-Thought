import discord
from discord import User
from discord.ext import commands
from discord.ext.commands import Bot

class banModule(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context = True)
    async def ban(self, ctx, user_name: discord.User, days = 1, reason = "reasons"):
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

#####  UNBAN CURRENTLY BROKEN -- DOES NOT WORK  #####
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
