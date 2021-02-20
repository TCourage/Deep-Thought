import discord
from discord.ext import commands
from discord.ext.commands import Bot, has_permissions, CheckFailure

class kickModule(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="kick", aliases=["boot"], pass_context = True)
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, user_name: discord.Member, reason = "reasons unknown (Check #mod-actions for details)"):
        await ctx.guild.kick(user_name, reason = reason)
        await ctx.send(f"{user_name} was kicked for {reason}")
    
    @kick.error
    async def kick_error(error, ctx, user_name: discord.Member):
        if isinstance(error, CheckFailure):
            await ctx.send(f"Sorry {messageAuthor}, you are not allowed to do that")

def setup(bot):
    bot.add_cog(kickModule(bot))
