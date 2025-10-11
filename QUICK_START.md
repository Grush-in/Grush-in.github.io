# ⚡ Быстрый старт - Интеграция плагина статистики

## 📋 Что нужно сделать

1. ✅ Выбрать способ приема статистики (Vercel или GitHub Actions)
2. ✅ Настроить API endpoint
3. ✅ Обновить настройки бота
4. ✅ Проверить что все работает

---

## 🎯 Способ 1: Vercel (Рекомендуется)

### Преимущества:
- ✅ Быстро и просто
- ✅ Автоматическое масштабирование
- ✅ Встроенный мониторинг
- ✅ Бесплатный план (100GB/месяц)

### Шаги:

#### 1. Установите Vercel CLI
```bash
npm install -g vercel
```

#### 2. Создайте GitHub Personal Access Token
1. Откройте https://github.com/settings/tokens
2. "Generate new token (classic)"
3. Выберите права: **repo** (full control)
4. Сохраните токен

#### 3. Деплой API
```bash
cd vercel-api-example
npm install
vercel login
vercel
```

#### 4. Добавьте секреты в Vercel
```bash
vercel env add GITHUB_TOKEN
# Вставьте ваш GitHub токен

vercel env add STATS_API_KEY
# Создайте секретный ключ (любая строка)
```

#### 5. Продакшн деплой
```bash
vercel --prod
```

Вы получите URL вида: `https://vpn-stats-api.vercel.app`

#### 6. Настройте бота

В `.env` файле бота (`bot_telegram/.env`):

```env
STATS_ENABLED=true
STATS_WEBSITE_URL=https://vpn-stats-api.vercel.app/api/stats
STATS_API_KEY=ваш_секретный_ключ  # Тот же что в Vercel
STATS_SEND_INTERVAL=300
```

#### 7. Перезапустите бота
```bash
cd bot_telegram
python main.py
```

✅ **Готово!** Статистика будет обновляться каждые 5 минут.

---

## 🔧 Способ 2: GitHub Actions

### Преимущества:
- ✅ Полностью бесплатно
- ✅ Не требует внешних сервисов
- ✅ Все в одном репозитории

### Недостатки:
- ⚠️ Требует изменения кода бота
- ⚠️ Лимит 2000 запусков в месяц

### Шаги:

#### 1. GitHub Actions уже настроен
Файл `.github/workflows/update-stats.yml` уже создан в репозитории.

#### 2. Создайте Personal Access Token
1. https://github.com/settings/tokens
2. "Generate new token (classic)"
3. Права: **repo** (full control)
4. Сохраните токен

#### 3. Обновите бота для работы с GitHub API

Добавьте в `bot_telegram/.env`:
```env
STATS_ENABLED=true
GITHUB_TOKEN=ghp_ваш_токен
GITHUB_REPO_OWNER=Grush-in
GITHUB_REPO_NAME=Grush-in.github.io
STATS_SEND_INTERVAL=300
```

#### 4. Обновите `stats_plugin.py` в боте

Добавьте новый метод отправки (вместо `_send_to_website`):

```python
async def _send_to_github(self, stats: Dict):
    """Отправить через GitHub Actions"""
    try:
        import os
        import requests
        
        url = f"https://api.github.com/repos/{os.getenv('GITHUB_REPO_OWNER')}/{os.getenv('GITHUB_REPO_NAME')}/dispatches"
        
        headers = {
            "Authorization": f"token {os.getenv('GITHUB_TOKEN')}",
            "Accept": "application/vnd.github.v3+json"
        }
        
        payload = {
            "event_type": "update-stats",
            "client_payload": {
                "stats": stats
            }
        }
        
        loop = asyncio.get_event_loop()
        
        def send_request():
            response = requests.post(url, headers=headers, json=payload, timeout=10)
            if response.status_code == 204:
                logger.info("✅ Статистика отправлена в GitHub Actions")
                return True
            else:
                logger.warning(f"⚠️ GitHub API вернул статус {response.status_code}")
                return False
        
        await loop.run_in_executor(None, send_request)
        
    except Exception as e:
        logger.error(f"❌ Ошибка отправки в GitHub: {e}")
```

