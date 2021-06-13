# bot.py
import emoji
import os
import cosmos_like_utils, subgraph_utils, monitor_misc_utils
import requests
import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
CHANNEL_ID = os.getenv('CHANNEL_ID')
BITCANNA_REST_ENDPOINT = os.getenv('BITCANNA_REST_ENDPOINT')
BITCANNA_EXPLORER_ENDPOINT = os.getenv('BITCANNA_EXPLORER_ENDPOINT')

bot = commands.Bot(command_prefix='!')

ALL_ACTIVE_DELEGATION_TITLE = 'All Active Delegations for Your Requested Address'
STAKING_DELEGATION_TITLE = 'Staking Details for Your Requested Address'
STAKING_PARAMS_TITLE = 'Current Staking Params'
STAKING_POOL_TITLE = 'Staking Pool Details'
DELEGATOR_VALIDATOR_TITLE = 'Your Delegation Details For the Validator'
REDELEGATION_TITLE = 'Redelegation For The Requested Address'


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


@bot.command(name='bitcanna_delegation', help=ALL_ACTIVE_DELEGATION_TITLE)
async def bitcanna_delegation(ctx, address: str):
    try:
        r_json = requests.get(BITCANNA_REST_ENDPOINT + '/staking/delegators/' + address + '/delegations').json()
        embed = discord.Embed(color=discord.Color.green(), title=ALL_ACTIVE_DELEGATION_TITLE)
        embed.set_thumbnail(
            url='https://gblobscdn.gitbook.com/spaces%2F-MZWzVTthMwZ1G3jMP-6%2Favatar-1620730421877.png')
        for dataObj in r_json['result']:
            embed.add_field(name='Amount', value=dataObj['balance']['amount'], inline=True)
            embed.add_field(name='Denom', value=dataObj['balance']['denom'], inline=True)

            validator_address = dataObj['delegation']['validator_address']
            validators_json = requests.get(BITCANNA_REST_ENDPOINT + '/staking/validators/'
                                           + validator_address).json()
            moniker = validators_json['result']['description']['moniker']
            explorer_address = BITCANNA_EXPLORER_ENDPOINT + '/validators/' + validator_address
            embed.add_field(name='Validator', value='[{0}]({1})'.format(moniker, explorer_address), inline=True)
        await ctx.send(embed=embed)
    except:
        response = emoji.emojize('Something is wrong, try it later. :cry:')
        await ctx.send(response)
        raise


@bot.command(name='bitcanna_delegations', help=ALL_ACTIVE_DELEGATION_TITLE)
async def bitcanna_delegations(ctx, address: str):
    try:
        r_json = requests.get(BITCANNA_REST_ENDPOINT + '/staking/delegators/' + address + '/delegations').json()
        embed = discord.Embed(color=discord.Color.green(), title=ALL_ACTIVE_DELEGATION_TITLE)
        embed.set_thumbnail(
            url='https://gblobscdn.gitbook.com/spaces%2F-MZWzVTthMwZ1G3jMP-6%2Favatar-1620730421877.png')
        for dataObj in r_json['result']:
            embed.add_field(name='Amount', value=dataObj['balance']['amount'], inline=True)
            embed.add_field(name='Denom', value=dataObj['balance']['denom'], inline=True)

            validator_address = dataObj['delegation']['validator_address']
            validators_json = requests.get(BITCANNA_REST_ENDPOINT + '/staking/validators/'
                                           + validator_address).json()
            moniker = validators_json['result']['description']['moniker']
            explorer_address = BITCANNA_EXPLORER_ENDPOINT + '/validators/' + validator_address
            embed.add_field(name='Validator', value='[{0}]({1})'.format(moniker, explorer_address), inline=True)
        await ctx.send(embed=embed)
    except:
        response = emoji.emojize('Something is wrong, try it later. :cry:')
        await ctx.send(response)
        raise


@bot.command(name='bitcanna_validator', help=STAKING_DELEGATION_TITLE)
async def bitcanna_validator(ctx, address: str):
    try:
        r_json = requests.get(BITCANNA_REST_ENDPOINT + '/staking/validators/' + address).json()
        embed = discord.Embed(color=discord.Color.green(), title=STAKING_DELEGATION_TITLE)
        embed.set_thumbnail(
            url='https://gblobscdn.gitbook.com/spaces%2F-MZWzVTthMwZ1G3jMP-6%2Favatar-1620730421877.png')
        dataObj = r_json['result']
        embed.add_field(name='Total Amount', value=dataObj['tokens'], inline=True)
        embed.add_field(name='Commission', value=dataObj['commission']['commission_rates']['rate'][:4], inline=True)
        moniker = dataObj['description']['moniker']
        explorer_address = BITCANNA_EXPLORER_ENDPOINT + '/validators/' + address
        embed.add_field(name='Validator', value='[{0}]({1})'.format(moniker, explorer_address), inline=True)
        await ctx.send(embed=embed)
    except:
        response = emoji.emojize('Something is wrong, try it later. :cry:')
        await ctx.send(response)
        raise


