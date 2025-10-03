import disnake
import hashlib

from loguru import logger
from disnake.ext import commands
from main import cursor, connection, use_embed, get_system_color, generate_password

class UsersCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def is_setup(self, guild_id: int) -> bool:
        try:
            cursor.execute("SELECT 1 FROM settings WHERE guild_id = ?", (guild_id,))
            return cursor.fetchone() is not None
        except Exception as e:
            print(f"Ошибка при проверке установки: {e}")
            return False

    @commands.slash_command(name="user", description="Управление пользователями")
    async def user(self, interaction: disnake.ApplicationCommandInteraction):
        pass

    @user.sub_command(name="list", description="Посмотреть список пользователей")
    async def list_users(self, interaction: disnake.ApplicationCommandInteraction):
        await interaction.response.defer(ephemeral=True)
        if not self.is_setup(interaction.guild.id):
            await interaction.followup.send("Бот не настроен на этом сервере. Пожалуйста, используйте команду `/setup` для настройки.")
            return

        cursor.execute("SELECT user_id, username, discriminator, lvl FROM users WHERE guild_id = ?", (interaction.guild.id,))
        users = cursor.fetchall()
        if use_embed(interaction.guild.id):
            if not users:
                embed = disnake.Embed(description="Нет зарегистрированных пользователей на этом сервере.", color=disnake.Color(get_system_color(interaction.guild.id)))
                await interaction.followup.send(embed=embed)
                return

            embed = disnake.Embed(title="Список пользователей:", color=disnake.Color(get_system_color(interaction.guild.id)))
            for user in users:
                embed.add_field(name=f"{user[1]}#{user[2]}", value=f"ID: {user[0]} уровень: {user[3]}", inline=False)
            await interaction.followup.send(embed=embed)
        else:
            if not users:
                await interaction.followup.send("Нет зарегистрированных пользователей на этом сервере.")
                return

            user_list = "\n".join([f"{user[0]} уровень: {user[3]} - {user[1]}#{user[2]}" for user in users])
            await interaction.followup.send(f"Список пользователей:\n{user_list}")

    @user.sub_command(name="add", description="Добавить пользователя")
    async def add_user(self, interaction: disnake.ApplicationCommandInteraction, member: disnake.Member):
        await interaction.response.defer(ephemeral=True)
        if not self.is_setup(interaction.guild.id):
            await interaction.followup.send("Бот не настроен на этом сервере. Пожалуйста, используйте команду `/setup` для настройки.")
            return

        cursor.execute("SELECT lvl FROM users WHERE user_id = ?", (interaction.author.id,))
        user_lvl = cursor.fetchone()
        if user_lvl is None or user_lvl[0] != 2:
            await interaction.followup.send("У тебя недостаточно прав для выполнения команды")
            logger.warning(f"Пользователь {interaction.user} попытался добавить пользователя {member.user} в систему без прав.")
            return

        if use_embed(interaction.guild.id):
            cursor.execute("SELECT * FROM users WHERE guild_id = ? AND user_id = ?", (interaction.guild.id, member.id))
            if cursor.fetchone():
                embed = disnake.Embed(description="Пользователь уже имеет доступк к логам сервера.", color=disnake.Color(get_system_color(interaction.guild.id)))
                await interaction.followup.send(embed=embed)
                return

            password = generate_password()
            hash_password = hashlib.sha256(password.encode()).hexdigest()
            cursor.execute("INSERT INTO users (guild_id, user_id, username, discriminator, avatar_url, password) VALUES (?, ?, ?, ?, ?, ?)", (interaction.guild.id, member.id, member.name, member.discriminator, member.avatar.url, hash_password))
            connection.commit()
            embed = disnake.Embed(title="Пользователь успешно добавлен", description=f"Пользователю {member.name}#{member.discriminator} успешно выдан доступ к логам сервера.", color=disnake.Color(get_system_color(interaction.guild.id)))

            await member.send(f"Вам был выдан доступ к логам сервера {interaction.guild.name}. Ваш пароль: `{password}`")
            await interaction.followup.send(embed=embed)
        else:
            cursor.execute("SELECT * FROM users WHERE guild_id = ? AND user_id = ?", (interaction.guild.id, member.id))
            if cursor.fetchone():
                await interaction.followup.send("Пользователь уже имеет доступк к логам сервера.")
                return

            password = generate_password()
            hash_password = hashlib.sha256(password.encode()).hexdigest()
            cursor.execute("INSERT INTO users (guild_id, user_id, username, discriminator, avatar_url, password) VALUES (?, ?, ?, ?, ?, ?)", (interaction.guild.id, member.id, member.name, member.discriminator, member.avatar.url, hash_password))
            connection.commit()

            await member.send(f"Вам был выдан доступ к логам сервера {interaction.guild.name}. Ваш пароль: `{password}`")
            await interaction.followup.send(f"Пользователю {member.name}#{member.discriminator} успешно выдан доступ к логам сервера.")

    @user.sub_command(name="remove", description="Удалить пользователя")
    async def remove_user(self, interaction: disnake.ApplicationCommandInteraction, member: disnake.Member):
        await interaction.response.defer(ephemeral=True)
        if not self.is_setup(interaction.guild.id):
            await interaction.followup.send("Бот не настроен на этом сервере. Пожалуйста, используйте команду `/setup` для настройки.")
            return

        cursor.execute("SELECT lvl FROM users WHERE user_id = ?", (interaction.author.id,))
        user_lvl = cursor.fetchone()
        if user_lvl is None or user_lvl[0] != 2:
            await interaction.followup.send("У тебя недостаточно прав для выполнения команды")
            logger.warning(f"Пользователь {interaction.user} попытался удалить пользователя {member.user} из системы без прав.")
            return

        if use_embed(interaction.guild.id):
            cursor.execute("SELECT * FROM users WHERE guild_id = ? AND user_id = ?", (interaction.guild.id, member.id))
            if not cursor.fetchone():
                embed = disnake.Embed(description="Пользователь не найден в списке пользователей.", color=disnake.Color(get_system_color(interaction.guild.id)))
                await interaction.followup.send(embed=embed)
                return

            cursor.execute("DELETE FROM users WHERE guild_id = ? AND user_id = ?", (interaction.guild.id, member.id))
            connection.commit()
            embed = disnake.Embed(title="Пользователь успешно удален", description=f"Пользователь {member.name}#{member.discriminator} был удален из списка пользователей.", color=disnake.Color(get_system_color(interaction.guild.id)))

            await member.send(f"Ваш доступ к логам сервера {interaction.guild.name} был удален.")
            await interaction.followup.send(embed=embed)
        else:
            cursor.execute("SELECT * FROM users WHERE guild_id = ? AND user_id = ?", (interaction.guild.id, member.id))
            if not cursor.fetchone():
                await interaction.followup.send("Пользователь не найден в списке пользователей.")
                return

            cursor.execute("DELETE FROM users WHERE guild_id = ? AND user_id = ?", (interaction.guild.id, member.id))
            connection.commit()

            await member.send(f"Ваш доступ к логам сервера {interaction.guild.name} был удален.")
            await interaction.followup.send(f"Пользователь {member.name}#{member.discriminator} был удален из списка пользователей.")

def setup(bot: commands.Bot):
    bot.add_cog(UsersCog(bot))
