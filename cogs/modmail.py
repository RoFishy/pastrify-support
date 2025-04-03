import discord
from discord.ext import commands
from datetime import datetime
from dotenv import dotenv_values

config = dotenv_values(".env")
GUILD_ID = config["SERVER_ID"]
SUPPORT_CATEGORY = config["SUPPORT_CATEGORY"]

class Modmail(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{__name__} loaded successfully")

    @commands.Cog.listener()
    async def on_message(self, message):
        if str(message.channel.type) == "private":
            if message.author == self.client.user:
                return
            else:
                try:
                    guild = self.client.get_guild(int(GUILD_ID))
                except Exception as e:
                    print(e)
                channel = None
                try:
                    for ch in guild.channels:
                        if not isinstance(ch, discord.TextChannel):
                            continue
                        if ch.topic == str(message.author.id):
                            channel = ch
                            break
                except Exception as e:
                    print(e)

                if channel is None:
                    category = discord.utils.get(guild.categories, id=int(SUPPORT_CATEGORY))
                    channel = await guild.create_text_channel((str("ticket-"+message.author.name)),category=category)
                    await channel.edit(topic = message.author.id)
                    user_embed = discord.Embed(
                        title="Ticket Opened",
                        description="Thank you for contacting Pastrify's support team today, a member of our support team will be with you shortly.\n\nIn the meantime, please describe your issue in detail so we can assist you as soon as possible.",
                        timestamp=datetime.utcnow(),
                        color=discord.Color.pink()
                    )
                    await message.author.send(embed=user_embed)
                    Embed = discord.Embed(
                        title = f"{message.author.name} has created a new Modmail thread",
                        description = "**Message: **" + message.content + "\n\n**Support Commands:**\n* `!close` - Closes the ticket\n* `!name <name>` - Changes the name of the ticket\n* `!reply <message>` - Replies to the user",
                        timestamp=datetime.utcnow(),
                        color = discord.Color.pink()
                    )
                    await channel.send(embed=Embed, content="@here")
                
                else:
                    content = message.content[:-2]
                    content = content[2:]
                    Embed = discord.Embed(
                        title = "",
                        description = message.content,
                        timestamp=datetime.utcnow(),
                        color = discord.Color.pink()
                    )
                    Embed.set_author(                                
                            name = f"{message.author.name}",
                            icon_url = f"{message.author.avatar}",)
                    await channel.send(embed= Embed)
                    await message.add_reaction("✅")


async def setup(client):
    await client.add_cog(Modmail(client))