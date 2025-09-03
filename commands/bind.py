from util.functions import loadJSON, saveJSON
from discord.ext import commands
from discord import app_commands
from typing import Literal
import discord



class Bind(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="bind", description="[ADMIN ONLY] Bind a resource to a channel")
    @app_commands.describe(resource="What you want to bind (e.g., leaderboard, announcements, logs, stats)")
    @app_commands.describe(channel="The channel to bind to this resource")
    async def bind(
        self,
        interaction: discord.Interaction,
        resource: Literal["leaderboard", "announcements", "logs", "stats"],
        channel: discord.TextChannel
    ) -> None:
        guild_settings = loadJSON("guild_settings")
        if not interaction.user.guild_permissions.administrator:
            return await interaction.response.send_message("❌ You must be an admin to use this command.", ephemeral=True)

        guild_id = str(interaction.guild.id)

        # Check if the resource is already bound
        if (guild_id in guild_settings and
            "bindings" in guild_settings[guild_id] and
            resource.lower() in guild_settings[guild_id]["bindings"]):

            existing_channel_id = guild_settings[guild_id]["bindings"][resource.lower()]
            try:
                existing_channel = interaction.guild.get_channel(existing_channel_id)
                if existing_channel:
                    existing_channel_mention = existing_channel.mention
                else:
                    existing_channel_mention = f"<#{existing_channel_id}> (deleted channel)"
            except:
                existing_channel_mention = f"<#{existing_channel_id}> (unknown channel)"

            return await interaction.response.send_message(
                f"❌ **{resource}** is already bound to {existing_channel_mention}. Use `/rebind` to change the binding.",
                ephemeral=True
            )

        if guild_id not in guild_settings:
            guild_settings[guild_id] = {"bindings": {}}

        guild_settings[guild_id]["bindings"][resource.lower()] = channel.id
        saveJSON(guild_settings, "guild_settings")

        await interaction.response.send_message(
            f"✅ Bound **{resource}** to {channel.mention}", ephemeral=True
        )

    @bind.error
    async def bind_error(self, interaction: discord.Interaction, error):
        await interaction.response.send_message(
            f"❌ Failed to bind: {error}", ephemeral=True
        )


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Bind(bot))
