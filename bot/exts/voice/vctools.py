import discord
from discord.ext import commands

COG_DESCRIPTION = "A helpful voice channel extension that provides commands for better controlling your VC's."

BASE_DESCRIPTION = "Base VCTools command. For all commands, the `all` keyword can be used to use the command on all users in your current voice channel."

MOVE_DESCRIPTION = "Move users from one voice channel to another. Requires the `Move Members` permission."

MUTE_DESCRIPTION = "Mute one or more users while they are in voice channels. Requires the `Mute Members` permission."

UNMUTE_DESCRIPTION = "Unmute one or more users while they are in voice channels. Requires the `Mute Members` permission."
    
DEAFEN_DESCRIPTION = "Deafen one or more users while they are in voice channels. Requires the `Deafen Members` permission."

UNDEAFEN_DESCRIPTION = "Undeafen one or more users while they are in voice channels. Requires the `Deafen Members` permission."


class VCTools(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.vc.invoke_without_command = True
        self.description = COG_DESCRIPTION

    @commands.group(pass_context=True, description = BASE_DESCRIPTION)
    async def vc(self,ctx):
        await ctx.invoke(self.bot.get_command("help"), "VCTools")
    
    async def _changeState(self, ctx, users, state = {}):
        word = state["action_name"]
        converter = commands.MemberConverter()
        users = users.split(' ')
        all_users = False
        if 'all' in [u.lower() for u in users]:
            all_users = True
            if not ctx.author.voice:
                await ctx.reply(f"You can only {word} all members when you are in a voice channel")
                return
            users = ctx.author.voice.channel.members
        users = [await converter.convert(ctx, user) if type(user) != discord.Member else user for user in users]
        off_users = []

        for user in [ u for u in users ]:
            if user.voice:
                    await user.edit(**state)
            else:
                users.remove(user)
                off_users.append(user)
        
        stripped = word.rstrip('e')

        if all_users:
            await ctx.reply(f"{stripped.capitalize()}ed all users in {ctx.author.voice.channel}")
        else:
            await ctx.reply("%s%s" % (
                f"{stripped.capitalize()}ed users: {', '.join(map(str,users))}. " if len(users) > 0 else "",
                f"Users {', '.join(map(str,off_users))} were unable to be {stripped}ed, because they are not in a voice channel." if len(off_users) > 0 else ""
            ))

    @vc.command(aliases=['mv'], description=MOVE_DESCRIPTION)
    @commands.has_guild_permissions(move_members=True)
    async def move(self, ctx, channel, *, users):
        try:
            channel = await commands.VoiceChannelConverter().convert(ctx, channel)
        except commands.errors.ChannelNotFound:
            await ctx.reply(f'Could not find channel {channel}')
            return
        await self._changeState(ctx, users, { "action_name": "move", "voice_channel": channel })

    @vc.command(aliases=['m'], description=MUTE_DESCRIPTION)
    @commands.has_guild_permissions(mute_members=True)
    async def mute(self,ctx, *, users):
        await self._changeState(ctx, users, { "action_name": "mute", "mute": True })

    @vc.command(aliases=['um'], description=UNMUTE_DESCRIPTION)
    @commands.has_guild_permissions(mute_members=True)
    async def unmute(self,ctx, *, users):
        await self._changeState(ctx, users, { "action_name": "unmute", "mute": False })

    @vc.command(aliases=['dfn'], description=DEAFEN_DESCRIPTION)
    @commands.has_guild_permissions(deafen_members=True)
    async def deafen(self, ctx, *, users):
        await self._changeState(ctx, users, { "action_name": "deafen", "deafen": True })

    @vc.command(aliases=['udfn'], description=UNDEAFEN_DESCRIPTION)
    @commands.has_guild_permissions(deafen_members=True)
    async def undeafen(self, ctx, *, users):
        await self._changeState(ctx, users, { "action_name": "undeafen", "deafen": False })

def setup(bot):
    bot.add_cog(VCTools(bot))