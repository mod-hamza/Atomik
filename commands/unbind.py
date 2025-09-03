from util.functions import loadJSON, saveJSON
from discord.ext import commands
from discord import app_commands
from typing import Literal
import discord



class Unbind(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="unbind", description="[ADMIN ONLY] Unbind a resource from a channel")
    @app_commands.describe(resource="What you want to unbind (e.g., leaderboard, announcements, logs, stats)")
    async def unbind(
        self,
        interaction: discord.Interaction,
        resource: Literal["leaderboard", "announcements", "logs", "stats"]
    ) -> None:
        guild_settings = loadJSON("guild_settings")
        if not interaction.user.guild_permissions.administrator:
            return await interaction.response.send_message("❌ You must be an admin to use this command.", ephemeral=True)

        guild_id = str(interaction.guild.id)

        # Check if guild exists in settings
        if guild_id not in guild_settings:
            return await interaction.response.send_message(
                f"❌ No bindings found for **{resource}** in this server.", ephemeral=True
            )

        # Check if bindings exist for this guild
        if "bindings" not in guild_settings[guild_id]:
            return await interaction.response.send_message(
                f"❌ No bindings found for **{resource}** in this server.", ephemeral=True
            )

        # Check if the specific resource is bound
        if resource.lower() not in guild_settings[guild_id]["bindings"]:
            return await interaction.response.send_message(
                f"❌ **{resource}** is not currently bound to any channel.", ephemeral=True
            )

        # Remove the binding
        del guild_settings[guild_id]["bindings"][resource.lower()]

        # Clean up empty bindings dict if no more bindings exist
        if not guild_settings[guild_id]["bindings"]:
            del guild_settings[guild_id]["bindings"]

        # Clean up empty guild entry if no more data exists
        if not guild_settings[guild_id]:
            del guild_settings[guild_id]

        saveJSON(guild_settings, "guild_settings")

        await interaction.response.send_message(
            f"✅ Unbound **{resource}** from its channel", ephemeral=True
        )

    @unbind.error
    async def unbind_error(self, interaction: discord.Interaction, error):
        await interaction.response.send_message(
            f"❌ Failed to unbind: {error}", ephemeral=True
        )


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Unbind(bot))
