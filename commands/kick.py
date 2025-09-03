from discord.ext import commands
from discord import app_commands
from typing import Optional
import discord


class Kick(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="kick", description="[ADMIN ONLY] Kick people!")
    @app_commands.describe(member="Member to kick")
    @app_commands.describe(reason="Reason for kick")
    async def kick(self, interaction:discord.Interaction, member:discord.Member, reason:Optional[str]):
        if not interaction.user.guild_permissions.administrator:
            reason = "No Reason Provided" if reason is None else reason
            guild_name = interaction.guild.name
            await interaction.response.defer(thinking=True, ephemeral=True)
            embed = discord.Embed(title="Kick", description=f"You have been kicked from {guild_name}")
            embed.add_field(name = "Reason", value=f"{reason}")
            try:
                await member.send(embed=embed)
            except:
                pass

            try:
                await member.kick(reason=reason, delete_message_days=7)
                await interaction.followup.send(f"{member.mention} was kicked.")

            except:
                await interaction.followup.send(f"Failed. Please kick {member.mention} yourself.")

        else:
            await interaction.response.send_message("Haha, no", ephemeral=True)


    @kick.error
    async def kick_error(self, interaction:discord.Interaction, error):
        if isinstance(error, app_commands.MissingPermissions):
            await interaction.response.send_message("Haha, no", ephemeral=True)
        else:
            await interaction.response.send_message("Failed. Please kick {member.mention} yourself.", ephemeral=True)


async def setup(bot:commands.Bot) -> None:
  await bot.add_cog(Kick(bot))
