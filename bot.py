# bot.py
import os
import cosmos_like_utils
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix=commands.when_mentioned)


@bot.command(name='validator_status', help='Show validator status with given project name')
async def validator_status(ctx, project_name: str):
    if project_name == 'Desmos':
        response = cosmos_like_utils.get_validator_status(project_name)
    else:
        response = 'Not valid project name.'
    await ctx.send(response)


@bot.command(name='faucet', help='Get airdrop token from faucet.')
async def faucet(ctx, project_name: str):
    if project_name == 'Desmos':
        response = cosmos_like_utils.request_faucet(project_name)
    else:
        response = 'Not valid project name.'
    await ctx.send(response)


def run_bot():
    bot.run(TOKEN)