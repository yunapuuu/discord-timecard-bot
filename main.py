import discord
from discord import app_commands, ui
from dotenv import load_dotenv
import os
import requests

# 環境変数の読み込み
load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

# ボットの設定
intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

# トークンの有効性テスト
async def test_token():
    headers = {
        'Authorization': f'Bot {DISCORD_TOKEN}',
        'User-Agent': 'practiceLoLBot/1.0 (contact: yunapuuu35@gmail.com)'
    }
    response = requests.get('https://discord.com/api/v10/users/@me', headers=headers)
    print(f'トークンテスト: ステータスコード={response.status_code}, レスポンス={response.json()}')

# 登録済みコマンドを確認
async def check_commands():
    headers = {
        'Authorization': f'Bot {DISCORD_TOKEN}',
        'User-Agent': 'practiceLoLBot/1.0 (contact: yunapuuu35@gmail.com)'
    }
    response = requests.get(
        'https://discord.com/api/v10/applications/1362981262473822439/guilds/1361387017715322982/commands',
        headers=headers
    )
    print(f'チェック結果: ステータスコード={response.status_code}, レスポンス={response.json()}')

# ギルドコマンドをクリア
async def clear_guild_commands():
    headers = {
        'Authorization': f'Bot {DISCORD_TOKEN}',
        'User-Agent': 'practiceLoLBot/1.0 (contact: yunapuuu35@gmail.com)'
    }
    response = requests.put(
        'https://discord.com/api/v10/applications/1362981262473822439/guilds/1361387017715322982/commands',
        headers=headers,
        json=[]  # 空のコマンドリストで上書き
    )
    print(f'ギルドコマンドクリア: ステータスコード={response.status_code}, レスポンス={response.json()}')

# 24時間稼働のエンドポイント作成
@app.route('/lolkdacustom0518', methods=['GET'])
def lol_kda_custom_0518():
    return jsonify({'message': 'Alive'}), 200

# ボット起動時の処理
@client.event
async def on_ready():
    print(f'ボットが起動しました: {client.user}')
    print(f'登録済みのコマンド: {[cmd.name for cmd in tree.get_commands()]}')
    await test_token()
    await check_commands()
    try:
        await tree.sync(guild=discord.Object(id=1361387017715322982))
        print('コマンドの同期が完了しました')
        # テストメッセージを送信
        # channel = client.get_channel(1362778081974161448)
        # if channel:
        #     await channel.send("ボットがチャンネルにアクセスできました！")
        # else:
        #     print("チャンネルが見つかりません")
    except discord.errors.HTTPException as e:
        print(f'HTTPエラー: {e.status}, {e.text}')
    except discord.errors.Forbidden as e:
        print(f'権限エラー: {e}')
    except Exception as e:
        print(f'その他のエラー: {e}')

# /start コマンド
@tree.command(name="start", description="練習開始を記録します", guild=discord.Object(id=1361387017715322982))
async def start(interaction: discord.Interaction):
    select = discord.ui.Select(
        custom_id="team_select",
        placeholder="チームを選択してください",
        options=[
            discord.SelectOption(label="チームA", value="A"),
            discord.SelectOption(label="チームB", value="B"),
            discord.SelectOption(label="チームC", value="C"),
        ]
    )
    view = discord.ui.View()
    view.add_item(select)
    await interaction.response.send_message("チームを選択してください！", view=view, ephemeral=True)

# /test コマンド（デバッグ用）
@tree.command(name="test", description="テストコマンド", guild=discord.Object(id=1361387017715322982))
async def test(interaction: discord.Interaction):
    await interaction.response.send_message("テスト成功！")

# /end コマンド
@tree.command(name="end", description="練習終了を記録します", guild=discord.Object(id=1361387017715322982))
async def end(interaction: discord.Interaction):
    select = discord.ui.Select(
        custom_id="team_select_end",  # startと区別するために異なるcustom_id
        placeholder="チームを選択してください",
        options=[
            discord.SelectOption(label="チームA", value="A"),
            discord.SelectOption(label="チームB", value="B"),
            discord.SelectOption(label="チームC", value="C"),
        ]
    )
    view = discord.ui.View()
    view.add_item(select)
    await interaction.response.send_message("終了するチームを選択してください！", view=view, ephemeral=True)

# セレクトメニューの処理
@client.event
async def on_interaction(interaction: discord.Interaction):
    if interaction.type == discord.InteractionType.component:
        # 実行ユーザーのメンションを取得
        user_mention = interaction.user.mention 
        if interaction.data["custom_id"] == "team_select":
            selected_team = interaction.data["values"][0]
            await interaction.response.send_message(f"{user_mention} チーム{selected_team}練習開始します！を送信しました！", ephemeral=True)
            await interaction.channel.send(f"{user_mention} チーム{selected_team}練習開始します！")
        elif interaction.data["custom_id"] == "team_select_end":
            selected_team = interaction.data["values"][0]
            await interaction.response.send_message(f"{user_mention} チーム{selected_team}練習終了しました！を送信しました！", ephemeral=True)
            await interaction.channel.send(f"{user_mention} チーム{selected_team}練習終了しました！")

# エラーハンドリング
@tree.error
async def on_command_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
    await interaction.response.send_message(f"エラー: {error}", ephemeral=True)

# ボットを起動
client.run(DISCORD_TOKEN)