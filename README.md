<div align="center">
<img width="250" alt="Discord Log Hub Logo" src="https://cdn.imgchest.com/files/f97b4f383b68.png" />

# Discord Log Hub
**Мощная и гибкая система логирования для ваших Discord-сообществ**

[![Версия](https://img.shields.io/badge/Версия-1.1.0-blue?style=for-the-badge&logo=github)](https://github.com/Dimentiy-cmd/Discord-Log-Hub/releases)
[![Лицензия](https://img.shields.io/badge/Лицензия-MIT-green?style=for-the-badge&logo=opensourceinitiative)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-3.1.2-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![Disnake](https://img.shields.io/badge/Disnake-2.11.0-7289DA?style=for-the-badge&logo=discord&logoColor=white)](https://disnake.dev/)

</div>

## 📋 О проекте

Discord Log Hub позволяет записывать, хранить и просматривать все ключевые события вашего Discord-сервера в удобном веб-интерфейсе. Управляйте настройками прямо из Discord и получите полный контроль над активностью сообщества.

## ✨ Возможности

### 📝 Всестороннее логирование
- **Сообщения**: отслеживание редактирования и удаления
- **Участники**: вход, выход, изменение никнейма, блокировки
- **Сервер**: управление ролями, каналами, приглашениями
- **Голосовые каналы**: подключения, отключения, перемещения

### ⚙️ Удобное управление
- Настройка через привычные Discord-команды
- Гибкая конфигурация событий для логирования
- Настройка цветов системных сообщений

### 🗄️ Архив и поиск
- Веб-интерфейс для просмотра логов
- Удобный поиск и фильтрация
- Долгосрочное хранение

### 🔒 Приватность и безопасность
- Полный контроль над данными
- Возможность self-hosting

## 🚀 Быстрый старт

### 🛠️ Требования
- Python 3.8 или выше
- Windows или любой современный дистрибутив Linux
- Git

### 🐧 Установка на сервер (протестировано на Debian/Fedora)

Арендуйте VPS/VDS у любого провайдера. После создания сервера подключитесь к нему через SSH:

```bash
ssh root@server-ip
```

Вводим пароль от сервера который был выслан на почту/выдан при покупке. Обновляем пакетный менеджер:

Если у вас Debian/Ubuntu:

```bash
sudo apt update && sudo apt upgrade -y
```

Если у вас Fedora:

```
sudo dnf update && sudo dnf upgrade
```

Устанавливаем docker через официальный скрипт:

```bash
curl -fsSL https://get.docker.com | sudo sh
```

Клонируем репозиторий:

```bash
git clone https://github.com/Dimentiy-cmd/Discord-Log-Hub && cd Discord-Log-Hub
```

Создаем и редактируем .env файл:

```bash
cp .env.example .env && nano .env
```

В строку `TOKEN=""` вставляем токен от бота. Запускаем контейнер:

```
docker compose up -d
```

Приглашаем бота на сервер и выдаем ему права администратора. После установки запускаем команду `/setup` и в аргумент `log_url` прописываем ссылку в формате:

```
http://server-ip:5000
```

В личные сообщения бот отправит вам пароль для авторизации в веб-интерфейсе.

### Обновление

Обновляем репозиторий через git:

```bash
git fetch && git pull
```

Пересобираем контейнер:

```bash
docker compose up -d --build
```
## 🤝 Поддержка и сообщество

### 🆘 Нужна помощь?
- 🐛 **Баги**: [Создать issue](https://github.com/Dimentiy-cmd/Discord-Log-Hub/issues/new?template=bug_report.md)
- 💡 **Предложения**: [Feature Request](https://github.com/Dimentiy-cmd/Discord-Log-Hub/issues/new?template=feature_request.md)
- 💬 **Обсуждения**: [GitHub Discussions](https://github.com/Dimentiy-cmd/Discord-Log-Hub/discussions)

### 📞 Связь с разработчиком
- **Discord**: [@dimenciti](https://discord.com)
- **Telegram**: [@amyde3600](https://t.me/amyde3600)

## 🤝 Участие в разработке

Мы приветствуем вклад в развитие проекта!

1. Форкните репозиторий
2. Создайте ветку для вашей фичи (`git checkout -b feature/amazing-feature`)
3. Сделайте коммит (`git commit -m 'Add amazing feature'`)
4. Пушьте в ветку (`git push origin feature/amazing-feature`)
5. Откройте Pull Request

## 📄 Лицензия

Этот проект распространяется под [MIT License](LICENSE.md). Вы можете свободно использовать, модифицировать и распространять код.

---

<div align="center">
  <p>Сделано с ❤️ для Discord-сообществ</p>
  <p>
    <a href="#top">⬆️ Наверх</a>
  </p>
</div>
