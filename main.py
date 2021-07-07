#beta v1.0.0

'''

Справка по коду:
Добавить слеш команды(потребуется изменить в настройках бота разрешения)
Попробовать подключить боту "голос"
Сделать открытие ссылко на ютубе

'''

import discord
from discord.ext import commands
from random import *
import json  # для формирования json
import requests  # для формирования гет запросов
# надо разобраться в дальнейшей перспективе с модулем requests
from discord_slash import SlashCommand, SlashContext

import DB

GUILD = 'Новый отряд ПЕ-01б'  # название гильдии

# НЕ ТРОГААААААТЬ!!!!!!!!!!!!!!
TOKEN = 'your token'



bufшлёпа = 0

intents = discord.Intents.default()
intents.members = True
# использование как объект
client = commands.Bot(command_prefix='!', intents=intents)
# ПРЕФИКС ДЛЯ КОММАНД ЭТО     !
# , intents=discord.Intents.all() узнать что это
#slash = SlashCommand(client)

# -------------------СОЗДАТЬ БД ДЛЯ ЗАНЕСЕНИЯ УРОВНЕЙ И ПОЛЬЗОВАТЕЛЕЙ-----------------------------

DATABASE_PATH = 'Discord_API_bot.db'
database = DB.DiscordIdDataBase(DATABASE_PATH)




#_________________________________СОБЫТИЯ В ЧАТЕ_________________________________#

@client.event  # готовность бота пахать
async def on_ready():

    for guild in client.guilds:
        if guild.name == GUILD:
            break

    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})\n'
        )

    for guild in client.guilds:
        for member in guild.members:
            print(member)
            if member.id == 822189431444078653: #отлов ID бота
                pass
            else:
                if database.get_info_on_id(member.id): #при пустом массиве выодится False
                    pass
                else:
                    print("Массив пуст")
                    database.add_user([member.id, member.name, 0, 500])


@client.event
# возможен  on_messange (или будет замена на более поздний))
async def on_message(message):
    if message.author == client.user:
        return
    else:
        await client.process_commands(message)
        # if message.author.id == 502361945526108170:
        #    await message.channel.send("<@502361945526108170> завали ебало!")

        print(message.author.id)  # изи получил айди пользователя
        database.increase_column(message.author.id, 'total_messages')
#-----------------------------------------------------------------------------------------------------Ждем обновление БД от Даниила!!!!!
        user_message = database.get_info_on_id(message.author.id)[2] #[id, name, message, cash]
        if user_message % 10 ==  5:
            await message.channel.send(f"Поздравляю, {message.author.mention} с повышением уровня!!!!")
            #database.increase_column(message.author.id, 'total_messages', -user_message)



#_________________________________КОММАНДЫ_________________________________#

@client.command()  # пинг- понг
async def ping(ctx):
    await ctx.send('pong 🏓')


@client.command(name='rand')  # рандомное число
async def random(ctx):

    ping = randint(0, 6)
    emoji = '🟩🔳🔳🔳🔳'  # стандартное состояние

    if ping > 1:
        emoji = '🟧🟩🔳🔳🔳'
    if ping > 2:
        emoji = '🟥🟧🟩🔳🔳'
    if ping > 3:
        emoji = '🟥🟥🟧🟩🔳'
    if ping > 4:
        emoji = '🟥🟥🟥🟧🟩'
    if ping > 5:
        emoji = '🟥🟥🟥🟥🟧'
    if ping > 6:
        emoji = '🟥🟥🟥🟥🟥'

    message = await ctx.send('Пожалуйста, подождите. . .')
    await message.edit(content=f'! {emoji}')


@client.command(name='text')  # бот передразнивает человека
async def command(ctx, *, text):
    await ctx.send(f'{text}')


# ---------------------------------------справочные данные
@client.command(name='vk')  # МАЙ ВК
async def command(ctx):
    await ctx.send('https://vk.com/nikiyroman')


@client.command(name='steam')  # МАЙ СТИМ
async def command(ctx):
    await ctx.send("https://steamcommunity.com/id/r_ev1le/")


