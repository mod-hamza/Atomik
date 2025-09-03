from util.functions import loadJSON
from discord.ext import commands
from discord import app_commands
import discord

guild_settings = loadJSON("guild_settings")

class Leaderboard(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="leaderboard", description="[ADMIN ONLY] Post the leaderboard to the bound leaderboard channel")
    async def leaderboard(self, interaction: discord.Interaction) -> None:
        guild_id = str(interaction.guild.id)

        # Check if guild has settings
        if guild_id not in guild_settings:
            return await interaction.response.send_message(
                "❌ No leaderboard channel is bound for this server. Please use `/bind` to set one up first.",
                ephemeral=True
            )

        # Check if bindings exist
        if "bindings" not in guild_settings[guild_id]:
            return await interaction.response.send_message(
                "❌ No leaderboard channel is bound for this server. Please use `/bind` to set one up first.",
                ephemeral=True
            )

        # Check if leaderboard is specifically bound
        if "leaderboard" not in guild_settings[guild_id]["bindings"]:
            return await interaction.response.send_message(
                "❌ No leaderboard channel is bound for this server. Please use `/bind` to set one up first.",
                ephemeral=True
            )

        # Get the bound channel
        leaderboard_channel_id = guild_settings[guild_id]["bindings"]["leaderboard"]
        leaderboard_channel = interaction.guild.get_channel(leaderboard_channel_id)

        if not leaderboard_channel:
            return await interaction.response.send_message(
                f"❌ The bound leaderboard channel <#{leaderboard_channel_id}> no longer exists. Please use `/rebind` to update the binding.",
                ephemeral=True
            )

        # Mock leaderboard data
        mock_leaderboard_data = [
            {"user": "AlphaGamer", "points": 2450},
            {"user": "BetaPlayer", "points": 2180},
            {"user": "GammaChamp", "points": 1920},
            {"user": "DeltaWarrior", "points": 1750},
            {"user": "EpsilonMaster", "points": 1580},
            {"user": "ZetaLegend", "points": 1420},
            {"user": "EtaHero", "points": 1280},
            {"user": "ThetaPro", "points": 1150},
            {"user": "IotaElite", "points": 1020},
            {"user": "KappaRookie", "points": 890}
        ]

        # Create the leaderboard embed
        embed = discord.Embed(
            title="🏆 Server Leaderboard",
            description="Here are the top players in our community!",
            color=0x00ff00
        )

        # Position emojis for visual appeal
        position_emojis = ["🥇", "🥈", "🥉", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]

        leaderboard_text = ""
        for i, player in enumerate(mock_leaderboard_data):
            position = i + 1
            emoji = position_emojis[i]
            leaderboard_text += f"**#{position}** {emoji} {player['user']}: **{player['points']:,}** points\n"

        embed.add_field(
            name="Top 10 Players",
            value=leaderboard_text,
            inline=False
        )

        embed.set_footer(text="Stay active in the server to climb the ranks!")

        try:
            # Post to the bound channel
            await leaderboard_channel.send(embed=embed)

            # Confirm to the admin
            await interaction.response.send_message(
                f"✅ Leaderboard posted successfully to {leaderboard_channel.mention}!",
                ephemeral=True
            )

        except discord.Forbidden:
            await interaction.response.send_message(
                f"❌ I don't have permission to send messages in {leaderboard_channel.mention}. Please check my permissions.",
                ephemeral=True
            )
        except Exception as e:
            await interaction.response.send_message(
                f"❌ Failed to post leaderboard: {str(e)}",
                ephemeral=True
            )

    @leaderboard.error
    async def leaderboard_error(self, interaction: discord.Interaction, error):
        await interaction.response.send_message(
            f"❌ Failed to post leaderboard: {error}", ephemeral=True
        )


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Leaderboard(bot))
