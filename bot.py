import discord
from discord.ext import commands

from discord_bot.config import load_config

cfg = load_config(".env")
cogs: list = [
    "discord_bot.cogs.tracker.login",
    "discord_bot.cogs.tracker.logout",
    "discord_bot.cogs.tracker.shop",
    "discord_bot.cogs.tracker.stats",

    "discord_bot.cogs.actions.actions",

    "discord_bot.cogs.events.close.create",
    "discord_bot.cogs.events.new_member.new_member"
]
intents = discord.Intents.all()
client = commands.Bot(command_prefix="?", help_command=None, intents=intents)


@client.event
async def on_ready():
    print(f"Bot {client.user} is running!")
    for cog in cogs:
        try:
            print(f"Loading cog {cog}")
            await client.load_extension(cog)
            print(f"Loaded cog {cog}")
        except Exception as e:
            exc = f"{type(e).__name__}: {e}"
            print(f"Failed to load cog {cog}\n{exc}")

    qty_members = 0
    for guild in client.guilds:
        qty_members += len(guild.members)
        client.tree.clear_commands(guild=guild)

    await client.change_presence(
        status=discord.Status.online,
        activity=discord.Game(
            name=f'мониторю {qty_members} уродов'
        )
    )

    await client.tree.sync()


client.run(cfg.bot.token)