import os
import disnake

from loguru import logger
from disnake.ext import commands
from main import connection, cursor

TOKEN = os.getenv("TOKEN")
bot = commands.Bot(command_prefix='!', intents=disnake.Intents.all())

@bot.event
async def on_ready():
    logger.info("Бот запущен!")

@bot.event
async def on_slash_command_error(interaction: disnake.ApplicationCommandInteraction, error: Exception):
    if isinstance(error, disnake.ext.commands.MissingPermissions):
        await interaction.response.send_message("У тебя недостаточно прав для выполнения команды", ephemeral=True)
        logger.warning(f"Пользователь {interaction.user} попытался выполнить команду /{interaction.application_command.name} без прав.")
    else:
        logger.error(f"ОШИБКА | Выполнение команды /{interaction.application_command.name}: {error}")
        await interaction.response.send_message("Произошла ошибка при выполнении команды.", ephemeral=True)

@bot.slash_command(name="info", description="Информация о боте")
async def info(interaction: disnake.ApplicationCommandInteraction):
    await interaction.response.defer(ephemeral=True)
    cursor.execute("SELECT guild_id FROM settings WHERE guild_id = ?", (interaction.guild.id,))
    if cursor.fetchone() is None:
        await interaction.followup.send("Бот не настроен на этом сервере. Пожалуйста, используйте команду `/setup` для настройки.")
        return

    cursor.execute("SELECT use_embed, system_color FROM settings WHERE guild_id = ?", (interaction.guild.id,))
    settings = cursor.fetchone()
    use_embed = settings[0]
    system_color = settings[1]

    if use_embed == 0:
        await interaction.followup.send("Discord Log Hub - современная система для логирования вашего discord сервера")
    else:
        color = int(system_color.lstrip('#'), 16) if system_color.startswith('#') else int(system_color, 16)
        embed = disnake.Embed(description="Discord Log Hub - современная система для логирования вашего discord сервера", color=disnake.Color(color))
        await interaction.followup.send(embed=embed)

def run_bot():
    try:
        bot.load_extension("cogs.logs")
        logger.info("Загружен ког logs")
        bot.load_extension("cogs.settings")
        logger.info("Загружен ког settings")
        bot.load_extension("cogs.setup")
        logger.info("Загружен ког setup")
        bot.load_extension("cogs.users")
        logger.info("Загружен ког users")
        logger.info("Запуск бота...")
        bot.run(TOKEN)
    except Exception as e:
        logger.error(f"Ошибка при запуске бота или загрузке кога: {e}")

if __name__ == "__main__":
    run_bot()
