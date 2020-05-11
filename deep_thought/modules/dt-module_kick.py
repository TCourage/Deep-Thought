import discord
from discord.ext import commands
from discord.ext.commands import Bot

class kickModule(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="kick", aliases=["boot"], pass_context = True)
    async def kick(self, ctx, user_name: discord.User, reason = "reasons"):
        try:
            await ctx.guild.kick(user_name, reason = reason)
            await ctx.send(f"{user_name} was kicked for {reason}")
        except discord.Forbidden:
            messageAuthor = ctx.author.mention
            await ctx.send(f"Sorry {messageAuthor}, you are not allowed to do that")

def setup(bot):
    bot.add_cog(kickModule(bot))
