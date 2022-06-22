from discord.ext import commands
from discord.commands import slash_command
from discord.channel import VoiceChannel
import discord
import asyncio
import os
from google.cloud import texttospeech

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'gcp-key.json'
tts_client = texttospeech.TextToSpeechClient()

class TextToSpeech(commands.Cog)
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener(name='on_message')
    async def read_message(self, message):
        if message.guild.voice_client is None and message.author.voice is not None:
            await message.author.voice.channel.connect()
        elif message.guild.voice_client:
            text = message.content
            text = text.replace('\n', '、')
            
            while message.guild.voice_client.is_playing():
                await asyncio.sleep(0.5)
            filename = f'tmp/{str(message.guild.voice_client.channel.id)}.mp3'
            self.__tts(filename, text)
            message.guild.voice_client.play(discord.FFmpegPCMAudio(filename))

    def __tts(filename, message):
        synthesis_input = texttospeech.SynthesisInput(text=message)
        voice = texttospeech.VoiceSelectionParams(
                language_code='ja-JP', name='ja-JP-Standard-A'
                )
        audio_config = texttospeech.AudioConfig(
                audio_encoding=texttospeech.AudioEncoding.MP3, speaking_rate=1.2
                )
        response = tts_client.synthesize_speech(
                input=synthesis_input, voice=voice, audio_config=audio_config
                )
        with open(filename, 'wb') as out:
            out.write(response.audio_content)
