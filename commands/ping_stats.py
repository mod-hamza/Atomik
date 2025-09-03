from util.functions import loadJSON
from discord.ext import commands
from discord import app_commands
import discord

guild_settings = loadJSON("guild_settings")

class PingStats(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="ping-stats", description="[ADMIN ONLY] Send a ping to the bound stats channel")
    async def ping_stats(self, interaction: discord.Interaction) -> None:
        if not interaction.user.guild_permissions.administrator:
            return await interaction.response.send_message("❌ You must be an admin to use this command.", ephemeral=True)

        guild_id = str(interaction.guild.id)

        # Check if guild has settings
        if guild_id not in guild_settings:
            return await interaction.response.send_message(
                "❌ No stats channel is bound for this server. Please use `/bind resource:stats channel:#your-channel` to set one up first.",
                ephemeral=True
            )

        # Check if bindings exist
        if "bindings" not in guild_settings[guild_id]:
            return await interaction.response.send_message(
                "❌ No stats channel is bound for this server. Please use `/bind resource:stats channel:#your-channel` to set one up first.",
                ephemeral=True
            )

        # Check if stats is specifically bound
        if "stats" not in guild_settings[guild_id]["bindings"]:
            return await interaction.response.send_message(
                "❌ No stats channel is bound for this server. Please use `/bind resource:stats channel:#your-channel` to set one up first.",
                ephemeral=True
            )

        # Get the bound channel
        stats_channel_id = guild_settings[guild_id]["bindings"]["stats"]
        stats_channel = interaction.guild.get_channel(stats_channel_id)

        if not stats_channel:
            return await interaction.response.send_message(
                f"❌ The bound stats channel <#{stats_channel_id}> no longer exists. Please use `/rebind resource:stats channel:#new-channel` to update the binding.",
                ephemeral=True
            )

        # Create the ping embed
        embed = discord.Embed(
            title="🏓 Pong!",
            description="Stats channel is working properly!",
            color=0x2ecc71
        )

        # Add some fake stats as an example
        embed.add_field(
            name="📊 Server Stats",
            value="```\nMembers: 1,337\nChannels: 42\nRoles: 15\nBoosts: 3\n```",
            inline=False
        )

        embed.add_field(
            name="🤖 Bot Stats",
            value="```\nUptime: 23h 42m\nCommands: 156\nLatency: 42ms\n```",
            inline=False
        )

        embed.set_footer(
            text=f"Pinged by {interaction.user.display_name}",
            icon_url=interaction.user.display_avatar.url
        )
        embed.timestamp = discord.utils.utcnow()

        try:
            # Post to the bound channel
            await stats_channel.send(embed=embed)

            # Confirm to the admin
            await interaction.response.send_message(
                f"🏓 Pong sent successfully to {stats_channel.mention}!",
                ephemeral=True
            )

        except discord.Forbidden:
            await interaction.response.send_message(
                f"❌ I don't have permission to send messages in {stats_channel.mention}. Please check my permissions.",
                ephemeral=True
            )
        except Exception as e:
            await interaction.response.send_message(
                f"❌ Failed to send ping: {str(e)}",
                ephemeral=True
            )

    @ping_stats.error
    async def ping_stats_error(self, interaction: discord.Interaction, error):
        await interaction.response.send_message(
            f"❌ Failed to ping stats: {error}", ephemeral=True
        )


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(PingStats(bot))