@bot.command(name='bitcanna_staking_params', help=STAKING_PARAMS_TITLE)
async def bitcanna_staking_params(ctx):
    try:
        r_json = requests.get(BITCANNA_REST_ENDPOINT + '/staking/parameters').json()
        embed = discord.Embed(color=discord.Color.green(), title=STAKING_PARAMS_TITLE)
        embed.set_thumbnail(
            url='https://gblobscdn.gitbook.com/spaces%2F-MZWzVTthMwZ1G3jMP-6%2Favatar-1620730421877.png')
        dataObj = r_json['result']
        unbondingTime = str(int(dataObj['unbonding_time']) / (pow(10, 9) * 60 * 60 * 24))
        embed.add_field(name='Unboding Time', value=unbondingTime + ' day(s)', inline=True)
        embed.add_field(name='Max Validators', value=dataObj['max_validators'], inline=True)
        embed.add_field(name='Bond Denom', value=dataObj['bond_denom'], inline=True)
        await ctx.send(embed=embed)
    except:
        response = emoji.emojize('Something is wrong, try it later. :cry:')
        await ctx.send(response)
        raise


@bot.command(name='bitcanna_staking_pool', help=STAKING_POOL_TITLE)
async def bitcanna_staking_pool(ctx):
    try:
        r_json = requests.get(BITCANNA_REST_ENDPOINT + '/staking/pool').json()
        embed = discord.Embed(color=discord.Color.green(), title=STAKING_POOL_TITLE)
        embed.set_thumbnail(
            url='https://gblobscdn.gitbook.com/spaces%2F-MZWzVTthMwZ1G3jMP-6%2Favatar-1620730421877.png')
        dataObj = r_json['result']
        height = r_json['height']
        embed.add_field(name='Current Height', value=height, inline=True)
        notBondedTokens = str(int(dataObj['not_bonded_tokens']) / (pow(10, 6)))
        bondedTokens = str(int(dataObj['bonded_tokens']) / (pow(10, 6)))
        embed.add_field(name='Not Bonded', value=notBondedTokens, inline=True)
        embed.add_field(name='Bonded Tokens', value=bondedTokens, inline=True)
        await ctx.send(embed=embed)
    except:
        response = emoji.emojize('Something is wrong, try it later. :cry:')
        await ctx.send(response)
        raise


@bot.command(name='bitcanna_redelegations', help=REDELEGATION_TITLE)
async def bitcanna_redelegations(ctx, address: str):
    try:
        r_json = requests.get(BITCANNA_REST_ENDPOINT + '/staking/redelegations?delegator=' + address).json()
        embed = discord.Embed(color=discord.Color.green(), title=REDELEGATION_TITLE)
        embed.set_thumbnail(
            url='https://gblobscdn.gitbook.com/spaces%2F-MZWzVTthMwZ1G3jMP-6%2Favatar-1620730421877.png')
        for dataObj in r_json['result']:
            src_address = dataObj['redelegation']['validator_src_address']
            src_json = requests.get(BITCANNA_REST_ENDPOINT + '/staking/validators/' + src_address).json()
            src_moniker = src_json['result']['description']['moniker']
            src_explorer_address = BITCANNA_EXPLORER_ENDPOINT + '/validators/' + src_address
            embed.add_field(name='Validator Src Address', value='[{0}]({1})'.format(src_moniker, src_explorer_address), inline=True)

            dst_address = dataObj['redelegation']['validator_dst_address']
            dst_json = requests.get(BITCANNA_REST_ENDPOINT + '/staking/validators/' + dst_address).json()
            dst_moniker = dst_json['result']['description']['moniker']
            dst_explorer_address = BITCANNA_EXPLORER_ENDPOINT + '/validators/' + dst_address
            embed.add_field(name='Validator Dst Address', value='[{0}]({1})'.format(dst_moniker, dst_explorer_address), inline=True)

            if len(dataObj['entries']) > 0:
                embed.add_field(name='Balance', value=dataObj['entries'][0]['balance'], inline=True)

        await ctx.send(embed=embed)
    except:
        response = emoji.emojize('Something is wrong, try it later. :cry:')
        await ctx.send(response)
        raise


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

