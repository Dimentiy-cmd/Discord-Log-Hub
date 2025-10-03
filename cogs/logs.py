import disnake

from disnake.ext import commands
from main import cursor, connection

class LogsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def is_enabled(self, guild_id: int) -> bool:
        try:
            cursor.execute("SELECT enabled FROM settings WHERE guild_id = ?", (guild_id,))
            result = cursor.fetchone()

            if result is None:
                return False
            return bool(result[0])

        except Exception as e:
            print(f"Ошибка при проверке настроек: {e}")
            return False

    def should_ignore_bots(self, guild_id: int) -> bool:
        try:
            cursor.execute("SELECT ignore_bots FROM settings WHERE guild_id = ?", (guild_id,))
            result = cursor.fetchone()

            if result is None:
                return False
            return bool(result[0])

        except Exception as e:
            print(f"Ошибка при проверке настроек: {e}")
            return False

    @commands.Cog.listener()
    async def on_message_delete(self, message: disnake.Message):
        if not self.is_enabled(message.guild.id) or (message.author.bot and self.should_ignore_bots(message.guild.id)):
            return

        cursor.execute("SELECT log_message_delete FROM settings WHERE guild_id = ?", (message.guild.id,))
        if cursor.fetchone() is None or False:
            return

        cursor.execute("INSERT INTO logs_messages (message_id, channel_id, guild_id, user_id, username, action_type, old_content) VALUES (?, ?, ?, ?, ?, 'DELETE', ?)", (message.id, message.channel.id, message.guild.id, message.author.id, f"{message.author.name}#{message.author.discriminator}", message.content))
        connection.commit()

    @commands.Cog.listener()
    async def on_message_edit(self, before: disnake.Message, after: disnake.Message):
        if not self.is_enabled(before.guild.id) or (before.author.bot and self.should_ignore_bots(before.guild.id)):
            return

        cursor.execute("SELECT log_message_edit FROM settings WHERE guild_id = ?", (before.guild.id,))
        if cursor.fetchone() is None or False:
            return

        if before.content == after.content:
            return
        cursor.execute("INSERT INTO logs_messages (message_id, channel_id, guild_id, user_id, username, action_type, old_content, new_content) VALUES (?, ?, ?, ?, ?, 'EDIT', ?, ?)", (before.id, before.channel.id, before.guild.id, before.author.id, f"{before.author.name}#{before.author.discriminator}", before.content, after.content))
        connection.commit()

    @commands.Cog.listener()
    async def on_member_join(self, member: disnake.Member):
        if not self.is_enabled(member.guild.id) or (member.bot and self.should_ignore_bots(member.guild.id)):
            return

        cursor.execute("SELECT log_member_join FROM settings WHERE guild_id = ?", (member.guild.id,))
        if cursor.fetchone() is None or False:
            return

        cursor.execute("INSERT INTO logs_members (user_id, guild_id, username, action_type) VALUES (?, ?, ?, 'JOIN')", (member.id, member.guild.id, f"{member.name}#{member.discriminator}"))
        connection.commit()

    @commands.Cog.listener()
    async def on_member_remove(self, member: disnake.Member):
        if not self.is_enabled(member.guild.id) or (member.bot and self.should_ignore_bots(member.guild.id)):
            return

        cursor.execute("SELECT log_member_leave FROM settings WHERE guild_id = ?", (member.guild.id,))
        if cursor.fetchone() is None or False:
            return

        cursor.execute("INSERT INTO logs_members (user_id, guild_id, username, action_type) VALUES (?, ?, ?, 'LEAVE')", (member.id, member.guild.id, f"{member.name}#{member.discriminator}"))
        connection.commit()

    @commands.Cog.listener()
    async def on_member_ban(self, guild: disnake.Guild, user: disnake.User):
        if not self.is_enabled(guild.id) or (user.bot and self.should_ignore_bots(guild.id)):
            return

        cursor.execute("SELECT log_member_ban FROM settings WHERE guild_id = ?", (guild.id,))
        if cursor.fetchone() is None or False:
            return

        async for entry in guild.audit_logs(limit=1, action=disnake.AuditLogAction.ban):
            if entry.target.id == user.id:
                moderator = entry.user
                reason = entry.reason or "не указана"
                content = f" Модератор {moderator.name}#{moderator.discriminator} заблокировал пользователя. Причина: {reason}"
                cursor.execute("INSERT INTO logs_members (user_id, guild_id, username, action_type, content) VALUES (?, ?, ?, 'BAN', ?)", (user.id, guild.id, f"{user.name}#{user.discriminator}", content))
                connection.commit()
                return

    @commands.Cog.listener()
    async def on_member_unban(self, guild: disnake.Guild, user: disnake.User):
        if not self.is_enabled(guild.id) or (user.bot and self.should_ignore_bots(guild.id)):
            return

        cursor.execute("SELECT log_member_unban FROM settings WHERE guild_id = ?", (guild.id,))
        if cursor.fetchone() is None or False:
            return

        async for entry in guild.audit_logs(limit=1, action=disnake.AuditLogAction.unban):
            if entry.target.id == user.id:
                moderator = entry.user
                reason = entry.reason or "не указана"
                content = f" Модератор {moderator.name}#{moderator.discriminator} разблокировал пользователя. Причина: {reason}"
                cursor.execute("INSERT INTO logs_members (user_id, guild_id, username, action_type, content) VALUES (?, ?, ?, 'UNBAN', ?)", (user.id, guild.id, f"{user.name}#{user.discriminator}", content))
                connection.commit()
                return
        connection.commit()

    @commands.Cog.listener()
    async def on_member_update(self, before: disnake.Member, after: disnake.Member):
        if not self.is_enabled(before.guild.id):
            return

        cursor.execute("SELECT log_member_nickname_change FROM settings WHERE guild_id = ?", (before.guild.id,))
        if cursor.fetchone() is None or False:
            return

        if before.nick != after.nick:
            old = before.nick
            new = after.nick
            cursor.execute("INSERT INTO logs_members (guild_id, user_id, username, action_type, old_value, new_value) VALUES (?, ?, ?, 'EDITNICK', ?, ?)", (after.guild.id, after.id, after.name, old, new))
            connection.commit()

    @commands.Cog.listener()
    async def on_guild_role_update(self, before: disnake.Role, after: disnake.Role):
        if not self.is_enabled(before.guild.id):
            return

        cursor.execute("SELECT log_role_changes FROM settings WHERE guild_id = ?", (before.guild.id,))
        if cursor.fetchone() is None or False:
            return

        async for entry in after.guild.audit_logs(limit=1, action=disnake.AuditLogAction.role_update):
            if before.name != after.name:
                cursor.execute("INSERT INTO logs_server (guild_id, user_id, username, action_type, content) VALUES (?, ?, ?, 'EDITROLE', ?)", (after.guild.id, entry.user.id, entry.user.name, f"Смена названия роли {before.name} → {after.name}"))
            elif before.colour != after.colour:
                cursor.execute("INSERT INTO logs_server (guild_id, user_id, username, action_type, content) VALUES (?, ?, ?, 'EDITROLE', ?)", (after.guild.id, entry.user.id, entry.user.name, f"Смена цвета роли {before.colour} → {after.colour}"))
            elif before.permissions != after.permissions:
                before_perms = set(p for p, v in before.permissions if v)
                after_perms = set(p for p, v in after.permissions if v)

                added = after_perms - before_perms
                removed = before_perms - after_perms
                if added:
                    cursor.execute("INSERT INTO logs_server (guild_id, user_id, username, action_type, content) VALUES (?, ?, ?, 'EDITROLE', ?)", (after.guild.id, entry.user.id, entry.user.name, f"Добавлены права роли {', '.join(added)}"))
                if removed:
                    cursor.execute("INSERT INTO logs_server (guild_id, user_id, username, action_type, content) VALUES (?, ?, ?, 'EDITROLE', ?)", (after.guild.id, entry.user.id, entry.user.name, f"Удалены права роли {', '.join(removed)}"))
        connection.commit()

    @commands.Cog.listener()
    async def on_guild_channel_update(self, before: disnake.abc.GuildChannel, after: disnake.abc.GuildChannel):
        if not self.is_enabled(before.guild.id):
            return

        cursor.execute("SELECT log_channel_updates FROM settings WHERE guild_id = ?", (before.guild.id,))
        if cursor.fetchone() is None or False:
            return

        async for entry in after.guild.audit_logs(limit=1, action=disnake.AuditLogAction.channel_update):
            if before.name != after.name:
                cursor.execute("INSERT INTO logs_server (guild_id, user_id, username, action_type, content) VALUES (?, ?, ?, 'EDITCHANNEL', ?)", (after.guild.id, entry.user.id, entry.user.name, f"Смена названия канала {before.name} → {after.name}"))
            elif before.position != after.position:
                cursor.execute("INSERT INTO logs_server (guild_id, user_id, username, action_type, content) VALUES (?, ?, ?, 'EDITCHANNEL', ?)", (after.guild.id, entry.user.id, entry.user.name, f"Смена позиции канала {before.position} → {after.position}"))
            elif before.category != after.category:
                before_cat = before.category.name if before.category else "Нет"
                after_cat = after.category.name if after.category else "Нет"
                cursor.execute("INSERT INTO logs_server (guild_id, user_id, username, action_type, content) VALUES (?, ?, ?, 'EDITCHANNEL', ?)", (after.guild.id, entry.user.id, entry.user.name, f"Смена категории канала {before_cat} → {after_cat}"))
        connection.commit()

    @commands.Cog.listener()
    async def on_voice_state_update(self, member: disnake.Member, before: disnake.VoiceState, after: disnake.VoiceState):
        if not self.is_enabled(member.guild.id) or (member.bot and self.should_ignore_bots(member.guild.id)):
            return

        cursor.execute("SELECT log_voice_channel_events FROM settings WHERE guild_id = ?", (member.guild.id,))
        if cursor.fetchone() is None or False:
            return

        if before.channel is None and after.channel is not None:
            cursor.execute("INSERT INTO logs_server (guild_id, user_id, username, action_type, content) VALUES (?, ?, ?, 'VOICECHANNEL', ?)", (member.guild.id, member.id, member.name, f"Зашел в канал {after.channel.name}"))
        elif before.channel is not None and after.channel is None:
            cursor.execute("INSERT INTO logs_server (guild_id, user_id, username, action_type, content) VALUES (?, ?, ?, 'VOICECHANNEL', ?)", (member.guild.id, member.id, member.name, f"Вышел с канала {before.channel.name}"))
        elif before.channel != after.channel:
            cursor.execute("INSERT INTO logs_server (guild_id, user_id, username, action_type, content) VALUES (?, ?, ?, 'VOICECHANNEL', ?)", (member.guild.id, member.id, member.name, f"Перемещение из {before.channel.name} в {after.channel.name}"))
        connection.commit()

    @commands.Cog.listener()
    async def on_invite_create(self, invite: disnake.Invite):
        if not self.is_enabled(invite.guild.id) or (invite.inviter.bot and self.should_ignore_bots(invite.guild.id)):
            return

        cursor.execute("SELECT log_invites FROM settings WHERE guild_id = ?", (invite.guild.id,))
        if cursor.fetchone() is None or False:
            return

        if invite.max_age == 0:
            expire = "Бессрочно"
        else:
            expire = f"{invite.max_age // 60} мин."

        if invite.max_uses == 0:
            uses = "Бесконечно"
        else:
            uses = invite.max_uses

        content = (f"Создано приглашение: {invite.code} | Канал: {invite.channel.name} | Срок: {expire} | Использований: {uses} | Временное: {'Да' if invite.temporary else 'Нет'}")
        cursor.execute("INSERT INTO logs_server (guild_id, user_id, username, action_type, content) VALUES (?, ?, ?, 'INVITES', ?)", (invite.guild.id, invite.inviter.id, invite.inviter.name, content))
        connection.commit()

    @commands.Cog.listener()
    async def on_application_command(self, interaction: disnake.ApplicationCommandInteraction):
        if not self.is_enabled(interaction.guild.id) or (interaction.author.bot and self.should_ignore_bots(interaction.guild.id)):
            return

        cursor.execute("SELECT log_command_usage FROM settings WHERE guild_id = ?", (interaction.guild.id,))
        if cursor.fetchone() is None or False:
            return

        content = f"Пользователь использовал команду /{interaction.application_command.name}. Приложение: {interaction.client.user.name}"
        cursor.execute("INSERT INTO logs_other (guild_id, user_id, username, action_type, content) VALUES (?, ?, ?, 'USECOMMAND', ?)", (interaction.guild.id, interaction.author.id, interaction.author.name, content))
        connection.commit()

    @commands.Cog.listener()
    async def on_guild_emojis_update(self, guild: disnake.Guild, before: disnake.Emoji, after: disnake.Emoji):
        if not self.is_enabled(guild.guild.id):
            return

        cursor.execute("SELECT log_emoji_changes FROM settings WHERE guild_id = ?", (guild.id,))
        if cursor.fetchone() is None or False:
            return

        pass

    @commands.Cog.listener()
    async def on_guild_stickers_update(self, guild: disnake.Guild, before: disnake.Emoji, after: disnake.Emoji):
        if not self.is_enabled(guild.guild.id):
            return

        cursor.execute("SELECT log_sticker_changes FROM settings WHERE guild_id = ?", (guild.id,))
        if cursor.fetchone() is None or False:
            return

        pass

def setup(bot: commands.Bot):
    bot.add_cog(LogsCog(bot))
