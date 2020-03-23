#!/bin/python3
# Python room temperature bot

import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import time
import board
import adafruit_dht
import threading
import datetime

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
UNIT = os.getenv('UNIT')
HOT = int(os.getenv('HOT'))
COLD = int(os.getenv('COLD'))
LOG_LEVEL = os.getenv('LOG_LEVEL')

HIGH=None
LOW=None
PREV=None
TEMP=None
HUM=None

def log(msg, level='info'):
    global LOG_LEVEL

    levels = {
        'error': [ 'error' ],
        'warn': [ 'error', 'warn' ],
        'info': [ 'error', 'warn', 'info' ],
        'debug': [ 'error', 'warn', 'info', 'debug' ],
        'trace': [ 'error', 'warn', 'info', 'debug', 'trace' ],
    }

    if level in levels[LOG_LEVEL]:
        with open('bot.log', 'a') as f:
            f.write('[' + str(level).upper() + '] - ' + str(datetime.datetime.now()) + ' - ' + str(msg) + '\n')

def getDataFromSensor():
    global HIGH, LOW, UNIT, TEMP, HUM

    dhtDevice = adafruit_dht.DHT22(board.D4)
    
    while True:
        try:
            temp = dhtDevice.temperature
            if UNIT == 'F':
                temp = temp * (9 / 5) + 32
            
            humidity = dhtDevice.humidity

            if HIGH == None:
                HIGH = temp
            elif HIGH < temp:
                HIGH = temp

            if LOW == None:
                LOW = temp
            elif temp < LOW:
                LOW = temp

            HUM = humidity
            TEMP = temp
            log('Temp=' + str(temp) + ', Humidity=' + str(humidity), 'debug')
        except RuntimeError as error:
            log(error, level='error')
            continue
        
        time.sleep(2.0)

def getCurrentTemp():
    global TEMP, HUM

    data = {
        'temp': TEMP,
        'humidity': HUM
    }    
    return data

thread = threading.Thread(target=getDataFromSensor)
thread.start()

bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')
    guild = discord.utils.get(bot.guilds, name=GUILD)
    log('Bot connected to discord', level='info')

@bot.command(name='temp', help='Responds with temperature info')
async def respondWithTemp(ctx):
    log('Replying to !temp command', level='info') 
    global HIGH, LOW, HOT, COLD
    current = getCurrentTemp()
    print('Replying to !temp command (' + str(current['temp']) + '°C)')
    
    if current['temp'] >= HOT:
        colour = 0xffa600
    elif current['temp'] <= COLD:
        colour = 0x00a6ff
    else:
        colour = 0x00ff00

    embed = discord.Embed(title="Room temperature", color=colour)
    embed.add_field(name="Current", value=str(current['temp']) + '°C', inline=False)
    embed.add_field(name="Humidity", value=str(current['humidity']) + '%', inline=False)
    embed.add_field(name="High", value=str(HIGH) + '°C', inline=True)
    embed.add_field(name="Low", value=str(LOW) + '°C', inline=True)

    await ctx.send(embed=embed)

bot.remove_command('help')
@bot.command(name='help')
async def help(ctx):
    log('Replying to !help command', level='info')
    embed = discord.Embed(title="Room temp help", color=0xf77d74)
    embed.add_field(name='Info command', value="`!temp` - will return current, high and low temp", inline=True)
    await ctx.send(embed=embed)

@bot.event
async def on_error(event, *args, **kwargs):
    log(event, level='error')

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CommandNotFound):
        True
    else:
        log(error, level='error')

bot.run(TOKEN)