from discord.ext import commands
from discord import FFmpegPCMAudio


class Music(commands.Cog):    
    def __init__(self, bot):
        self.bot = bot

    def cog_check(self, ctx):
        if not ctx.guild:
            raise commands.NoPrivateMessage('This command can\'t be used in DM channels.')
        return True
    
    async def cog_command_error(self, ctx, error):
        await ctx.send("An error occurred: {}".format(str(error)))

    @commands.command(name='join', invoke_without_subcommand=True, description="The bot joins your voice channel.")
    @commands.has_role("DJ")
    async def _join(self, ctx):
        if ctx.author.voice:
            destination = ctx.author.voice.channel
            if ctx.voice_client:
                await ctx.voice_client.move_to(destination)
                await ctx.send("Bot joined.")
            else:
                await destination.connect()
                await ctx.send("Bot joined.")
        else:
            await ctx.send("You must be in a voice channel first.")

    @commands.command(name='leave', aliases=['disconnect', "stop"], description="The bot leaves your voice channel.")
    @commands.has_role("DJ")
    async def _leave(self, ctx):
        if ctx.voice_client:
            await ctx.guild.voice_client.disconnect()
            await ctx.send("Bot left.")
        else:
            await ctx.send('Not connected to any voice channel.')

    @commands.command(name="play", description="The bot joins your voice channel if you are not already in one and plays the audio/video from the provided url.")
    @commands.has_role("DJ")
    async def _play(self, ctx, url=None):
        if url == None:
            await ctx.send('You must provide a link providing an audio or video track.')
        else:
            await ctx.invoke(self._join)
            source = FFmpegPCMAudio(url)
            ctx.voice_client.play(source)
            await ctx.send("Playing audio track.")