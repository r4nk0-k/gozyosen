from discord.ext import commands
from discord.channel import VoiceChannel
import discord
import asyncio
import os
import yaml
from google.cloud import texttospeech

settings_info = yaml.load(open('settings.yaml').read(), Loader=yaml.SafeLoader)['text_to_speech']
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = settings_info['gcp_credential_path']
tts_client = texttospeech.TextToSpeechClient()
ENABLE_CHANNELS = settings_info['enable_channels']

class TextToSpeech(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.voice_client = None

        self.speed = 1
        self.pitch = 1

    @commands.Cog.listener(name='on_message')
    async def read_message(self, message):
        # 指定されたチャンネルのメッセージのみ再生
        if message.channel.id not in ENABLE_CHANNELS:
            return

        # 発言者がボイチャにいない
        if message.author.voice is None:
            return

        if self.voice_client is None:
            await message.author.voice.channel.connect()
            self.voice_client = message.guild.voice_client

        # 発言者と同じボイチャに移動する
        if self.voice_client.channel.id is not message.author.voice.channel.id:
            await self.voice_client.move_to(message.author.voice.channel)

        text = message.content
        
        if text.startswith('&'):
            return

        text = text.replace('\n', '、')
        
        while message.guild.voice_client.is_playing():
            await asyncio.sleep(0.5)
        filename = f'tmp/{str(message.guild.voice_client.channel.id)}.mp3'

        # 月間400万文字超えたら金が発生するので文字数制限を一応
        if len(text) >= 200:
            text = text[0:200]

        self.__tts(filename, text)
        message.guild.voice_client.play(discord.FFmpegPCMAudio(filename))

    # 誰もいなくなったら退出
    @commands.Cog.listener(name='on_voice_state_update')
    async def disconnect_with_empty_channel(self, member, before, after):
        if self.voice_client is None:
            return

        if before.channel.id == self.voice_client.channel.id and len(before.channel.members) == 1:
            await self.voice_client.disconnect()
            self.voice_client = None

    # 読み上げ速度・ピッチの変換
    # gcpのttxが受け取れる範囲に丸めこむ
    @commands.command()
    async def voice_pitch(self, ctx, pitch):
        self.pitch = max(-20 ,min(20 ,float(pitch)))

    @commands.command()
    async def voice_speed(self, ctx, speed):
        self.speed = max(0.25 ,min(4.0 ,float(speed)))

    def __tts(self, filename, message):
        synthesis_input = texttospeech.SynthesisInput(text=message)
        voice = texttospeech.VoiceSelectionParams(
                language_code='ja-JP', name='ja-JP-Standard-A'
                )
        audio_config = texttospeech.AudioConfig(
                audio_encoding=texttospeech.AudioEncoding.MP3,
                speaking_rate=self.speed,
                pitch=self.pitch
                )
        response = tts_client.synthesize_speech(
                input=synthesis_input, voice=voice, audio_config=audio_config
                )
        with open(filename, 'wb') as out:
            out.write(response.audio_content)

def setup(bot):
    return bot.add_cog(TextToSpeech(bot))
