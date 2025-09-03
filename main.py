from discord.ext import commands
from dotenv import load_dotenv
from datetime import datetime
import discord
import logging
import time
import sys
import os

load_dotenv()

os.makedirs("logs", exist_ok=True)
log_filename = f"logs/{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log"
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    filename=log_filename,
    filemode="w"
)
logger = logging.getLogger(__name__)

def log_uncaught_exceptions(exctype, value, tb):
    logger.error("Uncaught exception", exc_info=(exctype, value, tb))

sys.excepthook = log_uncaught_exceptions

bot_token=os.getenv("BOT_TOKEN")
intents=discord.Intents.all()

class Client(commands.Bot):
    def __init__(self) -> None:
        super().__init__(command_prefix=commands.when_mentioned_or('%$'), intents=intents)
        self.cogslist=[
            "commands.announce", "commands.ban", "commands.bind", "commands.developers", "commands.rebind",
            "commands.help", "commands.kick", "commands.leaderboard", "commands.ping_stats", "commands.reload", "commands.settings",
            "commands.status", "commands.userinfo", "commands.unbind", "commands.settings"
        ]

    async def setup_hook(self) -> None:
        for ext in self.cogslist:
            try:
                await self.load_extension(ext)
                logger.info(f"Loaded cog: {ext}")
            except Exception as e:
                logger.error(f"Failed to load cog {ext}: {e}")

    async def on_ready(self) -> None:
        synced = await self.tree.sync()
        print(f"Synced {len(synced)} commands.")
        print(f"Logged in as {self.user} (ID: {self.user.id})")

        os.makedirs("temp", exist_ok=True)
        with open("uptime.txt","w") as file:
            file.write(str(time.time()))

try:
    bot=Client()
    bot.run(f"{bot_token}")
except Exception as e:
    logger.error(f"Error: {e}")
