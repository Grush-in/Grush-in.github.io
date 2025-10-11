# 🔄 Инструкция по обновлению бота для работы со статистикой

## 📋 Обзор

Если вы выбрали **GitHub Actions** вместо Vercel, вам нужно обновить `stats_plugin.py` в боте.

## ✅ Вариант 1: Использование Vercel (уже работает)

Если вы развернули API через Vercel, **ничего менять не нужно**!

Просто обновите `.env`:
```env
STATS_ENABLED=true
STATS_WEBSITE_URL=https://ваш-проект.vercel.app/api/stats
STATS_API_KEY=ваш_секретный_ключ
STATS_SEND_INTERVAL=300
```

## 🔧 Вариант 2: Использование GitHub Actions

### Шаг 1: Обновите `.env` в боте

```env
# Включить плагин
STATS_ENABLED=true

# GitHub настройки
GITHUB_TOKEN=ghp_ваш_токен_сюда
GITHUB_REPO_OWNER=Grush-in
GITHUB_REPO_NAME=Grush-in.github.io

# Интервал отправки
STATS_SEND_INTERVAL=300

# Опционально: уведомления в Telegram
STATS_TELEGRAM_BOT_TOKEN=
STATS_TELEGRAM_CHAT_ID=
```

### Шаг 2: Обновите `config.py` в боте

Добавьте в конец файла:

```python
# ============================================================================
# GitHub Integration для статистики
# ============================================================================
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN', '')
GITHUB_REPO_OWNER = os.getenv('GITHUB_REPO_OWNER', 'Grush-in')
GITHUB_REPO_NAME = os.getenv('GITHUB_REPO_NAME', 'Grush-in.github.io')
```

### Шаг 3: Обновите `stats_plugin.py` в боте

#### Вариант A: Полная замена метода (рекомендуется)

Замените метод `_send_to_website` на:

```python
async def _send_to_website(self, stats: Dict):
    """Отправить статистику через GitHub Actions"""
    try:
        import os
        from config import GITHUB_TOKEN, GITHUB_REPO_OWNER, GITHUB_REPO_NAME
        
        # Проверяем что токен установлен
        if not GITHUB_TOKEN:
            logger.warning("⚠️  GITHUB_TOKEN не установлен, пропускаем отправку")
            return
        
        url = f"https://api.github.com/repos/{GITHUB_REPO_OWNER}/{GITHUB_REPO_NAME}/dispatches"
        
        headers = {
            "Authorization": f"token {GITHUB_TOKEN}",
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "RunaVPN-Bot-Stats-Plugin/1.0"
        }
        
        payload = {
            "event_type": "update-stats",
            "client_payload": {
                "stats": stats
            }
        }
        
        def send_request():
            try:
                response = requests.post(url, headers=headers, json=payload, timeout=10)
                
                if response.status_code == 204:
                    logger.info(f"✅ Статистика отправлена в GitHub Actions")
                    return True
                elif response.status_code == 401:
                    logger.error(f"❌ Неверный GitHub токен (401)")
                    return False
                elif response.status_code == 404:
                    logger.error(f"❌ Репозиторий не найден (404)")
                    return False
                else:
                    logger.warning(f"⚠️  GitHub API вернул статус {response.status_code}")
                    logger.warning(f"    Response: {response.text}")
                    return False
            
            except requests.exceptions.RequestException as e:
                logger.error(f"❌ Ошибка отправки в GitHub: {e}")
                return False
        
        # Запускаем в отдельном потоке
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, send_request)
    
    except Exception as e:
        logger.error(f"❌ Ошибка при отправке через GitHub Actions: {e}")
```

#### Вариант B: Добавление нового метода (если хотите поддержать оба способа)

Добавьте новый метод в класс `VPNStatsPlugin`:

```python
async def _send_to_github_actions(self, stats: Dict):
    """Отправить через GitHub Actions"""
    try:
        import os
        from config import GITHUB_TOKEN, GITHUB_REPO_OWNER, GITHUB_REPO_NAME
        
        if not GITHUB_TOKEN:
            logger.warning("⚠️  GITHUB_TOKEN не установлен")
            return
        
        url = f"https://api.github.com/repos/{GITHUB_REPO_OWNER}/{GITHUB_REPO_NAME}/dispatches"
        
        headers = {
            "Authorization": f"token {GITHUB_TOKEN}",
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "RunaVPN-Bot-Stats-Plugin/1.0"
        }
        
        payload = {
            "event_type": "update-stats",
            "client_payload": {
                "stats": stats
            }
        }
        
        def send_request():
            response = requests.post(url, headers=headers, json=payload, timeout=10)
            if response.status_code == 204:
                logger.info("✅ Статистика отправлена в GitHub Actions")
            else:
                logger.warning(f"⚠️ GitHub API вернул статус {response.status_code}")
        
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, send_request)
        
    except Exception as e:
        logger.error(f"❌ Ошибка отправки в GitHub: {e}")
```

