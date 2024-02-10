import nextcord
from nextcord.ext import commands
from datetime import datetime

class Activity(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(name="server_active", description="サーバー内のユーザーのアクティビティステータスを表示します")
    async def server_ac(self, ctx):
        if isinstance(ctx.channel, nextcord.DMChannel):
            error_embed = nextcord.Embed(title="エラー", description="DMでこのコマンドは使用できません。", color=nextcord.Color.red())
            await ctx.send(embed=error_embed)
            return

        embed = nextcord.Embed(title="サーバー内のアクティビティステータス", color=0x00ff00)

        activity_count = 0

        for member in ctx.guild.members:
            if not member.bot and member.activities:
                for activity in member.activities:
                    if isinstance(activity, nextcord.Spotify):
                        activity_details = f"\n曲名：{activity.title}\nアーティスト：{activity.artist}\nアルバム：{activity.album}"
                    elif isinstance(activity, nextcord.Streaming):
                        activity_details = f"\n配信名：{activity.name}\n配信URL：{activity.url}"
                    elif isinstance(activity, nextcord.Game):
                        playtime = (datetime.utcnow() - activity.start).total_seconds() // 3600
                        activity_details = f"\nゲーム名：{activity.name}\nプレイ時間：{playtime} 時間"
                    elif isinstance(activity, nextcord.CustomActivity):
                        activity_details = activity.name if activity.name else "詳細なし"
                    else:
                        activity_details = getattr(activity, "details", "詳細なし")

                    embed.add_field(name=f"{member.name} - {activity.type.name}", value=activity_details, inline=False)
                    activity_count += 1

        if activity_count == 0:
            await ctx.send("アクティビティのユーザーは存在しません")
            return

        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Activity(bot))
