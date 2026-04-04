from ram_bot.bot import RamBot
from ram_bot.config import BotConfig


def create_bot() -> RamBot:
    return RamBot(BotConfig.from_env())


def main():
    bot = create_bot()
    bot.run(bot.config.token)
