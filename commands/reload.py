from util.functions import loadJSON
from discord.ext import commands
from discord import app_commands
from typing import Literal
import discord




class Reload(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        super().__init__()
        self.bot=bot

    @app_commands.command(name="reload", description="[DEV ONLY]")
    async def reload(self, interaction: discord.Interaction, cog: Literal[
        "About", "Announce", "Bind", "Help", "Ping_Stats", "Reload", "Settings", "Status", "Leaderboard", "Userinfo",
        "Ban", "Developers", "Kick", "Rebind", "Status", "Unbind"
    ]) -> None:
        developers = loadJSON("developers")
        user_id = str(interaction.user.id)

        if user_id not in developers or not developers[user_id]:
            await interaction.response.send_message(content="You can't use this command. :)", ephemeral=True)
            return

        await self.bot.reload_extension(name=f"cogs.{cog.lower()}")
        await interaction.response.send_message(content=f"```diff\n+ Reloaded {cog} cog!```", ephemeral=True)

    @reload.error
    async def error(self, interaction: discord.Interaction, error: discord.app_commands.AppCommandError) -> None:
        if isinstance(error, discord.app_commands.AppCommandError):
            await interaction.response.send_message("```diff\n- Command failed! Please try again.```", ephemeral=True)
            print(error)


async def setup(bot:commands.Bot) -> None:
  await bot.add_cog(Reload(bot))
