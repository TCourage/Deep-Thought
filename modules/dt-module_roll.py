import discord
from discord import User
from discord.ext import commands
from discord.ext.commands import Bot
import random
import array

class rollModule(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context = True)
    async def roll(self, ctx, dice):
        if dice[0] == 'd' or dice[0] == 'D':
            num = int(dice[1:])
            rand = random.randint(1, num)
            await ctx.send(f"1x d{num}: {rand}")
        if dice[0] != 'd' or dice[0] != 'D':
            if dice[1] == 'd' or dice[1] == 'D':
                numDice = int(dice[0])
                num = int(dice[2:])
                numArray = [0] * numDice
                for x in range(numDice):
                    randNum = random.randint(1, num)
                    numArray[x] = randNum
                    if x == 0:
                        rand = randNum
                    else:
                        rand += randNum
                await ctx.send(f"{numDice}x d{num}: {rand}   {numArray}")

            if dice[2] == 'd' or dice[2] == 'D':
                numDice = int(dice[0:2])
                num = int(dice[3:])
                numArray = [0] * numDice
                for x in range(numDice):
                    randNum = random.randint(1, num)
                    numArray[x] = randNum
                    if x == 0:
                        rand = randNum
                    else:
                        rand += randNum
                await ctx.send(f"{numDice}x d{num}: {rand}   {numArray}")


def setup(bot):
    bot.add_cog(rollModule(bot))