И обновите метод `_send_stats`:

```python
async def _send_stats(self):
    """Отправить статистику"""
    try:
        stats = await self.get_stats()
        
        # Логируем локально
        logger.info(f"📊 Статистика:")
        logger.info(f"   👥 Онлайн: {stats['online_users']}")
        logger.info(f"   👤 Всего пользователей: {stats['total_users']}")
        logger.info(f"   🔑 Активных ключей: {stats['active_keys']}")
        if 'revenue_today' in stats:
            logger.info(f"   💰 Выручка сегодня: {stats['revenue_today']:.2f}₽")
        
        # Выбираем способ отправки
        if hasattr(config, 'GITHUB_TOKEN') and config.GITHUB_TOKEN:
            # Отправляем через GitHub Actions
            await self._send_to_github_actions(stats)
        elif self.website_url:
            # Отправляем на внешний API
            await self._send_to_website(stats)
        else:
            logger.warning("⚠️  Не настроен ни один способ отправки статистики")
        
        # Отправляем в Telegram (опционально)
        if self.telegram_bot_token and self.telegram_chat_id:
            await self._send_to_telegram(stats)
    
    except Exception as e:
        logger.error(f"❌ Ошибка при отправке статистики: {e}")
```

### Шаг 4: Перезапустите бота

```bash
cd bot_telegram
python main.py
```

## 🧪 Проверка работы

### 1. Проверьте логи бота

Должно быть:
```
✅ VPN Stats Plugin инициализирован
   Приложение: RunaVPN Bot
   Интервал отправки: 300с
🚀 Запуск VPN Stats Plugin...
📊 Статистика:
   👥 Онлайн: X
   👤 Всего пользователей: Y
   🔑 Активных ключей: Z
✅ Статистика отправлена в GitHub Actions
```

### 2. Проверьте GitHub Actions

1. Откройте https://github.com/Grush-in/Grush-in.github.io/actions
2. Должен появиться новый workflow run "Update VPN Stats"
3. Проверьте что он выполнился успешно (зеленая галочка ✅)

### 3. Проверьте stats.json

1. Откройте https://github.com/Grush-in/Grush-in.github.io/blob/main/stats.json
2. Проверьте что файл обновился (свежий commit)
3. Проверьте что данные корректные

### 4. Проверьте сайт

1. Откройте https://grush-in.github.io
2. Перейдите на вкладку "Сервисы"
3. Кликните "VPN Service"
4. Данные должны отображаться!

## ❗ Возможные проблемы

### Ошибка: "Bad credentials" (401)

**Решение:**
- Проверьте что GITHUB_TOKEN правильный
- Убедитесь что токен имеет права `repo`
- Создайте новый токен если старый истек

### Ошибка: "Not Found" (404)

**Решение:**
- Проверьте GITHUB_REPO_OWNER и GITHUB_REPO_NAME
- Убедитесь что репозиторий существует
- Проверьте что токен имеет доступ к репозиторию

### GitHub Actions не запускается

**Решение:**
- Проверьте что файл `.github/workflows/update-stats.yml` существует в main ветке
- Проверьте что workflow включен (Settings → Actions → General)
- Проверьте логи бота - статус код должен быть 204

### stats.json не обновляется

**Решение:**
- Проверьте GitHub Actions logs
- Убедитесь что GITHUB_TOKEN имеет права записи
- Проверьте что workflow выполняется без ошибок

## 🔍 Отладка

### Включите детальное логирование

В `main.py` измените уровень логирования:

```python
logging.basicConfig(
    level=logging.DEBUG,  # Было: logging.INFO
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

### Тестовая отправка

Создайте файл `test_github_stats.py`:

```python
import asyncio
import os
from dotenv import load_dotenv
load_dotenv()

async def test():
    from stats_plugin import VPNStatsPlugin
    from database import db
    
    await db.init_db()
    
    plugin = VPNStatsPlugin(
        app_name="Test App",
        telegram_bot_token="",
        telegram_chat_id="",
        website_url="",  # Не используем
        database=db,
        auto_send_interval=10
    )
    
    await plugin.start()
    
    # Симулируем пользователей
    for i in range(5):
        plugin.user_online(i)
    
    # Ждем отправки
    await asyncio.sleep(15)
    
    await plugin.stop()

if __name__ == '__main__':
    asyncio.run(test())
```

Запустите:
```bash
python test_github_stats.py
```

## 📞 Нужна помощь?

1. ✅ Проверьте все логи (бот + GitHub Actions)
2. ✅ Убедитесь что все токены правильные
3. ✅ Проверьте что все файлы на месте
4. ✅ Попробуйте ручной запуск workflow в GitHub

---

**Удачи с интеграцией! 🚀**


