import discord
import json
from discord.ext import commands
from config import GREEN


class Verification(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.is_owner()
    async def verification(self, ctx, emoji, role: discord.Role):

        emb = discord.Embed(colour=GREEN, title="Developer Access",
                            description="In order to get developer access react with the 🎮 emoji below!\n\n")
        msg = await ctx.channel.send(embed=emb)
        await msg.add_reaction(emoji)

        with open('./React.json') as json_file:
            data = json.load(json_file)

            new_react_role = {'role_name': role.name,
                              'role_id': role.id,
                              'emoji': emoji,
                              'message_id': msg.id}

            data.append(new_react_role)

        with open('./React.json', 'w') as f:
            json.dump(data, f, indent=4)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.member.bot:
            pass
        else:
            with open('./React.json') as react_file:
                data = json.load(react_file)
                for x in data:
                    if x['emoji'] == payload.emoji.name:
                        role = discord.utils.get(self.bot.get_guild(
                            payload.guild_id).roles, id=x['role_id'])
                        await payload.member.add_roles(role)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        guild = await self.bot.fetch_guild(payload.guild_id)
        member = await guild.fetch_member(payload.user_id)
        with open('./React.json') as react_file:
            data = json.load(react_file)
            for x in data:
                if x['emoji'] == payload.emoji.name:
                    role = discord.utils.get(self.bot.get_guild(
                        payload.guild_id).roles, id=x['role_id'])

                    await member.remove_roles(role)

def setup(bot):
    bot.add_cog(Verification(bot))
