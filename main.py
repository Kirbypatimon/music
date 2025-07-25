import discord
from discord import app_commands
from discord.ext import commands
import os

intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True

bot = commands.Bot(command_prefix="/", intents=intents)
tree = bot.tree  # スラッシュコマンド用

AUDIO_DIR = "audio"

@bot.event
async def on_ready():
    await tree.sync()
    print(f"Logged in as {bot.user} and synced commands.")

@tree.command(name="join", description="ボイスチャンネルに参加します")
async def join(interaction: discord.Interaction):
    if interaction.user.voice:
        await interaction.user.voice.channel.connect()
        await interaction.response.send_message("ボイスチャンネルに接続しました！")
    else:
        await interaction.response.send_message("先にボイスチャンネルに参加してください。")

@tree.command(name="play", description="音声を再生します")
@app_commands.describe(name="再生したいファイル名（拡張子不要）")
async def play(interaction: discord.Interaction, name: str):
    if not interaction.guild.voice_client:
        await interaction.response.send_message("先に `/join` でボイスチャンネルに接続してください。")
        return

    filename = f"{name}.mp3"
    filepath = os.path.join(AUDIO_DIR, filename)

    if not os.path.exists(filepath):
        await interaction.response.send_message(f"ファイル「{filename}」が見つかりません。")
        return

    if interaction.guild.voice_client.is_playing():
        interaction.guild.voice_client.stop()

    interaction.guild.voice_client.play(discord.FFmpegPCMAudio(filepath))
    await interaction.response.send_message(f"「{name}」を再生します。")

@tree.command(name="list", description="再生可能な音声一覧を表示します")
async def list_files(interaction: discord.Interaction):
    if not os.path.exists(AUDIO_DIR):
        await interaction.response.send_message("音楽フォルダがありません。")
        return

    files = [f[:-4] for f in os.listdir(AUDIO_DIR) if f.endswith(".mp3")]
    if files:
        await interaction.response.send_message("再生可能なファイル一覧：\n" + "\n".join(files))
    else:
        await interaction.response.send_message("音楽ファイルがありません。")

@tree.command(name="leave", description="ボイスチャンネルから退出します")
async def leave(interaction: discord.Interaction):
    if interaction.guild.voice_client:
        await interaction.guild.voice_client.disconnect()
        await interaction.response.send_message("ボイスチャンネルから切断しました。")
    else:
        await interaction.response.send_message("ボイスチャンネルに接続していません。")

bot.run(os.environ["DISCORD_TOKEN"])
