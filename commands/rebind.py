from util.functions import loadJSON, saveJSON
from discord.ext import commands
from discord import app_commands
from typing import Literal
import discord

guild_settings = loadJSON("guild_settings")

class Rebind(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="rebind", description="[ADMIN ONLY] Rebind a resource to a different channel")
    @app_commands.describe(resource="What you want to rebind (e.g., leaderboard, announcements, logs, stats)")
    @app_commands.describe(channel="The new channel to bind this resource to")
    async def rebind(
        self,
        interaction: discord.Interaction,
        resource: Literal["leaderboard", "announcements", "logs", "stats"],
        channel: discord.TextChannel
    ) -> None:
        if not interaction.user.guild_permissions.administrator:
            return await interaction.response.send_message("❌ You must be an admin to use this command.", ephemeral=True)

        guild_id = str(interaction.guild.id)

        old_channel_id = None
        old_channel_mention = "none"

        if (guild_id in guild_settings and
            "bindings" in guild_settings[guild_id] and
            resource.lower() in guild_settings[guild_id]["bindings"]):

            old_channel_id = guild_settings[guild_id]["bindings"][resource.lower()]
            try:
                old_channel = interaction.guild.get_channel(old_channel_id)
                if old_channel:
                    old_channel_mention = old_channel.mention
                else:
                    old_channel_mention = f"<#{old_channel_id}> (deleted channel)"
            except:
                old_channel_mention = f"<#{old_channel_id}> (unknown channel)"

        # Initialize guild settings if they don't exist
        if guild_id not in guild_settings:
            guild_settings[guild_id] = {"bindings": {}}
        elif "bindings" not in guild_settings[guild_id]:
            guild_settings[guild_id]["bindings"] = {}

        # Set the new binding
        guild_settings[guild_id]["bindings"][resource.lower()] = channel.id
        saveJSON("guild_settings", guild_settings)

        # Create response message
        if old_channel_id:
            response_message = f"✅ Rebound **{resource}** from {old_channel_mention} to {channel.mention}"
        else:
            response_message = f"✅ Bound **{resource}** to {channel.mention} (was not previously bound)"

        await interaction.response.send_message(response_message, ephemeral=True)

    @rebind.error
    async def rebind_error(self, interaction: discord.Interaction, error) -> None:
        await interaction.response.send_message(
            f"❌ Failed to rebind: {error}", ephemeral=True
        )


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Rebind(bot))
