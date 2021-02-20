import discord, random, array
from discord import User
from discord.ext import commands
from discord.ext.commands import Bot

'''
Our Dice rolling module

Currently allows for up to 99 virutal dice of any size to be rolled
'''

class rollModule(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context = True)
    async def roll(self, ctx, dice = "roll"):
        if dice == "roll":
            rand = random.randint(1, 6)
            await ctx.send(f"1x d6: {rand}")
            embed=discord.Embed(title=f"{rand}:")
            embed.add_field(name=f"1x d6", value=f"{rand}", inline=False)
            await ctx.channel.send(embed=embed)

        if dice[0] == 'd' or dice[0] == 'D': #check for one die
            num = int(dice[1:])
            rand = random.randint(1, num)
            embed=discord.Embed(title=f"{rand}:")
            embed.add_field(name=f"1x d{num}", value=f"{rand}", inline=False)
            await ctx.channel.send(embed=embed)
            
        if dice[0] != 'd' or dice[0] != 'D':  #check for multiple Dice
            if dice[1] == 'd' or dice[1] == 'D':  #xdyy, where x is the number of dice
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
                embed=discord.Embed(title=f"{rand}")
                embed.add_field(name=f"{numDice}x d{num}: {rand}", value=f"{numArray}", inline=False)
                await ctx.channel.send(embed=embed)

            if dice[2] == 'd' or dice[2] == 'D':  #xxdyy, where x is the number of dice
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
                embed=discord.Embed(title=f"{rand}")
                embed.add_field(name=f"{numDice}x d{num}: {rand}", value=f"{numArray}", inline=False)
                await ctx.channel.send(embed=embed)


def setup(bot):
    bot.add_cog(rollModule(bot))
