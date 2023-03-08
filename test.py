# test.py

# URL OAuth2
# https://discord.com/api/oauth2/authorize?client_id=1082106315679223879&permissions=8&scope=bot

import os
import discord
import validators
from dotenv import load_dotenv
from discord.ext import commands

# Token desde .env
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Nuestros Intents requeridos
intents = discord.Intents.default()
intents.message_content = True
intents.members         = True

prefix          = '/'             # Prefijo para comandos
welcome_channel = 'bienvenidos'   # Canal para bienvenidas
ann_channel     = 'anuncios'      # Canal para anuncios
poll_channel    = 'encuestas'     # Canal para encuestas
admin_rol       = 'Maestro Admin' # Rol Admin
vip_rol         = 'Maestro VIP'   # Rol VIP
regular_rol     = 'Maestro'       # Rol regular
emoji_pos       = '👍'           # Emoji positivo
emoji_neg       = '👎'           # Emoji negativo
emoji_club      = '♟'            # Emoji club
image_url       = 'https://www.joystick.com.mx/wp-content/uploads/2023/01/icon-megaphone-with-white-bubble-social-media-marketing-concept_175838-976.jpg'
bot_version         = '1.0.0'         # Versión del bot

# Iniciando nuestro cliente
bot = commands.Bot(intents=intents, command_prefix=prefix)

# Evento on_ready()
@bot.event
async def on_ready():
    
    maestro = bot.user
    
    print(f'¡El Maestro {maestro} se ha conectado a Discord!')
    print(f'¡El Maestro tiene el id: {maestro.id} !')
    
    # Informacion de servidores conectados
    for guild in bot.guilds:
        print(f'Agregado a: {guild}({guild.id})')
        
        print(f'Tiene los miembros: {guild.member_count}')
        
        print('Tiene los miembros:')
        for member in guild.members:
            print(f'Canal: {member}')
        
        print('Tiene los canales:')
        for channel in guild.channels:
            print(f'Canal: {channel}')
            
#Evento on_message()
@bot.event
async def on_message(msg):
    # Nuestra lógica a ejecutar cada que se reciba un mensaje
    autor = msg.author
    
    # Prevenir el bucle infinito
    if (bot.user == autor):
        return
    
    # Validamos que un miembro escriba "Hola"
    if (msg.content.lower() == "hola"):
        # Imprimimos el mensaje
        print(f'Nuevo mensaje de {autor.name}: {msg.content}')
        # Enviamos un mensaje con nuestro bot
        await msg.reply(f'!Hola Maestro {autor.mention}!', mention_author=True)
        
    await bot.process_commands(msg)
    
# Eveneto on_member_join()
@bot.event
async def on_member_join(member):
    
    # Prevenir el bucle infinito al unir alguien nuevo
    if member.bot:
        return
    
    # Para que itere sobre todos los guilds / servidores
    for guild in bot.guilds:
        # Utilidad para buscar el canal
        channel = discord.utils.get(guild.text_channels, name=welcome_channel)
    
    if channel:
        #Plantilla del mensjae
        msg = f'¡Bienvenido Maestro {member.mention} al Club Peón Legendario! Unete a nuestro club de Lichess www.lichess.com\n`Reacciona con un 👍 si quires convertirte en un Maestro VIP y obtener acceso exclusivo.`'
        
        #Nuevo miembro
        print(f'{member.name}({member.id}) se unió al servidot {member.guild}')
        
        # Enviamos el Mensaje
        welcome_msg = await channel.send(msg)
        
        await welcome_msg.add_reaction(emoji_pos)
        
    # Utilidad para buscar
    role = discord.utils.get(guild.roles, name=regular_rol)
    
    # Solo si existe el rol, se le agrega al usuaio
    if role:
        print(f'Se añadió el rol {role} a {member.name}.')
        await member.add_roles(role)
        
# Evento on_reaction_add()
@bot.event
async def on_reaction_add(reaction, member):
    
    # Evitamos el loop
    if (reaction.message.author == member):
        return
    
    # Utilidad para buscar el rol VIP
    rol = discord.utils.get(member.guild.roles, name=vip_rol)
    # Utilidad para buscar el canal
    channel = discord.utils.get(member.guild.text_channels, name=welcome_channel)
    # Canal en el cual ocurrió la reacción
    reacted_on = True if reaction.message.channel == channel else False # Operación con ternarios de Python
    # Emoji requerido
    emoji = True if str(reaction.emoji) == str(emoji_pos) else False # Operación con ternarios de Python
    # Verificar si el mimbro ya tiene el rol
    has_rol = True if rol in member.roles else False
    
    if rol and channel and reacted_on and emoji:
        if has_rol:
            print(f'El miembro {member.name} ya tiene el rol {rol}')
            return
    
        #Loggeamos la acción
        print(f'Se añadió el rol {rol} a {member.name}.')
    
        await member.add_roles(rol)
    
