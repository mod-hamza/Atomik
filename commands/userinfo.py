from discord.ext import commands
from discord import app_commands
import discord

class UserInfo(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        super().__init__()
        self.bot=bot

    @app_commands.command(name="user_info", description="Get information about a user")
    async def user_info(self, interaction: discord.Interaction, member:discord.Member) -> None:
        embed = discord.Embed(title=f"💡 | User Information")
        embed.description = f"Here is some information about {member.mention}:"
        embed.add_field(
            name = "Basic Info",
            value = (
                f"**User ID**: {member.id}\n"
                f"**Display Name**: {member.display_name}\n"
                f"**Bot?**: {member.bot}\n"
            )
        )
        embed.add_field(
            name = "Events",
            value = (
                f"**Registered Date**: {member.created_at} <t:{int(member.created_at.timestamp())}:R>\n"
                f"**Joined At**: {member.joined_at} <t:{int(member.joined_at.timestamp())}:R>\n"
            )
        )
        embed.add_field(
            name = "Server Roles",
            value = (
                f"{' '.join(role.mention for role in member.roles if role.name != '@everyone')}"
                if member.roles else "No Roles"
            )
        )
        embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
        await interaction.response.send_message(embed=embed)

    @user_info.error
    async def error(self, interaction: discord.Interaction, error: discord.app_commands.AppCommandError) -> None:
        if isinstance(error, discord.app_commands.AppCommandError):
            await interaction.response.send_message("```diff\n- Command failed! Please try again.```", ephemeral=True)
            print(error)


async def setup(bot:commands.Bot) -> None:
  await bot.add_cog(UserInfo(bot))
