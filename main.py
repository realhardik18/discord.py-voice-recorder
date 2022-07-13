import discord
from discord.ext import commands
from discord.ext.audiorec import NativeVoiceClient
from secrets import token
import random

intents = discord.Intents().all()
client = commands.Bot(command_prefix="!", intents=intents)
client.remove_command('help')


@client.event
async def on_ready():
    print('im ready')


@client.command()
async def help(ctx):
    embedVar = discord.Embed(title="here are my commands!",
                             description="nuser **!join** to start the recording\nuser **!stop** to stop the recording", color=0x546e7a)
    await ctx.send(embed=embedVar)


@client.command()
async def join(ctx: commands.Context):
    channel: discord.VoiceChannel = ctx.author.voice.channel
    if ctx.voice_client is not None:
        return await ctx.voice_client.move_to(channel)
    await channel.connect(cls=NativeVoiceClient)
    await ctx.invoke(client.get_command('rec'))


@client.command()
async def test(ctx):
    await ctx.send('hello im alive!')


@client.command()
async def rec(ctx):
    ctx.voice_client.record(lambda e: print(f"Exception: {e}"))
    embedVar = discord.Embed(title="Started the Recording!",
                             description="use !stop to stop!", color=0x546e7a)
    await ctx.send(embed=embedVar)


@client.command()
async def stop(ctx: commands.Context):
    if not ctx.voice_client.is_recording():
        return
    await ctx.send(f'Stopping the Recording')

    wav_bytes = await ctx.voice_client.stop_record()

    # print(wav_bytes)
    name = str(random.randint(000000, 999999))
    with open(f'{name}.wav', 'wb') as f:
        f.write(wav_bytes)
    await ctx.voice_client.disconnect()


@rec.before_invoke
async def ensure_voice(ctx):
    if ctx.voice_client is None:
        if ctx.author.voice:
            await ctx.author.voice.channel.connect(cls=NativeVoiceClient)
        else:
            await ctx.send("You are not connected to a voice channel.")
            raise commands.CommandError(
                "Author not connected to a voice channel.")
    elif ctx.voice_client.is_playing():
        ctx.voice_client.stop()

client.run(token)
