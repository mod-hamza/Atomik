from discord.ext import commands
from discord import app_commands
from typing import Optional
import discord


class Ban(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="ban", description="[ADMIN ONLY] Banish people!")
    @app_commands.describe(member="Member to ban")
    @app_commands.describe(reason="Reason for ban")
    async def ban(self, interaction:discord.Interaction, member:discord.Member, reason:Optional[str]):
        if not interaction.user.guild_permissions.administrator:
            reason = "No Reason Provided" if reason is None else reason
            guild_name = interaction.guild.name
            await interaction.response.defer(thinking=True, ephemeral=True)
            embed = discord.Embed(title="Ban", description=f"You have been banned from {guild_name}")
            embed.add_field(name = "Reason", value=f"{reason}")
            try:
                await member.send(embed=embed)
            except:
                pass

            try:
                await member.ban(reason=reason, delete_message_days=7)
                await interaction.followup.send(f"{member.mention} was banned.")

            except:
                await interaction.followup.send(f"Failed. Please ban {member.mention} yourself.")

        else:
            await interaction.response.send_message("Haha, no", ephemeral=True)


    @ban.error
    async def ban_error(self, interaction:discord.Interaction, error):
        if isinstance(error, app_commands.MissingPermissions):
            await interaction.response.send_message("Haha, no", ephemeral=True)
        else:
            await interaction.response.send_message("Failed. Please ban {member.mention} yourself.", ephemeral=True)


async def setup(bot:commands.Bot) -> None:
  await bot.add_cog(Ban(bot))
