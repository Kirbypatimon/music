import discord
from discord.ext import commands
import os

intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True

bot = commands.Bot(command_prefix='/', intents=intents)

AUDIO_DIR = "audio"

@bot.command()
async def join(ctx):
    if ctx.author.voice:
        await ctx.author.voice.channel.connect()
        await ctx.send("ボイスチャンネルに接続しました！")
    else:
        await ctx.send("先にボイスチャンネルに参加してください。")

@bot.command()
async def play(ctx, *, name: str):
    if not ctx.voice_client:
        await ctx.send("先に /join でボイスチャンネルに接続してください。")
        return

    filename = f"{name}.mp3"
    filepath = os.path.join(AUDIO_DIR, filename)

    if not os.path.exists(filepath):
        await ctx.send(f"ファイル「{filename}」が見つかりません。")
        return

    if ctx.voice_client.is_playing():
        ctx.voice_client.stop()

    # FFmpegで再生
    ctx.voice_client.play(discord.FFmpegPCMAudio(filepath))
    await ctx.send(f"「{name}」を再生します。")

@bot.command()
async def list(ctx):
    if not os.path.exists(AUDIO_DIR):
        await ctx.send("音楽フォルダがありません。")
        return

    files = [f[:-4] for f in os.listdir(AUDIO_DIR) if f.endswith(".mp3")]
    if files:
        await ctx.send("再生可能なファイル一覧：\n" + "\n".join(files))
    else:
        await ctx.send("音楽ファイルがありません。")

@bot.command()
async def leave(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send("ボイスチャンネルから切断しました。")
    else:
        await ctx.send("ボイスチャンネルに接続していません。")

bot.run(os.environ["DISCORD_TOKEN"])
