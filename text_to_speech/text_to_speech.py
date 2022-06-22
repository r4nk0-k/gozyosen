from discord.ext import commands
from discord.channel import VoiceChannel
import discord
import asyncio
import os
from google.cloud import texttospeech

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'gcp-key.json'
tts_client = texttospeech.TextToSpeechClient()
ENABLE_CHANNELS = [766330592441794642] # todo settings.json的なのに出す

class TextToSpeech(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.voice_client = None;

    @commands.Cog.listener(name='on_message')
    async def read_message(self, message):
        # 指定されたチャンネルのメッセージのみ再生
        if message.channel.id not in ENABLE_CHANNELS:
            return

        if message.guild.voice_client is None and message.author.voice is not None:
            await message.author.voice.channel.connect()
            self.voice_client = message.guild.voice_client
        elif message.guild.voice_client:
            text = message.content
            text = text.replace('\n', '、')
            
            while message.guild.voice_client.is_playing():
                await asyncio.sleep(0.5)
            filename = f'tmp/{str(message.guild.voice_client.channel.id)}.mp3'
            self.__tts(filename, text)
            message.guild.voice_client.play(discord.FFmpegPCMAudio(filename))

    # 誰もいなくなったら退出
    @commands.Cog.listener(name='on_voice_state_update')
    async def disconnect_with_empty_channel(self, member, before, after):
        if self.voice_client is None:
            return

        if before.channel.id == self.voice_client.channel.id and not before.channel.members:
            await self.voice_client.disconnect()
            self.voice_client = None

    def __tts(self, filename, message):
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

def setup(bot):
    return bot.add_cog(TextToSpeech(bot))
