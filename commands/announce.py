from util.functions import loadJSON
from discord.ext import commands
from discord import app_commands
import discord


class Announce(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="announce", description="[ADMIN ONLY] Send an announcement to the bound announcements channel")
    @app_commands.describe(title="The title of the announcement")
    @app_commands.describe(message="The announcement message content")
    async def announce(
        self,
        interaction: discord.Interaction,
        title: str,
        message: str
    ) -> None:
        guild_settings = loadJSON("guild_settings")
        if not interaction.user.guild_permissions.administrator:
            return await interaction.response.send_message("❌ You must be an admin to use this command.", ephemeral=True)

        guild_id = str(interaction.guild.id)

        # Check if guild has settings
        if guild_id not in guild_settings:
            return await interaction.response.send_message(
                "❌ No announcements channel is bound for this server. Please use `/bind` to set one up first.",
                ephemeral=True
            )

        # Check if bindings exist
        if "bindings" not in guild_settings[guild_id]:
            return await interaction.response.send_message(
                "❌ No announcements channel is bound for this server. Please use `/bind` to set one up first.",
                ephemeral=True
            )

        # Check if announcements is specifically bound
        if "announcements" not in guild_settings[guild_id]["bindings"]:
            return await interaction.response.send_message(
                "❌ No announcements channel is bound for this server. Please use `/bind` to set one up first.",
                ephemeral=True
            )

        # Get the bound channel
        announcements_channel_id = guild_settings[guild_id]["bindings"]["announcements"]
        announcements_channel = interaction.guild.get_channel(announcements_channel_id)

        if not announcements_channel:
            return await interaction.response.send_message(
                f"❌ The bound announcements channel <#{announcements_channel_id}> no longer exists. Please use `/rebind` to update the binding.",
                ephemeral=True
            )

        # Create the announcement embed
        embed = discord.Embed(
            title=f"📢 {title}",
            description=message,
            color=0x3498db
        )

        # Add footer with admin info
        embed.set_footer(
            text=f"Announcement by {interaction.user.display_name}",
            icon_url=interaction.user.display_avatar.url
        )

        # Add timestamp
        embed.timestamp = discord.utils.utcnow()

        try:
            # Post to the bound channel
            await announcements_channel.send(embed=embed)

            # Confirm to the admin
            await interaction.response.send_message(
                f"✅ Announcement posted successfully to {announcements_channel.mention}!",
                ephemeral=True
            )

        except discord.Forbidden:
            await interaction.response.send_message(
                f"❌ I don't have permission to send messages in {announcements_channel.mention}. Please check my permissions.",
                ephemeral=True
            )
        except Exception as e:
            await interaction.response.send_message(
                f"❌ Failed to post announcement: {str(e)}",
                ephemeral=True
            )

    @announce.error
    async def announce_error(self, interaction: discord.Interaction, error):
        await interaction.response.send_message(
            f"❌ Failed to post announcement: {error}", ephemeral=True
        )


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Announce(bot))
