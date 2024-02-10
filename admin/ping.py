import nextcord
from nextcord.ext import commands
import time

class Ping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(name="ping", description="応答速度を計測します")
    async def ping(self, ctx):
        embed = nextcord.Embed(title="計測中...", color=nextcord.Color.blurple())
        message = await ctx.send(embed=embed)

        start_time = time.time()
        await self.bot.wait_until_ready()
        end_time = time.time()

        ping = round((end_time - start_time) * 1000, 3)

        embed.title = "Pong!"
        embed.description = f"応答速度: {ping}ms"
        await message.edit(embed=embed)


def setup(bot):
    bot.add_cog(Ping(bot))
