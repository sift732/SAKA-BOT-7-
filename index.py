import nextcord
from nextcord.ext import commands
import os
import traceback
import os
import importlib.util

bot = commands.Bot(command_prefix='!', intents=nextcord.Intents.all())

def load_cogs():
    load_directories = ["admin"]

    total_file_count = 0
    success_load_count = 0

    for load_directory in load_directories:
        files = [f for f in os.listdir(load_directory) if os.path.isfile(os.path.join(load_directory, f)) and f.endswith(".py")]

        print(f'ディレクトリ："{load_directory}"から読み込めたファイル数：{len(files)}')
        total_file_count += len(files)

        for file in files:
            if file.endswith('.py'):
                try:
                    cog_name = file[:-3]
                    cog_module = importlib.import_module(f'{load_directory}.{cog_name}')
                    cog_class = getattr(cog_module, cog_name.capitalize())

                    bot.add_cog(cog_class(bot))
                    success_load_count += 1
                except Exception as e:
                    print(f'エラー: {e}')
    print(f'BOTに同期できたファイル数：{success_load_count}')

    print(f'ロード成功ファイル数：{total_file_count}')

@bot.event
async def on_ready():
    print(f'{bot.user}としてログインしました')
    print(f"nextcordのバージョン{nextcord.__version__}")

    guild_count = len(bot.guilds)
    member_count = sum(guild.member_count for guild in bot.guilds)

    await bot.change_presence(activity=nextcord.Activity(
        type=nextcord.ActivityType.watching, 
        name=f"導入数：{guild_count}｜累計メンバー：{member_count}"
    ))

token = os.getenv("TOKEN")
try:
    load_cogs()
    bot.run(token)
except nextcord.errors.PrivilegedIntentsRequired:
    print("intentが無効")
except Exception as e:
    print(f"エラー: {e}")