from util.functions import loadJSON
from discord.ext import commands
from discord import app_commands
import discord

guild_settings = loadJSON("guild_settings")

class Status(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="status", description="[ADMIN ONLY] Check the status of all channel bindings")
    async def status(self, interaction: discord.Interaction) -> None:
        if not interaction.user.guild_permissions.administrator:
            return await interaction.response.send_message("❌ You must be an admin to use this command.", ephemeral=True)

        guild_id = str(interaction.guild.id)

        # Create the status embed
        embed = discord.Embed(
            title="📊 Channel Bindings Status",
            description=f"Channel binding status for **{interaction.guild.name}**",
            color=0x3498db
        )

        # Define all possible resources
        resources = ["leaderboard", "announcements", "logs", "stats"]

        # Check if guild has any settings
        if guild_id not in guild_settings or "bindings" not in guild_settings[guild_id]:
            embed.add_field(
                name="⚠️ No Bindings Found",
                value="No channels are currently bound to any resources.\nUse `/bind` to set up channel bindings.",
                inline=False
            )
            embed.color = 0xe74c3c  # Red color for no bindings
        else:
            bindings = guild_settings[guild_id]["bindings"]
            healthy_count = 0
            total_bindings = 0

            status_text = ""

            for resource in resources:
                if resource in bindings:
                    total_bindings += 1
                    channel_id = bindings[resource]
                    channel = interaction.guild.get_channel(channel_id)

                    if channel:
                        # Channel exists and is healthy
                        status_text += f"✅ **{resource.title()}**: {channel.mention} (Healthy)\n"
                        healthy_count += 1
                    else:
                        # Channel is missing/deleted
                        status_text += f"❌ **{resource.title()}**: <#{channel_id}> (Missing/Deleted)\n"
                else:
                    # Resource not bound
                    status_text += f"⚪ **{resource.title()}**: Not bound\n"

            if status_text:
                embed.add_field(
                    name="Resource Bindings",
                    value=status_text,
                    inline=False
                )

            # Add summary
            if total_bindings == 0:
                summary = "No resources are currently bound."
                embed.color = 0xe74c3c  # Red
            elif healthy_count == total_bindings:
                summary = f"All {total_bindings} binding(s) are healthy! 🎉"
                embed.color = 0x2ecc71  # Green
            else:
                missing_count = total_bindings - healthy_count
                summary = f"{healthy_count}/{total_bindings} bindings are healthy. {missing_count} channel(s) missing."
                embed.color = 0xf39c12  # Orange

            embed.add_field(
                name="📈 Summary",
                value=summary,
                inline=False
            )

            # Add helpful commands
            commands_text = ""
            if total_bindings == 0:
                commands_text = "• Use `/bind` to bind resources to channels"
            else:
                commands_text = "• Use `/rebind` to fix missing channels\n• Use `/unbind` to remove bindings\n• Use `/bind` to add new bindings"

            embed.add_field(
                name="🔧 Quick Actions",
                value=commands_text,
                inline=False
            )

        # Add footer with timestamp
        embed.set_footer(
            text=f"Status checked by {interaction.user.display_name}",
            icon_url=interaction.user.display_avatar.url
        )
        embed.timestamp = discord.utils.utcnow()

        await interaction.response.send_message(embed=embed, ephemeral=True)

    @status.error
    async def status_error(self, interaction: discord.Interaction, error):
        await interaction.response.send_message(
            f"❌ Failed to check status: {error}", ephemeral=True
        )


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Status(bot))
