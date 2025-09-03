from util.functions import loadJSON, saveJSON
from discord.ext import commands
from discord import app_commands
from typing import Literal
import discord

developers = loadJSON("developers")


class Developers(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        super().__init__()
        self.bot=bot

    @app_commands.command(name="developers", description="[DEV ONLY] Add/Remove Developers")
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    @app_commands.user_install()
    @app_commands.guild_install()
    async def developers(self, interaction: discord.Interaction, action: Literal["add", "remove"], user: discord.User) -> None:
        if developers[interaction.user.id]:
            if action == "add":
                developers[user.id] = True
                saveJSON(developers, "developers")
                await interaction.response.send_message(content=f"```diff\n+ Added {user} to developers!```", ephemeral=True)
            elif action == "remove":
                developers[user.id] = False
                saveJSON(developers, "developers")
                await interaction.response.send_message(content=f"```diff\n- Removed {user} from developers!```", ephemeral=True)
        else:
            await interaction.response.send_message(content="You can't use this command. :)", ephemeral=True)

    @developers.error
    async def error(self, interaction: discord.Interaction, error: discord.app_commands.AppCommandError) -> None:
        if isinstance(error, discord.app_commands.AppCommandError):
            await interaction.response.send_message("```diff\n- Command failed! Please try again.```", ephemeral=True)
            print(error)


async def setup(bot:commands.Bot) -> None:
  await bot.add_cog(Developers(bot))
