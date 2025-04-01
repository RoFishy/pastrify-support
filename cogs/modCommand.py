import discord
from discord.ext import commands
from datetime import datetime

class modCommand(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.command()
    async def reply(self, ctx, *, message):
        try:
            if "!close" in message:
                pass
            else:
                if str(ctx.channel.type) == "private":
                    return
                else:
                    if ctx.author == self.client.user:
                        return
                    else:
                        if ctx.channel.topic is None:
                            return
                        if ctx.channel.topic.isdigit():
                            user = await ctx.guild.fetch_member(int(ctx.channel.topic))
                            Embed = discord.Embed(
                                title = "",
                                description=message,
                                timestamp = datetime.utcnow(),
                                color = discord.Color.green()
                            )
                            Embed.set_author(                                
                                name = f"{ctx.author.name}",
                                icon_url = f"{ctx.author.avatar}",)
                            await user.send(embed = Embed)
                        else:
                            return

        except Exception as e:
            print(e)

    @commands.command()
    async def close(self, ctx):
        user = await ctx.guild.fetch_member(int(ctx.channel.topic))
        if user is None:
            pass
        else:
            await ctx.channel.delete()
            embed = discord.Embed(title = "❌ | Ticket Closed", description = "Ticket has been closed by Pastrify support.", timestamp = datetime.utcnow(), color = discord.Color.red())
            await user.send(embed=embed)

    @commands.command()
    async def name(self, ctx, *, name : str):
        user = await ctx.guild.fetch_member(int(ctx.channel.topic))
        channel = ctx.channel
        if user is None:
            pass
        else:
            await channel.edit(name=name)

async def setup(client):
    await client.add_cog(modCommand(client))