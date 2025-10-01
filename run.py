import discord
from discord.ext import commands
from db import db, cursor
from imp import config
import modules.fun
import modules.moderation
from discord.ext.tasks import loop
from datetime import datetime


client = commands.Bot(command_prefix = "!", intents=discord.Intents.all())
client.remove_command('help')


module_mod= modules.moderation.Moderation(client,db=db,cursor=cursor, cfg=config)
module_fun = modules.fun.fun(client,db=db,cursor=cursor, cfg=config)


client.run(config.TOKEN)