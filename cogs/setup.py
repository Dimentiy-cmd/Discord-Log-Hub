import disnake
import hashlib

from disnake.ext import commands
from main import cursor, connection, generate_password

class SetupCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        cursor.execute("""CREATE TABLE IF NOT EXISTS settings (
                guild_id INTEGER PRIMARY KEY,
                log_url TEXT, settings BOOLEAN DEFAULT TRUE,
                enabled BOOLEAN DEFAULT TRUE,
                system_color TEXT DEFAULT '#2f3136',
                use_embed BOOLEAN DEFAULT TRUE,
                log_message_edit BOOLEAN DEFAULT TRUE,
                log_message_delete BOOLEAN DEFAULT TRUE,
                log_member_join BOOLEAN DEFAULT TRUE,
                log_member_leave BOOLEAN DEFAULT TRUE,
                log_member_ban BOOLEAN DEFAULT TRUE,
                log_member_unban BOOLEAN DEFAULT TRUE,
                log_member_nickname_change BOOLEAN DEFAULT TRUE,
                log_role_changes BOOLEAN DEFAULT TRUE,
                log_channel_updates BOOLEAN DEFAULT TRUE,
                log_voice_channel_events BOOLEAN DEFAULT TRUE,
                log_invites BOOLEAN DEFAULT FALSE,
                log_command_usage BOOLEAN DEFAULT FALSE,
                ignore_bots BOOLEAN DEFAULT TRUE,
                log_emoji_changes BOOLEAN DEFAULT FALSE,
                log_sticker_changes BOOLEAN DEFAULT FALSE
            )""")
        cursor.execute("""CREATE TABLE IF NOT EXISTS users (
                guild_id INTEGER,
                user_id INTEGER,
                username TEXT,
                discriminator TEXT,
                avatar_url TEXT,
                password TEXT,
                lvl INT DEFAULT 1
            )""")
        cursor.execute("""CREATE TABLE IF NOT EXISTS logs_messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                message_id TEXT,
                channel_id TEXT,
                guild_id TEXT,
                user_id TEXT,
                username TEXT,
                action_type TEXT,
                old_content TEXT,
                new_content TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )""")
        cursor.execute("""CREATE TABLE IF NOT EXISTS logs_members (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                guild_id TEXT NOT NULL,
                user_id TEXT NOT NULL,
                username TEXT NOT NULL,
                action_type TEXT NOT NULL,
                old_value TEXT,
                new_value TEXT,
                content TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )""")
        cursor.execute("""CREATE TABLE IF NOT EXISTS logs_server (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                guild_id TEXT NOT NULL,
                user_id TEXT NOT NULL,
                username TEXT NOT NULL,
                action_type TEXT NOT NULL,
                content TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )""")
        cursor.execute("""CREATE TABLE IF NOT EXISTS logs_other (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                guild_id TEXT NOT NULL,
                user_id TEXT NOT NULL,
                username TEXT NOT NULL,
                action_type TEXT NOT NULL,
                content TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )""")
        cursor.execute("""CREATE TABLE IF NOT EXISTS errors (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                error TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )""")
        connection.commit()

    @commands.slash_command(name="setup", description="Произвести установку бота на сервер")
    async def setup(self, interaction: disnake.ApplicationCommandInteraction, log_url: str):
        await interaction.response.defer(ephemeral=True)
        if interaction.guild.owner.id != interaction.author.id:
            await interaction.followup.send("Установка доступна строго владельцу сервера")
            return

        try:
            cursor.execute("SELECT guild_id FROM settings WHERE guild_id = ?", (interaction.guild.id,))
            if cursor.fetchone():
                await interaction.followup.send("Бот уже настроен на сервере!")
            else:
                password = generate_password()
                hash = hashlib.sha256(password.encode()).hexdigest()
                await interaction.followup.send("Начинаю установку...")
                cursor.execute("INSERT INTO settings (guild_id, log_url) VALUES (?, ?)",(interaction.guild.id, log_url))
                cursor.execute("INSERT INTO users (guild_id, user_id, username, discriminator, avatar_url, password, lvl) VALUES (?, ?, ?, ?, ?, ?, ?)", (interaction.guild.id, interaction.author.id, interaction.author.name, interaction.author.discriminator, interaction.author.avatar.url, hash, 2))
                connection.commit()
                await interaction.author.send(f"Вам был выдан доступ к логам сервера {interaction.guild.name}. Ваш пароль: `{password}`")
                await interaction.followup.send("Установка завершена!", ephemeral=True)
        except Exception as e:
            await interaction.followup.send(f"Произошла ошибка при установке: {str(e)}")

def setup(bot):
    bot.add_cog(SetupCog(bot))
