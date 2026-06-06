import discord
from discord.ext import commands
from flask.cli import run_command
import random

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="-", intents=intents)

@bot.command()
async def trivia(ctx, tema:str):
 dict_temas = {
        "ciencia": [
            {
                "pregunta": "¿Cuál es el planeta más grande del sistema solar?",
                "respuesta": "jupiter"
            }
        ],
        "videojuegos": [
            {
                "pregunta": "¿Cómo se llama el personaje principal de Hollow Knight?",
                "respuesta": "el caballero"
            }
        ]
    }
 if tema.lower() not in dict_temas:
        await ctx.send("El tema no está disponible")
        return

 datos = random.choice(dict_temas[tema.lower()])
 await ctx.send(f"El tema que has escogido es {tema}")
 await ctx.send(f"La pregunta es {datos['pregunta']}")
 def check(m):
    return m.author == ctx.author and m.channel == ctx.channel
 try:
    respuesta = await bot.wait_for("message", check=check, timeout = 20.0)
    if respuesta.content.lower() == datos["respuesta"].lower():
        await ctx.send("Correcto, has acertado en la respuesta!")
    else: 
        await ctx.send(f"Incorrecto, la respuesta era {datos['respuesta']}")
 except TimeoutError:
        await ctx.send("Se te acabo el tiempo!")
@bot.command()
async def archivo(ctx):
    if ctx.message.attachments:
        for attachment in ctx.message.attachments:
            file_name = attachment.filename
            file_url = attachment.url
            await attachment.save(f"./{attachment.filename}")
            await ctx.send(f"He recibido tu imagen y la guarde en {file_url} con {file_name}")
    else:
        await ctx.send("Olvidaste subir la imagen :(")

player_score = 0
bot_score = 0
@bot.command()
async def ppt (ctx):
    global player_score, bot_score

    opciones  = ["piedra", "papel", "tijera"]

    await ctx.send("El juego comenzó, escribe piedra, papel o tijera")
    while True:
        def verificar(mensaje):
            return mensaje.author == ctx.author and mensaje.channel == ctx.channel
        
        respuesta = await bot.wait_for("message", check=verificar)
        eleccion_jugador = respuesta.content.lower()
        if eleccion_jugador == "salir":
            await ctx.send(f"Gracias por jugar, tu puntaje es de:{player_score}, el puntaje del bot es:{bot_score}")
            player_score = 0
            bot_score = 0
            break
        if eleccion_jugador not in opciones:
            await ctx.send("Opción no válida")
            continue
        botx = random.choice(opciones)
        if eleccion_jugador == "tijera" and botx == "piedra" or eleccion_jugador == "papel" and botx == "tijera" or eleccion_jugador == "piedra" and botx == "papel":
            bot_score += 1
            await ctx.send(f"Perdiste😐 la elección del bot fue: {botx} y tu elección fue: {eleccion_jugador}, tu puntaje es: {player_score} y el puntaje del bot es: {bot_score} ")
        elif eleccion_jugador == botx:
            await ctx.send(f"Empate técnico tu puntaje es: {player_score} y el puntaje del bot es: {bot_score} ")
        elif eleccion_jugador == "tijera" and botx == "papel" or eleccion_jugador == "papel" and botx == "piedra" or eleccion_jugador == "piedra" and botx == "tijera":
            player_score += 1
            await ctx.send(f"Ganaste la primera ronda🎉: la elección del bot fue: {botx} y tu elección fue: {eleccion_jugador}, tu puntaje es: {player_score} y el puntaje del bot es: {bot_score} ")
        if bot_score == 3:
            await ctx.send("El bot te ha vencido😐⚙")
            player_score = 0
            bot_score = 0
            break
        if player_score == 3:
            await ctx.send("🎉Ganaste🎉")
            player_score = 0
            bot_score = 0
            break
