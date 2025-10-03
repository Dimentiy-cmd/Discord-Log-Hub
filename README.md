<div align="center">
<img width="250" alt="Discord Log Hub Logo" src="https://cdn.imgchest.com/files/f97b4f383b68.png" />

# Discord Log Hub
**Мощная и гибкая система логирования для Discord-серверов**

[![Версия](https://img.shields.io/badge/Версия-1.0.0-blue?style=for-the-badge&logo=github)](https://github.com/Dimentiy-cmd/Discord-Log-Hub/releases)
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

### Требования
- Python 3.8 или выше
- Windows или Linux дистрибутив
- Git

### 🪟 Установка на Windows

Перед началом убедитесь, что у вас установлен Python и Git.

1. **Клонируйте репозиторий**
   ```bash
   git clone https://github.com/Dimentiy-cmd/Discord-Log-Hub
   cd Discord-Log-Hub
   ```

2. **Запустите установщик**
   ```cmd
   setup.exe
   ```
   > Следуйте инструкциям для создания всех нужных файлов

3. **Установите зависимости**
   ```cmd
   pip install -r requirements.txt
   ```

4. **Запустите приложение**
   ```cmd
   python main.py
   ```

### 🐧 Установка на Linux

Перед началом убедитесь, что у вас установлен Python и Git.

```bash
sudo apt install git python3 python3-pip python3-venv
```

1. **Клонируйте репозиторий**
   ```bash
   git clone https://github.com/Dimentiy-cmd/Discord-Log-Hub
   cd Discord-Log-Hub
   ```

2. **Запустите установщик**
   ```bash
   chmod +x setup
   ./setup
   ```
   > Следуйте инструкциям для создания всех нужных файлов

3. **Создайте и активируйте виртуальное окружение**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

4. **Установите зависимости**
   ```bash
   pip install -r requirements.txt
   ```

5. **Запустите приложение**
   ```bash
   python main.py
   ```

6. **Деактивируйте виртуальное окружение** (опционально)
   ```bash
   deactivate
   ```

## 🌐 Деплой

### ☁️ Amvera Cloud

1. **Подготовьте проект локально**
   ```bash
   git clone https://github.com/Dimentiy-cmd/Discord-Log-Hub
   cd Discord-Log-Hub
   ```

2. **Запустите setup** (Windows или Linux в зависимости от вашей ОС) и следуйте инструкциям для создания всех нужных файлов.

3. **Создайте проект на Amvera**
   - Зарегистрируйтесь на [Amvera Cloud](https://amvera.ru)
   - Нажмите "Создать проект" → "Приложение"
   - Введите название и выберите тариф

4. **Подключите репозиторий**
   ```bash
   git remote add amvera https://git.amvera.ru/<имя-пользователя>/<название-проекта>
   ```

5. **Загрузите код**
   ```bash
   git add .
   git commit -m "Initial commit"
   git push amvera master
   ```

6. **Настройте домен** (опционально)
   - В настройках проекта: "Домены" → "Создать доменное имя"
   - Выберите "HTTPS" и "Бесплатный домен Амвера"

> 🚀 Сборка запустится автоматически и проект будет доступен через несколько минут

## 🛠️ Технический стек

| Компонент | Технология |
|-----------|------------|
| **Backend** | Python, Flask, Disnake |
| **Frontend** | HTML, CSS, JavaScript |
| **База данных** | SQLite |

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
