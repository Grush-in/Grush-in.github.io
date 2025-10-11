# 🚀 НАЧНИТЕ ЗДЕСЬ - GitHub Actions Setup

## ⚡ Быстрая настройка (15 минут)

### Шаг 1: Создайте GitHub токен (2 минуты)

1. Откройте: https://github.com/settings/tokens
2. "Generate new token (classic)"
3. Выберите права: ✅ **repo**
4. "Generate token"
5. Скопируйте токен: `ghp_xxxxxxxxxxxxx`

### Шаг 2: Обновите config.py (1 минута)

Откройте `bot_telegram/config.py` и добавьте в конец:

```python
# GitHub Integration
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN', '')
GITHUB_REPO_OWNER = os.getenv('GITHUB_REPO_OWNER', 'Grush-in')
GITHUB_REPO_NAME = os.getenv('GITHUB_REPO_NAME', 'Grush-in.github.io')
```

### Шаг 3: Обновите stats_plugin.py (5 минут)

1. Откройте `bot_telegram/stats_plugin.py`
2. Найдите метод `_send_to_website` (строка ~224)
3. Откройте файл `bot_telegram/stats_plugin_github_actions_update.py`
4. Скопируйте весь код метода оттуда
5. Замените метод `_send_to_website` в `stats_plugin.py`

### Шаг 4: Настройте .env (2 минуты)

Откройте `bot_telegram/.env` и добавьте:

```env
STATS_ENABLED=true
GITHUB_TOKEN=ghp_ваш_токен_сюда
GITHUB_REPO_OWNER=Grush-in
GITHUB_REPO_NAME=Grush-in.github.io
STATS_SEND_INTERVAL=300
```

### Шаг 5: Запустите бота (1 минута)

```bash
cd bot_telegram
python main.py
```

Ищите в логах:
```
✅ Статистика отправлена в GitHub Actions
```

### Шаг 6: Проверьте работу (3 минуты)

1. **GitHub Actions:** https://github.com/Grush-in/Grush-in.github.io/actions
   - Должен быть workflow "Update VPN Stats" с ✅

2. **stats.json:** https://github.com/Grush-in/Grush-in.github.io/blob/main/stats.json
   - Должен обновиться

3. **Сайт:** https://grush-in.github.io
   - Вкладка "Сервисы" → "VPN Service"
   - Данные должны отображаться!

---

## 📚 Полная документация

- **GITHUB_ACTIONS_SETUP.md** - Подробная пошаговая инструкция
- **STATS_INTEGRATION_GUIDE.md** - Полное руководство по интеграции
- **QUICK_START.md** - Сравнение Vercel vs GitHub Actions

---

## ❌ Проблемы?

### Ошибка 401 (Unauthorized)
→ Проверьте что GITHUB_TOKEN правильный

### Ошибка 404 (Not Found)
→ Проверьте GITHUB_REPO_OWNER и GITHUB_REPO_NAME

### Ошибка 403 (Forbidden)
→ Токен должен иметь права **repo**

### Workflow не запускается
→ Settings → Actions → "Allow all actions"

---

## ✅ Готово!

После настройки:
- 🤖 Бот отправляет статистику каждые 5 минут
- ⚙️ GitHub Actions автоматически обновляет stats.json
- 🌐 Сайт показывает данные каждые 30 секунд

**Удачи! 🚀**

