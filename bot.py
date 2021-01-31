# bot.py
import emoji
import os
import cosmos_like_utils, subgraph_utils, monitor_misc_utils
from discord.ext import commands, tasks
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
CHANNEL_ID = os.getenv('CHANNEL_ID')

bot = commands.Bot(command_prefix=commands.when_mentioned)


@bot.command(name='validator_status', help='Show validator status with given project name')
async def validator_status(ctx, project_name: str):
    if project_name in ('Desmos', 'Bluzelle'):
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


@bot.command(name='luaswap_user', help='Query Luaswap user by Subgraph')
async def luaswap_user(ctx, address: str):
    try:
        response = subgraph_utils.get_luaswap_user(address)
    except:
        response = emoji.emojize('Something is wrong, try it later. :cry:')
    await ctx.send(response)


@bot.event
async def on_ready():
    check_status.start()
    print('MinatoBot is ready.')


@tasks.loop(minutes=10)
async def check_status():
    await bot.wait_until_ready()
    # Now Desmos node is paused, no need to monitor.
    '''
    if not cosmos_like_utils.is_validator_active('Desmos'):
        channel = bot.get_channel(int(CHANNEL_ID))
        await channel.send('@here Desmos node is inactive, please check!')
    '''
    # Now Mina Testnet is not stable, pause monitoring.
    # if not monitor_misc_utils.is_mina_node_synced():
        # await channel.send('@here Mina node is inactive, please check!')
    if monitor_misc_utils.is_slot_available():
        channel = bot.get_channel(int(CHANNEL_ID))
        await channel.send('@here Slot is available, please check!')


def run_bot():
    bot.run(TOKEN)

