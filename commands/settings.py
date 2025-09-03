from util.functions import loadJSON, saveJSON
from discord.ext import commands
from discord import app_commands
from typing import Literal
import discord
import os
import json
import io

developers = loadJSON("developers")

class Settings(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        super().__init__()
        self.bot = bot

    @app_commands.command(name="settings", description="[DEV ONLY] Manage database settings or extract JSON data")
    @app_commands.describe(action="Choose to fix the database or extract JSON data")
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    @app_commands.user_install()
    @app_commands.guild_install()
    async def settings(self, interaction: discord.Interaction, action: Literal["fix", "extract"]) -> None:
        # Check if user is a developer
        user_id = str(interaction.user.id)
        if user_id not in developers or not developers[user_id]:
            await interaction.response.send_message(content="You can't use this command. :)", ephemeral=True)
            return

        try:
            if action == "extract":
                await self._handle_extract(interaction)
            elif action == "fix":
                await self._handle_fix(interaction)
                
        except Exception as e:
            await interaction.response.send_message(
                content=f"```diff\n- Command failed! Error: {str(e)}```", 
                ephemeral=True
            )

    async def _handle_extract(self, interaction: discord.Interaction) -> None:
        """Handle JSON extraction"""
        try:
            # Load guild settings
            guild_settings = loadJSON("guild_settings")
            
            # Convert to pretty JSON string
            json_data = json.dumps(guild_settings, indent=2, ensure_ascii=False)
            
            # Check if data is too large for Discord message
            if len(json_data) > 1900:  # Leave room for code block formatting
                # Create a text file with the data
                file_content = json_data.encode('utf-8')
                file = discord.File(
                    fp=io.BytesIO(file_content),
                    filename="guild_settings.json"
                )
                
                embed = discord.Embed(
                    title="📄 Guild Settings Export",
                    description="The guild settings data is too large for a message, so it's been exported as a file.",
                    color=0x3498db
                )
                embed.add_field(
                    name="📊 Stats",
                    value=f"Total guilds: {len(guild_settings)}\nFile size: {len(file_content)} bytes",
                    inline=False
                )
                embed.set_footer(
                    text=f"Exported by {interaction.user.display_name}",
                    icon_url=interaction.user.display_avatar.url
                )
                embed.timestamp = discord.utils.utcnow()
                
                await interaction.response.send_message(embed=embed, file=file, ephemeral=True)
            else:
                # Send as code block
                embed = discord.Embed(
                    title="📄 Guild Settings Export",
                    description=f"```json\n{json_data}\n```",
                    color=0x3498db
                )
                embed.add_field(
                    name="📊 Stats",
                    value=f"Total guilds: {len(guild_settings)}",
                    inline=False
                )
                embed.set_footer(
                    text=f"Exported by {interaction.user.display_name}",
                    icon_url=interaction.user.display_avatar.url
                )
                embed.timestamp = discord.utils.utcnow()
                
                await interaction.response.send_message(embed=embed, ephemeral=True)
                
        except Exception as e:
            await interaction.response.send_message(
                content=f"```diff\n- Failed to extract JSON: {str(e)}```",
                ephemeral=True
            )

    async def _handle_fix(self, interaction: discord.Interaction) -> None:
        """Handle database migration/fixing"""
        try:
            # Initialize migration status
            migration_results = []
            
            # Migration 1: Create guild_settings structure
            migration_results.append(await self._migrate_guild_settings())
            
            # Prepare response
            success_count = sum(1 for result in migration_results if result['success'])
            total_migrations = len(migration_results)
            
            # Create response embed
            embed = discord.Embed(
                title="� Database Validation Results",
                color=0x2ecc71 if success_count == total_migrations else 0xf39c12
            )
            
            for result in migration_results:
                status_emoji = "✅" if result['success'] else "❌"
                embed.add_field(
                    name=f"{status_emoji} {result['name']}",
                    value=result['message'],
                    inline=False
                )
            
            embed.add_field(
                name="📊 Summary",
                value=f"Completed {success_count}/{total_migrations} migrations successfully",
                inline=False
            )
            
            embed.set_footer(
                text=f"Database validation by {interaction.user.display_name}",
                icon_url=interaction.user.display_avatar.url
            )
            embed.timestamp = discord.utils.utcnow()
            
            await interaction.response.send_message(embed=embed, ephemeral=True)
            
        except Exception as e:
            await interaction.response.send_message(
                content=f"```diff\n- Migration failed! Error: {str(e)}```", 
                ephemeral=True
            )

    async def _migrate_guild_settings(self) -> dict:
        """
        Migration: Create guild_settings table structure
        This migration is idempotent - running it multiple times won't break anything
        """
        try:
            # Load existing guild settings
            guild_settings = loadJSON("guild_settings")
            
            # Track if any changes were made
            changes_made = False
            initial_guilds = len(guild_settings)
            
            # Ensure the file exists (loadJSON creates it if it doesn't exist)
            if not isinstance(guild_settings, dict):
                guild_settings = {}
                changes_made = True
            
            # Validate and fix existing guild entries
            guilds_fixed = 0
            for guild_id in list(guild_settings.keys()):
                guild_data = guild_settings[guild_id]
                
                # Ensure guild_data is a dictionary
                if not isinstance(guild_data, dict):
                    guild_settings[guild_id] = {"bindings": {}}
                    changes_made = True
                    guilds_fixed += 1
                    continue
                
                # Ensure bindings key exists
                if "bindings" not in guild_data:
                    guild_data["bindings"] = {}
                    changes_made = True
                    guilds_fixed += 1
                
                # Ensure bindings is a dictionary
                if not isinstance(guild_data["bindings"], dict):
                    guild_data["bindings"] = {}
                    changes_made = True
                    guilds_fixed += 1
                
                # Validate binding values (should be integers for channel IDs)
                for resource, channel_id in list(guild_data["bindings"].items()):
                    if not isinstance(channel_id, int):
                        try:
                            guild_data["bindings"][resource] = int(channel_id)
                            changes_made = True
                            guilds_fixed += 1
                        except (ValueError, TypeError):
                            # Remove invalid binding
                            del guild_data["bindings"][resource]
                            changes_made = True
                            guilds_fixed += 1
            
            # Save changes if any were made
            if changes_made:
                saveJSON("guild_settings", guild_settings)
            
            # Prepare result message
            if initial_guilds == 0 and len(guild_settings) == 0:
                message = "Guild settings table created successfully (empty)"
            elif guilds_fixed > 0:
                message = f"Guild settings table validated and fixed {guilds_fixed} entries"
            else:
                message = "Guild settings table already exists and is valid"
            
            return {
                'name': 'Guild Settings Table',
                'success': True,
                'message': message
            }
            
        except Exception as e:
            return {
                'name': 'Guild Settings Table',
                'success': False,
                'message': f"Failed to create/validate guild settings: {str(e)}"
            }

    @settings.error
    async def settings_error(self, interaction: discord.Interaction, error: discord.app_commands.AppCommandError) -> None:
        if isinstance(error, discord.app_commands.AppCommandError):
            await interaction.response.send_message("```diff\n- Settings command failed! Please try again.```", ephemeral=True)
            print(f"Settings error: {error}")


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Settings(bot))