И замените вызов в методе `_send_stats`:
```python
# Отправляем через GitHub Actions
await self._send_to_github(stats)
```

#### 5. Перезапустите бота
```bash
cd bot_telegram
python main.py
```

✅ **Готово!** Статистика будет обновляться каждые 5 минут через GitHub Actions.

---

## 🧪 Тестирование

### 1. Проверьте логи бота
```
✅ VPN Stats Plugin инициализирован
   Приложение: RunaVPN Bot
   URL сайта: https://...
   Интервал отправки: 300с
🚀 Запуск VPN Stats Plugin...
📊 Статистика:
   👥 Онлайн: X
   👤 Всего пользователей: Y
✅ Статистика отправлена на ...
```

### 2. Проверьте что `stats.json` обновился
```bash
# Откройте репозиторий на GitHub
# Проверьте что stats.json имеет свежий commit
```

### 3. Проверьте сайт
1. Откройте https://grush-in.github.io
2. Перейдите на вкладку "Сервисы"
3. Кликните на "VPN Service"
4. Проверьте что данные отображаются

Откройте консоль (F12) и посмотрите:
```
✅ VPN статистика загружена: {...}
```

---

## 🔍 Troubleshooting

### Статистика не обновляется на сайте

**Решение 1: Очистите кэш браузера**
- Нажмите Ctrl+Shift+R (Windows) или Cmd+Shift+R (Mac)

**Решение 2: Проверьте что stats.json обновлен**
- Откройте https://github.com/Grush-in/Grush-in.github.io/blob/main/stats.json
- Проверьте дату последнего коммита

**Решение 3: Проверьте консоль браузера**
- Откройте F12 → Console
- Ищите ошибки загрузки

### Бот не отправляет статистику

**Проверьте логи бота:**
```bash
cd bot_telegram
python main.py
# Ищите строки с "Stats Plugin"
```

**Проверьте .env файл:**
- STATS_ENABLED=true
- URL правильный
- Токены установлены

**Проверьте что бот работает:**
- Отправьте боту /start
- Проверьте что он отвечает

### Vercel API возвращает ошибку

**401 Unauthorized:**
- Проверьте STATS_API_KEY в боте и Vercel

**403 Forbidden (GitHub):**
- Проверьте GITHUB_TOKEN
- Убедитесь что токен имеет права `repo`

**500 Internal Server Error:**
- Откройте Vercel Dashboard → Functions → Logs
- Посмотрите детали ошибки

---

## 📊 Что дальше?

### Опционально: Telegram уведомления

Добавьте в `.env` бота:
```env
STATS_TELEGRAM_BOT_TOKEN=токен_отдельного_бота
STATS_TELEGRAM_CHAT_ID=ваш_chat_id
```

Вы будете получать уведомления в Telegram каждые 5 минут.

### Опционально: Изменить интервал отправки

```env
STATS_SEND_INTERVAL=600  # 10 минут
```

### Опционально: Кастомизация отображения

Отредактируйте `index.html`:
- Измените цвета
- Добавьте графики
- Измените расположение элементов

---

## 📞 Поддержка

Если что-то не работает:

1. ✅ Проверьте логи бота
2. ✅ Проверьте консоль браузера (F12)
3. ✅ Проверьте что API endpoint работает
4. ✅ Проверьте GitHub Actions (если используете)

---

## 🎉 Готово!

Теперь статистика вашего VPN бота отображается на сайте в реальном времени!

**Полная документация:** `STATS_INTEGRATION_GUIDE.md`

---

**Время настройки:** ~15 минут  
**Сложность:** ⭐⭐☆☆☆ (Легко)


