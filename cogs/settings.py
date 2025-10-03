import disnake

from disnake.ext import commands
from main import cursor, connection, use_embed

class SettingsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def is_setup(self, guild_id: int) -> bool:
        try:
            cursor.execute("SELECT 1 FROM settings WHERE guild_id = ?", (guild_id,))
            return cursor.fetchone() is not None
        except Exception as e:
            print(f"Ошибка при проверке установки: {e}")
            return False

    @commands.slash_command(name="settings", description="Отображение настроек бота")
    async def settings(self, interaction: disnake.ApplicationCommandInteraction):
        await interaction.response.defer(ephemeral=True)
        cursor.execute("SELECT * FROM settings WHERE guild_id = ?", (interaction.guild.id,))
        settings = cursor.fetchone()
        if settings is None:
            await interaction.followup.send("Бот не настроен на этом сервере. Пожалуйста, используйте команду `/setup` для настройки.", ephemeral=True)
            return

        if use_embed(interaction.guild.id):
            color = int(settings["system_color"].lstrip('#'), 16)
            embed = disnake.Embed(title="Настройки бота", color=disnake.Color(color), description=f"Ссылка на логи: {settings['log_url']}\nID сервера: {interaction.guild.id}")
            embed.add_field(name="Основные настройки",
                value=f"**Логирование активно:** {'Да' if settings['enabled'] else 'Нет'}\n"
                    f"**Использовать embed-сообщений:** {'Да' if settings['use_embed'] else 'Нет'}\n"
                    f"**Игнорировать ботов:** {'Да' if settings['ignore_bots'] else 'Нет'}",
                inline=False)
            embed.add_field(name="Логирование сообщений",
                value=f"**Редактирование:** {'Да' if settings['log_message_edit'] else 'Нет'}\n"
                    f"**Удаление:** {'Да' if settings['log_message_delete'] else 'Нет'}\n",
                inline=True)
            embed.add_field(name="Логирование участников",
                value=f"**Вход:** {'Да' if settings['log_member_join'] else 'Нет'}\n"
                    f"**Выход:** {'Да' if settings['log_member_leave'] else 'Нет'}\n"
                    f"**Бан:** {'Да' if settings['log_member_ban'] else 'Нет'}\n"
                    f"**Разбан:** {'Да' if settings['log_member_unban'] else 'Нет'}\n"
                    f"**Смена ника:** {'Да' if settings['log_member_nickname_change'] else 'Нет'}",
                inline=True)
            embed.add_field(name="Логирование сервера",
                value=f"**Изменение ролей:** {'Да' if settings['log_role_changes'] else 'Нет'}\n"
                    f"**Изменение каналов:** {'Да' if settings['log_channel_updates'] else 'Нет'}\n"
                    f"**Голосовые каналы:** {'Да' if settings['log_voice_channel_events'] else 'Нет'}\n"
                    f"**Приглашения:** {'Да' if settings['log_invites'] else 'Нет'}",
                inline=True)
            embed.add_field(name="Прочее",
                value=f"**Использование команд:** {'Да' if settings['log_command_usage'] else 'Нет'}\n"
                    f"**Изменение эмодзи:** {'Да' if settings['log_emoji_changes'] else 'Нет'}\n"
                    f"**Изменение стикеров:** {'Да' if settings['log_sticker_changes'] else 'Нет'}\n",
                inline=True)
            await interaction.followup.send(embed=embed, ephemeral=True)
        else:
            message = (
                "**Настройки бота**\n"
                f"Ссылка на логи: {settings['log_url']}\n"
                f"ID сервера: {interaction.guild.id}\n"
                "**Основные настройки:**\n"
                f"- Логирование активно: {'Да' if settings['enabled'] else 'Нет'}\n"
                f"- Использовать embed: {'Да' if settings['use_embed'] else 'Нет'}\n"
                f"- Игнорировать ботов: {'Да' if settings['ignore_bots'] else 'Нет'}\n"
                "**Логирование сообщений:**\n"
                f"- Редактирование: {'Да' if settings['log_message_edit'] else 'Нет'}\n"
                f"- Удаление: {'Да' if settings['log_message_delete'] else 'Нет'}\n"
                "**Логирование участников:**\n"
                f"- Вход: {'Да' if settings['log_member_join'] else 'Нет'}\n"
                f"- Выход: {'Да' if settings['log_member_leave'] else 'Нет'}\n"
                f"- Бан: {'Да' if settings['log_member_ban'] else 'Нет'}\n"
                f"- Разбан: {'Да' if settings['log_member_unban'] else 'Нет'}\n"
                f"- Смена ника: {'Да' if settings['log_member_nickname_change'] else 'Нет'}\n"
                "**Логирование сервера:**\n"
                f"- Изменение ролей: {'Да' if settings['log_role_changes'] else 'Нет'}\n"
                f"- Изменение каналов: {'Да' if settings['log_channel_updates'] else 'Нет'}\n"
                f"- Голосовые каналы: {'Да' if settings['log_voice_channel_events'] else 'Нет'}\n"
                f"- Приглашения: {'Да' if settings['log_invites'] else 'Нет'}\n"
                "**Прочее:**\n"
                f"- Использование команд: {'Да' if settings['log_command_usage'] else 'Нет'}\n"
                f"- Изменение эмодзи: {'Да' if settings['log_emoji_changes'] else 'Нет'}\n"
                f"- Изменение стикеров: {'Да' if settings['log_sticker_changes'] else 'Нет'}")
            await interaction.followup.send(message, ephemeral=True)

    @commands.slash_command(name="set", description=("Редактирование настроек бота"))
    @commands.has_permissions(administrator=True)
    async def set(self, interaction: disnake.ApplicationCommandInteraction):
        pass

    @set.sub_command(name="color", description=("Установка цвета для системных embed сообщений"))
    async def set_color(self, interaction: disnake.ApplicationCommandInteraction, color: str):
        await interaction.response.defer(ephemeral=True)
        if not self.is_setup(interaction.guild.id):
            await interaction.followup.send("Бот не настроен на этом сервере. Пожалуйста, используйте команду `/setup` для настройки.")
            return

        if not color.startswith("#") or len(color) != 7:
            await interaction.followup.send("Пожалуйста, введите корректный HEX цвет (например, #FF0000).")
            return

        cursor.execute("UPDATE settings SET system_color = ? WHERE guild_id = ?", (color, interaction.guild.id))
        connection.commit()
        await interaction.followup.send(f"Цвет системных сообщений успешно обновлен на {color}.")

    @set.sub_command(name="embed", description="Включение или отключение использования embed сообщений")
    async def set_embed(self, interaction: disnake.ApplicationCommandInteraction, use_embed: bool):
        await interaction.response.defer(ephemeral=True)
        if not self.is_setup(interaction.guild.id):
            await interaction.followup.send("Бот не настроен на этом сервере. Пожалуйста, используйте команду `/setup` для настройки.")
            return

        cursor.execute("UPDATE settings SET use_embed = ? WHERE guild_id = ?", (int(use_embed), interaction.guild.id))
        connection.commit()
        status = "включено" if use_embed else "отключено"
        await interaction.followup.send(f"Использование embed сообщений успешно {status}.")

    @set.sub_command(name="logging", description="Включение или отключение логирования")
    async def set_logging(self, interaction: disnake.ApplicationCommandInteraction, enebled: bool):
        await interaction.response.defer(ephemeral=True)
        if not self.is_setup(interaction.guild.id):
            await interaction.followup.send("Бот не настроен на этом сервере. Пожалуйста, используйте команду `/setup` для настройки.")
            return

        cursor.execute("UPDATE settings SET enabled = ? WHERE guild_id = ?", (int(enebled), interaction.guild.id))
        connection.commit()
        status = "включено" if enebled else "отключено"
        await interaction.followup.send(f"Логирование сервера успешно {status}.")

    @set.sub_command(name="logurl", description="Установка ссылки на логи")
    async def set_logurl(self, interaction: disnake.ApplicationCommandInteraction, logurl: str):
        await interaction.response.defer(ephemeral=True)
        if not self.is_setup(interaction.guild.id):
            await interaction.followup.send("Бот не настроен на этом сервере. Пожалуйста, используйте команду `/setup` для настройки.")
            return

        cursor.execute("UPDATE settings SET log_url = ? WHERE guild_id = ?", (logurl, interaction.guild.id))
        connection.commit()
        await interaction.followup.send(f"Ссылка на логи была успешно изменена на: {logurl}.")

    @set.sub_command(name="ignorebots", description="Включить или выключить игнорирование ботов")
    async def set_ignore(self, interaction: disnake.ApplicationCommandInteraction, ignorebots: bool):
        await interaction.response.defer(ephemeral=True)
        if not self.is_setup(interaction.guild.id):
            await interaction.followup.send("Бот не настроен на этом сервере. Пожалуйста, используйте команду `/setup` для настройки.")
            return

        cursor.execute("UPDATE settings SET ignore_bots = ? WHERE guild_id = ?", (int(ignorebots), interaction.guild.id))
        connection.commit()
        status = "включено" if ignorebots else "отключено"
        await interaction.followup.send(f"Игнорирование ботов успешно {status}.", ephemeral=True)

    @set.sub_command(name="editmsg", description="Включить или выключить логирование изменений сообщений")
    async def set_editmsg(self, interaction: disnake.ApplicationCommandInteraction, editmsg: bool):
        await interaction.response.defer(ephemeral=True)
        if not self.is_setup(interaction.guild.id):
            await interaction.followup.send("Бот не настроен на этом сервере. Пожалуйста, используйте команду `/setup` для настройки.")
            return

        cursor.execute("UPDATE settings SET log_message_edit = ? WHERE guild_id = ?", (int(editmsg), interaction.guild.id))
        connection.commit()
        status = "включено" if editmsg else "отключено"
        await interaction.followup.send(f"Логирование изменений сообщений успешно {status}.", ephemeral=True)

    @set.sub_command(name="delmsg", description="Включить или выключить логирование удаления сообщений")
    async def set_delmsg(self, interaction: disnake.ApplicationCommandInteraction, editmsg: bool):
        await interaction.response.defer(ephemeral=True)
        if not self.is_setup(interaction.guild.id):
            await interaction.followup.send("Бот не настроен на этом сервере. Пожалуйста, используйте команду `/setup` для настройки.")
            return

        cursor.execute("UPDATE settings SET log_message_delete = ? WHERE guild_id = ?", (int(editmsg), interaction.guild.id))
        connection.commit()
        status = "включено" if editmsg else "отключено"
        await interaction.followup.send(f"Логирование удаления сообщений успешно {status}.", ephemeral=True)

    @set.sub_command(name="join", description="Включить или выключить логирование входа участников")
    async def set_join(self, interaction: disnake.ApplicationCommandInteraction, join: bool):
        await interaction.response.defer(ephemeral=True)
        if not self.is_setup(interaction.guild.id):
            await interaction.followup.send("Бот не настроен на этом сервере. Пожалуйста, используйте команду `/setup` для настройки.")
            return

        cursor.execute("UPDATE settings SET log_member_join = ? WHERE guild_id = ?", (int(join), interaction.guild.id))
        connection.commit()
        status = "включено" if join else "отключено"
        await interaction.followup.send(f"Логирование входа участников успешно {status}.", ephemeral=True)

    @set.sub_command(name="leave", description="Включить или выключить логирование выхода участников")
    async def set_join(self, interaction: disnake.ApplicationCommandInteraction, leave: bool):
        await interaction.response.defer(ephemeral=True)
        if not self.is_setup(interaction.guild.id):
            await interaction.followup.send("Бот не настроен на этом сервере. Пожалуйста, используйте команду `/setup` для настройки.")
            return

        cursor.execute("UPDATE settings SET log_member_leave = ? WHERE guild_id = ?", (int(leave), interaction.guild.id))
        connection.commit()
        status = "включено" if leave else "отключено"
        await interaction.followup.send(f"Логирование выхода участников успешно {status}.", ephemeral=True)

    @set.sub_command(name="ban", description="Включить или выключить логирование блокировок пользователей")
    async def set_ban(self, interaction: disnake.ApplicationCommandInteraction, ban: bool):
        await interaction.response.defer(ephemeral=True)
        if not self.is_setup(interaction.guild.id):
            await interaction.followup.send("Бот не настроен на этом сервере. Пожалуйста, используйте команду `/setup` для настройки.")
            return

        cursor.execute("UPDATE settings SET log_member_ban = ? WHERE guild_id = ?", (int(ban), interaction.guild.id))
        connection.commit()
        status = "включено" if ban else "отключено"
        await interaction.followup.send(f"Логирование блокировок пользователей успешно {status}.", ephemeral=True)

    @set.sub_command(name="unban", description="Включить или выключить логирование разблокировок пользователей")
    async def set_unban(self, interaction: disnake.ApplicationCommandInteraction, unban: bool):
        await interaction.response.defer(ephemeral=True)
        if not self.is_setup(interaction.guild.id):
            await interaction.followup.send("Бот не настроен на этом сервере. Пожалуйста, используйте команду `/setup` для настройки.")
            return

        cursor.execute("UPDATE settings SET log_member_unban = ? WHERE guild_id = ?", (int(unban), interaction.guild.id))
        connection.commit()
        status = "включено" if unban else "отключено"
        await interaction.followup.send(f"Логирование разблокировок пользователей успешно {status}.", ephemeral=True)

    @set.sub_command(name="changenick", description="Включить или выключить логирование изменений ников участников")
    async def set_changenick(self, interaction: disnake.ApplicationCommandInteraction, changenick: bool):
        await interaction.response.defer(ephemeral=True)
        if not self.is_setup(interaction.guild.id):
            await interaction.followup.send("Бот не настроен на этом сервере. Пожалуйста, используйте команду `/setup` для настройки.")
            return

        cursor.execute("UPDATE settings SET log_member_nickname_change = ? WHERE guild_id = ?", (int(changenick), interaction.guild.id))
        connection.commit()
        status = "включено" if changenick else "отключено"
        await interaction.followup.send(f"Логирование изменений ников участников успешно {status}.", ephemeral=True)

    @set.sub_command(name="editrole", description="Включить или выключить логирование редактирования ролей")
    async def set_editrole(self, interaction: disnake.ApplicationCommandInteraction, editrole: bool):
        await interaction.response.defer(ephemeral=True)
        if not self.is_setup(interaction.guild.id):
            await interaction.followup.send("Бот не настроен на этом сервере. Пожалуйста, используйте команду `/setup` для настройки.")
            return

        cursor.execute("UPDATE settings SET log_role_changes = ? WHERE guild_id = ?", (int(editrole), interaction.guild.id))
        connection.commit()
        status = "включено" if editrole else "отключено"
        await interaction.followup.send(f"Логирование редактирования ролей успешно {status}.", ephemeral=True)

    @set.sub_command(name="editchannel", description="Включить или выключить логирование редактирования каналов")
    async def set_editchannel(self, interaction: disnake.ApplicationCommandInteraction, editchannel: bool):
        await interaction.response.defer(ephemeral=True)
        if not self.is_setup(interaction.guild.id):
            await interaction.followup.send("Бот не настроен на этом сервере. Пожалуйста, используйте команду `/setup` для настройки.")
            return

        cursor.execute("UPDATE settings SET log_channel_updates = ? WHERE guild_id = ?", (int(editchannel), interaction.guild.id))
        connection.commit()
        status = "включено" if editchannel else "отключено"
        await interaction.followup.send(f"Логирование редактирования каналов успешно {status}.", ephemeral=True)

    @set.sub_command(name="voice", description="Включить или выключить логирование голосовых каналов")
    async def set_voice(self, interaction: disnake.ApplicationCommandInteraction, voice: bool):
        await interaction.response.defer(ephemeral=True)
        if not self.is_setup(interaction.guild.id):
            await interaction.followup.send("Бот не настроен на этом сервере. Пожалуйста, используйте команду `/setup` для настройки.")
            return

        cursor.execute("UPDATE settings SET log_voice_channel_events = ? WHERE guild_id = ?", (int(voice), interaction.guild.id))
        connection.commit()
        status = "включено" if voice else "отключено"
        await interaction.followup.send(f"Логирование голосовых каналов каналов успешно {status}.", ephemeral=True)

    @set.sub_command(name="invite", description="Включить или выключить логирование приглашений")
    async def set_invite(self, interaction: disnake.ApplicationCommandInteraction, invite: bool):
        await interaction.response.defer(ephemeral=True)
        if not self.is_setup(interaction.guild.id):
            await interaction.followup.send("Бот не настроен на этом сервере. Пожалуйста, используйте команду `/setup` для настройки.")
            return

        cursor.execute("UPDATE settings SET log_invites = ? WHERE guild_id = ?", (int(invite), interaction.guild.id))
        connection.commit()
        status = "включено" if invite else "отключено"
        await interaction.followup.send(f"Логирование приглашений успешно {status}.", ephemeral=True)

def setup(bot):
    bot.add_cog(SettingsCog(bot))