@client.command(name='about') #информация о боте
async def about(ctx):
    await ctx.send("Test_Bot v1.0.0 ")


@client.command(name='play') #заготовка!!!!!
async def play(ctx):
    await ctx.send("Не готово")


@client.command(name='m') #вывод всех участников гильдии
async def m(ctx):
    memR = ''
    for guild in client.guilds:
        if guild.name == GUILD:
            for member in guild.members:
                memR = memR + f'\n-{member}'
            await ctx.send(memR)


@client.command(name='cat') # печать рандомного изображения кота
async def cat(ctx):
    response = requests.get('https://some-random-api.ml/img/cat')  # Get-запрос
    json_data = json.loads(response.text)  # Извлекаем JSON

    embed = discord.Embed(
        color=0xff9900, title='Random Fox')  # Создание Embed'a
    embed.set_image(url=json_data['link'])  # Устанавливаем картинку Embed'a
    await ctx.send(embed=embed)  # Отправляем Embed


@client.command(name='dail')  # игра в числа
async def dail(ctx, text):
    print('Ставка - ',text)
    try:
        int(text)
    except ValueError :
        return await ctx.send('Неккоректная сумма!!!')
    
    if int(text) > database.get_info_on_id(ctx.author.id)[3]:
        return await ctx.send(f'У {ctx.author.name} не хвататет денег для ставок, пополните баланс на kidalovo.net')

    await ctx.send(f' {ctx.author.name} поставил {text} алмазов')
    a = [randint(1, 6), randint(1, 6)]
    await ctx.send(f' {ctx.author.name} выбил цыфры: :game_die: {a[0]} и {a[1]}')
    b = [randint(1, 6), randint(1, 6)]
    await ctx.send(f' Соперник выбил цыфры: :game_die: {b[0]} и {b[1]}')

    if (a[0]+a[1] > b[0]+b[1]): #Выбор результата игры
        await ctx.send(f' {ctx.author.name} выйграл {int(text)*2} алмазов')
        database.increase_column(ctx.author.id, 'cash', (int(text))*2)
    elif (a[0]+a[1] == b[0]+b[1]):
        await ctx.send(f' {ctx.author.name} вернул {text} алмазов')
        #database.increase_column(ctx.author.id, 'cash', 0)
    elif (a[0]+a[1] < b[0]+b[1]):
        await ctx.send(f' {ctx.author.name} проиграл {text} алмазов')
        database.increase_column(ctx.author.id, 'cash', -int(text))



@client.command(name='шлёпа') #вывод картинки рандомной шлёпы
async def rere(ctx):
    global bufшлёпа
    шлёпы = ['https://media1.tenor.com/images/9f61077990a3c31033c1620934dde704/tenor.gif?itemid=18413111',
             'https://pbs.twimg.com/media/EqF0aJhXUAIIB6R.jpg',
             'https://sun1-28.userapi.com/zKVb8i7AFgRa33SkuVMx-0sM9wxPi4YNIFgFFQ/FJV3XE-Pt7U.jpg',
             'https://static.wikia.nocookie.net/d49c64fe-08d8-4e1d-bdb0-f656fe87ed8d',
             'https://i.ytimg.com/vi/PV-DCnBwY5E/maxresdefault.jpg',
             'https://media1.tenor.com/images/f17cb7f46db22305680b1ea671b32f02/tenor.gif?itemid=20154951']
    шлёпа = discord.Embed(color=0xff9900, title='ШЛЁПА')  # Создание Embed'a
    if bufшлёпа > len(шлёпы)-1:
        bufшлёпа = 0
    шлёпа.set_image(url=шлёпы[bufшлёпа])  # Устанавливаем картинку Embed'a
    bufшлёпа += 1
    await ctx.send(embed=шлёпа)  # Отправляем Embed


# слеш команды НЕ РАБОТАЮЮЮЮЮЮТ!!!!!!!!!!!!(ИСправить через настройки бота)
slash = SlashCommand(client)


@slash.slash(name="test") #тетсовая слеш команда
async def test(ctx):
    embed = discord.Embed(title="embed test")
    await ctx.send(content="test", embeds=[embed])


client.run(TOKEN)  # запуск бота......
