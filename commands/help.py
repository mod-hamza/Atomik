from discord.ext import commands
from discord import app_commands
import discord


class Help(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="help", description="Show all available commands and their descriptions")
    async def help(self, interaction: discord.Interaction) -> None:
        embed = discord.Embed(
            title="🤖 Atomik Bot - Command List",
            description="Here are all the available commands organized by permission level:",
            color=0x3498db
        )

        # Public Commands
        public_commands = [
            ("**`/user_info`**", "Get information about a user")
        ]

        public_text = "\n".join([f"{cmd} - {desc}" for cmd, desc in public_commands])
        embed.add_field(
            name="👥 Public Commands",
            value=public_text,
            inline=False
        )

        # Admin Commands
        admin_commands = [
            ("**`/announce`**", "Send an announcement to the bound announcements channel"),
            ("**`/ban`**", "Ban a member from the server"),
            ("**`/bind`**", "Bind a resource (leaderboard, announcements, logs, stats) to a channel"),
            ("**`/kick`**", "Kick a member from the server"),
            ("**`/leaderboard`**", "Post the leaderboard to the bound leaderboard channel"),
            ("**`/ping-stats`**", "Send a ping to the bound stats channel"),
            ("**`/rebind`**", "Rebind a resource to a different channel"),
            ("**`/status`**", "Check the status of all channel bindings"),
            ("**`/unbind`**", "Unbind a resource from a channel")
        ]

        admin_text = "\n".join([f"{cmd} - {desc}" for cmd, desc in admin_commands])
        embed.add_field(
            name="🛡️ Admin Commands",
            value=admin_text,
            inline=False
        )

        # Developer Commands
        dev_commands = [
            ("**`/developers`**", "Add or remove developers"),
            ("**`/reload`**", "Reload bot cogs/modules"),
            ("**`/settings`**", "Manage database settings or extract JSON data")
        ]

        dev_text = "\n".join([f"{cmd} - {desc}" for cmd, desc in dev_commands])
        embed.add_field(
            name="🔧 Developer Commands",
            value=dev_text,
            inline=False
        )

        # Additional Information
        embed.add_field(
            name="📋 Permission Levels",
            value=(
                "**👥 Public:** Anyone can use these commands\n"
                "**🛡️ Admin:** Requires server administrator permissions\n"
                "**🔧 Developer:** Requires developer status in the bot"
            ),
            inline=False
        )

        embed.add_field(
            name="💡 Resource Binding",
            value=(
                "Many commands require channel bindings. Use `/bind` to set up:\n"
                "• **leaderboard** - For leaderboard posts\n"
                "• **announcements** - For announcements\n"
                "• **logs** - For logging events\n"
                "• **stats** - For statistics and ping data"
            ),
            inline=False
        )

        embed.set_footer(text="Use /status to check your current channel bindings")
        embed.set_thumbnail(url=self.bot.user.avatar.url if self.bot.user.avatar else None)

        await interaction.response.send_message(embed=embed)

    @help.error
    async def help_error(self, interaction: discord.Interaction, error: discord.app_commands.AppCommandError) -> None:
        if isinstance(error, discord.app_commands.AppCommandError):
            await interaction.response.send_message("```diff\n- Help command failed! Please try again.```", ephemeral=True)
            print(error)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Help(bot))
