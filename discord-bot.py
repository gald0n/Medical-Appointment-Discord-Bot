discord.py

import discord
from discord.ext import commands
import json
import os

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

# Cargar datos previos
if os.path.exists("citas.json"):
    with open("citas.json", "r") as f:
        citas = json.load(f)
else:
    citas = []

# Comando para registrar una cita
@bot.command(name="cita")
async def registrar_cita(ctx, paciente: discord.Member, psicologo: discord.Member, hora: str):
    entrada = {
        "paciente_id": paciente.id,
        "psicologo_id": psicologo.id,
        "hora": hora
    }
    citas.append(entrada)

    # Guardar en archivo
    with open("citas.json", "w") as f:
        json.dump(citas, f, indent=4)

    mensaje = f"Cita de Psicología de <@{paciente.id}> para el/la Psicólogo/a <@{psicologo.id}> a las {hora}."
    await ctx.send(mensaje)

# Comando para ver todas las citas
@bot.command(name="ver_citas")
async def ver_citas(ctx):
    if not citas:
        await ctx.send("No hay citas registradas.")
        return

    mensaje = "**Citas registradas:**\n"
    for i, c in enumerate(citas, 1):
        mensaje += f"{i}. <@{c['paciente_id']}> con <@{c['psicologo_id']}> a las {c['hora']}\n"
    await ctx.send(mensaje)

# Comando para limpiar todas las citas (administrador)
@bot.command(name="limpiar_citas")
@commands.has_permissions(administrator=True)
async def limpiar_citas(ctx):
    global citas
    citas = []
    with open("citas.json", "w") as f:
        json.dump(citas, f)
    await ctx.send("Todas las citas han sido eliminadas.")

# Mensaje de arranque
@bot.event
async def on_ready():
    print(f'Bot conectado como {bot.user}')

# Reemplaza 'TU_TOKEN_AQUI' con tu token real del bot
bot.run("TU_TOKEN_AQUI")
