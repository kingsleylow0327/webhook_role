# bot.py
import discord
from discord.ext import commands
from logger import Logger
from config import Config
from sql_con import ZonixDB

# Logger setup
logger_mod = Logger("WebRole")
logger = logger_mod.get_logger()

# Client setup
intents = discord.Intents.all()
intents.message_content = True
bot = commands.Bot(command_prefix="!",intents=intents)

# Bot setup
config = Config()

# DB Setup
dbcon = ZonixDB(config)
invite_cache = {}

@bot.event
async def on_ready():
    await bot.tree.sync()
    for guild in bot.guilds:
        invite_cache[guild.id] = await guild.invites()
    logger.info(" WebHook Role Bot Ready")


@bot.event
async def on_member_join(member):
    old_invites = invite_cache[member.guild.id]
    new_invites = await member.guild.invites()
    used_invite = None

    for old, new in zip(old_invites, new_invites):
        if old.uses < new.uses:
            used_invite = new
            break

    invite_cache[member.guild.id] = new_invites

    if used_invite:
        logger.info(f" {member} joined using {used_invite.code}")

        # Assign role based on invite code
        invite_to_role = {
            "GPVmCWqBWb": "80potato", # https://discord.gg/GPVmCWqBWb
            "BJtd5sk2xg": "TBC", # https://discord.gg/BJtd5sk2xg
            "GDgF39RBaE": "BCC", # https://discord.gg/GDgF39RBaE
            "4Cpt8S7c": "potato100" # https://discord.gg/4Cpt8S7c
        }

        role_name = invite_to_role.get(used_invite.code)
        if role_name:
            role = discord.utils.get(member.guild.roles, name=role_name)
            if role:
                await member.add_roles(role)
                dbcon.update_invitation_number_by_code(used_invite.code)
                logger.info(f" Assigned {role.name} to {member.display_name}")

bot.run(config.TOKEN)