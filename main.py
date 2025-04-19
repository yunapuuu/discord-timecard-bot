import discord
from discord import app_commands
from dotenv import load_dotenv
import os

# 環境変数の読み込み
load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

# ボットの設定
intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

# ボット起動時の処理
@client.event
async def on_ready():
    print(f'ボットが起動しました: {client.user}')
    try:
        synced = await tree.sync(guild=discord.Object(id='1361387017715322982'))  # ギルドコマンドを同期
        print(f'コマンドを同期しました: {synced}')
    except Exception as e:
        print(f'同期エラー: {e}')

# /start コマンド
@tree.command(name="start", description="練習開始を記録します")
async def start(interaction: discord.Interaction):
    # セレクトメニューを作成
    select = discord.ui.Select(
        custom_id="team_select",
        placeholder="チームを選択してください",
        options=[
            discord.SelectOption(label="チームA", value="TeamA"),
            discord.SelectOption(label="チームB", value="TeamB"),
        ]
    )
    view = discord.ui.View()
    view.add_item(select)
    
    await interaction.response.send_message("チームを選択してください！", view=view, ephemeral=True)

# セレクトメニューの処理
@client.event
async def on_interaction(interaction: discord.Interaction):
    if interaction.type == discord.InteractionType.component and interaction.data["custom_id"] == "team_select":
        selected_team = interaction.data["values"][0]
        await interaction.response.send_message(f"チーム{selected_team}練習開始します！を送信しました！", ephemeral=True)
        await interaction.channel.send(f"チーム{selected_team}練習開始します！")

# ボットを起動
client.run(DISCORD_TOKEN)