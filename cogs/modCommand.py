import discord
from discord.ext import commands
from datetime import datetime
import chat_exporter
import io

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
                            await ctx.message.add_reaction("✅")
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
            transcript = await chat_exporter.export(ctx.channel, bot=self.client)
            log_channel = self.client.get_channel(1357463048570405016)
            await ctx.channel.delete()
            embed = discord.Embed(title = "❌ | Ticket Closed", description = "Ticket has been closed by Pastrify support.", timestamp = datetime.utcnow(), color = discord.Color.red())
            await user.send(embed=embed)
            if transcript is None:
                return
            transcript_file = discord.File(
                io.BytesIO(transcript.encode()),
                filename=f"transcript-{ctx.channel.name}.html"
            )
            embed = discord.Embed(title = "📩 | Ticket Log", color=discord.Color.pink())
            embed.add_field(name="Ticket Opener", value=f"<@{ctx.channel.topic}>", inline=False)
            embed.add_field(name="Ticket Closer", value=f"<@{ctx.author.id}>", inline=False)
            embed.add_field(name="Ticket Name", value=f"{ctx.channel.name}", inline=False)
            embed.set_footer(text="Powered by Pastrify", icon_url="https://cdn.discordapp.com/attachments/1324151965579477035/1356349347440361582/noFilter.webp?ex=67ec3e44&is=67eaecc4&hm=5efa5737a1263967fd5659d96d8b41522d2edeeb27e594edf4baf728664b038d&")
            await log_channel.send(embed=embed, file=transcript_file)

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