# Evento on_reaction_remove()
@bot.event
async def on_reaction_remove(reaction, member):
    # Evitamos el loop
    if (reaction.message.author == member):
        return
    
    # Utilidad para buscar el rol VIP
    rol = discord.utils.get(member.guild.roles, name=vip_rol)
    # Utilidad para buscar el canal
    channel = discord.utils.get(member.guild.text_channels, name=welcome_channel)
    # Canal en el cual ocurrió la reacción
    reacted_on = True if reaction.message.channel == channel else False # Operación con ternarios de Python
    # Emoji requerido
    emoji = True if str(reaction.emoji) == str(emoji_pos) else False # Operación con ternarios de Python
    # Verificar si el mimbro ya tiene el rol
    has_rol = True if rol in member.roles else False
    
    if rol and channel and reacted_on and emoji:
        if has_rol == False:
            print(f'El miembro {member.name} no tiene el rol {rol}')
            return
    
        #Loggeamos la acción
        print(f'Se removió el rol {rol} a {member.name}.')
    
        await member.remove_roles(rol)
    
# Evento on_command_error()
@bot.event
async def on_command_error(ctx, error):
    await ctx.channel.send(f'Ocurrió un error en la ejecución del comando {ctx.author.mention}: **{error}**')

# Comando /hola
@bot.command()
async def hola(ctx):
    # Prevenir el bucle infinito
    if (bot.user == ctx.author):
        return
    
    await ctx.message.reply(f'¡Hola Maestro {ctx.author.mention}!', mention_author=True)
    
# Comando /ayuda
@bot.command(help='Solicita ayuda al equipo de Maestros por mensaje directo o dm.')
async def ayuda(ctx):
    # Lógica del comando
    autor = ctx.author
    msg = f' ¡Aquí estamos! ¿En qué podemos ayudarte {autor.name}?'
    url = 'https://cdn.shopify.com/s/files/1/0330/2067/4185/products/DP002_a4b39359-4109-4f62-9ab8-0a2ca1885760_900x.png?v=1606302474'
    
    await autor.send(msg)
    await autor.send(url)
    
# Comando /anuncio
@bot.command(help='Envia un anuncio nuevo al canal anuncios del guild.')
@commands.has_role('Maestro Admin')
async def anuncio(ctx, *, msg):
    
    # Validar canal
    channel     = discord.utils.get(ctx.guild.text_channels, name=ann_channel)
    
    if channel is None:
        await ctx.channel.send(f'El canal de text **{ann_channel}** no existe en la lista, {ctx.author.mention} prueba crearlo antes de continuar.')
        return
    
    role            = discord.utils.get(ctx.guild.roles, name=regular_rol)
    role_mention    = ''
    
    if role:
        role_mention = f'<@&{role.id}>'
    
    # Nuevo Embed
    title       = 'Atención Maestros'
    description = f'Nuevo anuncio de {ctx.guild}.'
    url         = 'https://www.liches.org'
    color       = 0xeccc68
    embed       = discord.Embed(title=title, description=description, url=url, color=color)
    embed.set_author(name=ctx.author, url=url, icon_url=ctx.author.display_avatar)
    embed.set_footer(text="www.liches.org")
    embed.add_field(name='Información', value='Buenas Maestros! Espero se encuentren bien y logren ingresar al próximo torneo!', inline=False)
    embed.add_field(name='Link', value=msg, inline=False)
    embed.add_field(name='Fecha', value='25 Febrero, 2023', inline=False)
    embed.add_field(name='Horario', value='12:34 PM', inline=False)
    embed.add_field(name='Contraseña', value='123456789', inline=False)
    embed.set_image(url=image_url)
    embed.set_thumbnail(url=image_url)
    
    await channel.send(' ' + role_mention, embed=embed)
    await ctx.message.reply(f'{ctx.author.mention} tu anuncio ha sido enviado con éxito al canal {channel}')
    
# Comando /encuesta
@bot.command(help="Crea una encuesta en el canal de Encuestas del guild.")
@commands.has_any_role(*["Maestro Admin", "Maestro VIP"])
async def encuesta(ctx, url):
    
    # Validar canal
    channel     = discord.utils.get(ctx.guild.text_channels, name=poll_channel)
    
    if channel is None:
        await ctx.channel.send(f'El canal de text **{ann_channel}** no existe en la lista, {ctx.author.mention} prueba crearlo antes de continuar.')
        return
    
    role            = discord.utils.get(ctx.guild.roles, name=vip_rol)
    role_mention    = ''
    
    if role:
        role_mention = f'<@&{role.id}>'
        
    #Validación del URL enviado
    valid_url = validators.url(url)
    
    if not valid_url:
        await ctx.message.reply(f'{ctx.author.mention} debes ingresar una URL válida para continuar.')
        return
    
    new_poll = await channel.send(url + ' ' + role_mention)
    await new_poll.add_reaction(emoji_pos)
    await new_poll.add_reaction(emoji_neg)
    
    await ctx.message.reply(f'{ctx.author.mention} tu encuesta ha sido enviada con éxito al canal {channel}.')

# Comando /version
@bot.command()
async def version(ctx):
    await ctx.send(f'La versión actual de **{bot.user}** es **{bot_version}**')
    
bot.run(TOKEN)