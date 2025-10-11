# 🔧 Настройка через GitHub Actions - Пошаговая инструкция

## ✅ Что у нас уже есть

- ✅ Workflow файл создан (`.github/workflows/update-stats.yml`)
- ✅ Сайт готов к отображению статистики
- ✅ `stats.json` создан

## 📋 Что нужно сделать

1. Создать GitHub Personal Access Token
2. Обновить код бота для работы с GitHub Actions
3. Настроить .env файл бота
4. Перезапустить бота
5. Проверить работу

---

## 🔑 Шаг 1: Создайте GitHub Personal Access Token

### 1.1 Откройте настройки GitHub

Перейдите на: https://github.com/settings/tokens

### 1.2 Создайте новый токен

1. Нажмите **"Generate new token"** → **"Generate new token (classic)"**
2. Введите название: `VPN Bot Stats`
3. Выберите срок действия: `No expiration` (или на ваше усмотрение)
4. Выберите права доступа:
   - ✅ **repo** (полный доступ к репозиториям)
   - Это даст доступ к:
     - repo:status
     - repo_deployment
     - public_repo
     - repo:invite
     - security_events

### 1.3 Создайте токен

1. Нажмите **"Generate token"**
2. **ВАЖНО:** Скопируйте токен и сохраните в безопасном месте!
3. Токен выглядит так: `ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxx`

⚠️ **Внимание:** Токен показывается только один раз! Сохраните его.

---

## 🔧 Шаг 2: Обновите код бота

### 2.1 Обновите config.py

Откройте файл `bot_telegram/config.py` и добавьте в конец:

```python
# ============================================================================
# GitHub Integration для статистики через GitHub Actions
# ============================================================================
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN', '')
GITHUB_REPO_OWNER = os.getenv('GITHUB_REPO_OWNER', 'Grush-in')
GITHUB_REPO_NAME = os.getenv('GITHUB_REPO_NAME', 'Grush-in.github.io')
```

### 2.2 Обновите stats_plugin.py

Откройте файл `bot_telegram/stats_plugin.py` и найдите метод `_send_to_website` (примерно строка 224).

**ЗАМЕНИТЕ** весь метод на:

```python
async def _send_to_website(self, stats: Dict):
    """Отправить статистику через GitHub Actions"""
    try:
        import os
        
        # Импортируем настройки GitHub
        try:
            from config import GITHUB_TOKEN, GITHUB_REPO_OWNER, GITHUB_REPO_NAME
        except ImportError:
            logger.error("❌ Не найдены настройки GitHub в config.py")
            return
        
        # Проверяем что токен установлен
        if not GITHUB_TOKEN:
            logger.warning("⚠️  GITHUB_TOKEN не установлен в .env")
            logger.warning("    Установите GITHUB_TOKEN для отправки статистики")
            return
        
        # URL GitHub API для repository_dispatch
        url = f"https://api.github.com/repos/{GITHUB_REPO_OWNER}/{GITHUB_REPO_NAME}/dispatches"
        
        # Заголовки для GitHub API
        headers = {
            "Authorization": f"token {GITHUB_TOKEN}",
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "RunaVPN-Bot-Stats-Plugin/1.0"
        }
        
        # Payload для GitHub Actions
        payload = {
            "event_type": "update-stats",
            "client_payload": {
                "stats": stats
            }
        }
        
        # Функция для синхронного запроса
        def send_request():
            try:
                response = requests.post(url, headers=headers, json=payload, timeout=10)
                
                if response.status_code == 204:
                    logger.info(f"✅ Статистика отправлена в GitHub Actions")
                    logger.info(f"   Репозиторий: {GITHUB_REPO_OWNER}/{GITHUB_REPO_NAME}")
                    return True
                elif response.status_code == 401:
                    logger.error(f"❌ Неверный GitHub токен (401 Unauthorized)")
                    logger.error(f"   Проверьте GITHUB_TOKEN в .env")
                    return False
                elif response.status_code == 404:
                    logger.error(f"❌ Репозиторий не найден (404 Not Found)")
                    logger.error(f"   Проверьте GITHUB_REPO_OWNER и GITHUB_REPO_NAME")
                    return False
                elif response.status_code == 403:
                    logger.error(f"❌ Нет доступа (403 Forbidden)")
                    logger.error(f"   Убедитесь что токен имеет права 'repo'")
                    return False
                else:
                    logger.warning(f"⚠️  GitHub API вернул статус {response.status_code}")
                    try:
                        error_data = response.json()
                        logger.warning(f"   Ошибка: {error_data.get('message', 'Unknown')}")
                    except:
                        logger.warning(f"   Response: {response.text[:200]}")
                    return False
            
            except requests.exceptions.Timeout:
                logger.error(f"❌ Timeout при отправке в GitHub")
                return False
            except requests.exceptions.RequestException as e:
                logger.error(f"❌ Ошибка отправки в GitHub: {e}")
                return False
        
        # Запускаем в отдельном потоке
        loop = asyncio.get_event_loop()
        success = await loop.run_in_executor(None, send_request)
        
        if success:
            logger.info(f"   Workflow должен запуститься в течение нескольких секунд")
    
    except Exception as e:
        logger.error(f"❌ Ошибка при отправке через GitHub Actions: {e}")
        import traceback
        logger.error(traceback.format_exc())
```

### 2.3 Сохраните изменения

Убедитесь что оба файла сохранены.

---

## ⚙️ Шаг 3: Настройте .env файл бота

Откройте файл `bot_telegram/.env` и добавьте/обновите следующие строки:

```env
# ============================================================================
# Stats Plugin - Настройки для GitHub Actions
# ============================================================================

# Включить плагин статистики
STATS_ENABLED=true

# GitHub Token (создали на шаге 1)
GITHUB_TOKEN=ghp_ваш_токен_сюда

# Информация о репозитории
GITHUB_REPO_OWNER=Grush-in
GITHUB_REPO_NAME=Grush-in.github.io

# Интервал отправки статистики (секунды)
STATS_SEND_INTERVAL=300

# Опционально: уведомления в Telegram (оставьте пустым если не нужно)
STATS_TELEGRAM_BOT_TOKEN=
STATS_TELEGRAM_CHAT_ID=

# Старые настройки (больше не нужны для GitHub Actions, но оставьте на всякий случай)
STATS_WEBSITE_URL=https://grush-in.github.io/api/stats
```

**Замените:**
- `ghp_ваш_токен_сюда` на ваш реальный токен из шага 1
- `Grush-in` на ваш GitHub username (если отличается)
- `Grush-in.github.io` на имя вашего репозитория (если отличается)

---

## 🚀 Шаг 4: Перезапустите бота

### 4.1 Остановите бота (если он запущен)

```bash
# Нажмите Ctrl+C в терминале где запущен бот
```

### 4.2 Запустите бота

```bash
cd bot_telegram
python main.py
```

### 4.3 Проверьте логи

Вы должны увидеть:

```
✅ VPN Stats Plugin инициализирован
   Приложение: RunaVPN Bot
   Интервал отправки: 300с
🚀 Запуск VPN Stats Plugin...
✅ VPN Stats Plugin запущен

# Через 5 минут (или при активности пользователей):
📊 Статистика:
   👥 Онлайн: X
   👤 Всего пользователей: Y
   🔑 Активных ключей: Z
   💰 Выручка сегодня: N₽
✅ Статистика отправлена в GitHub Actions
   Репозиторий: Grush-in/Grush-in.github.io
   Workflow должен запуститься в течение нескольких секунд
```

---

## ✅ Шаг 5: Проверьте работу

### 5.1 Проверьте GitHub Actions

1. Откройте: https://github.com/Grush-in/Grush-in.github.io/actions
2. Должен появиться workflow run **"Update VPN Stats"**
3. Кликните на него
4. Проверьте что он выполнился успешно (зеленая галочка ✅)

### 5.2 Проверьте stats.json

1. Откройте: https://github.com/Grush-in/Grush-in.github.io/blob/main/stats.json
2. Проверьте что файл обновился (должен быть свежий commit)
3. Проверьте что данные корректные

### 5.3 Проверьте сайт

1. Откройте: https://grush-in.github.io
2. Нажмите на вкладку **"Сервисы"**
3. Кликните на **"VPN Service"**
4. Проверьте что данные отображаются!

### 5.4 Проверьте консоль браузера

1. Откройте консоль (F12)
2. Должно быть: `✅ VPN статистика загружена: {...}`

---

## 🧪 Тестирование

### Тест 1: Ручной запуск Workflow

1. Откройте: https://github.com/Grush-in/Grush-in.github.io/actions
2. Выберите workflow **"Update VPN Stats"**
3. Нажмите **"Run workflow"** → **"Run workflow"**
4. Проверьте что он выполнился успешно

### Тест 2: Симуляция активности в боте

```bash
# В боте отправьте команду
/start
```

Плагин отметит вас как онлайн пользователя.

### Тест 3: Проверка времени обновления

На сайте в VPN Service внизу должно быть:
```
Обновлено: только что
```

или

```
Обновлено: 5 мин назад
```

---

## ❌ Возможные проблемы и решения

### Проблема 1: "Unauthorized" (401)

**Причина:** Неверный или истекший GitHub токен

**Решение:**
1. Проверьте что GITHUB_TOKEN в .env правильный
2. Проверьте что токен не истек
3. Создайте новый токен если нужно

### Проблема 2: "Not Found" (404)

**Причина:** Неправильное имя репозитория или владельца

**Решение:**
1. Проверьте GITHUB_REPO_OWNER (должно быть ваш username)
2. Проверьте GITHUB_REPO_NAME (должно быть имя репозитория)
3. Убедитесь что репозиторий существует

### Проблема 3: "Forbidden" (403)

**Причина:** Токен не имеет нужных прав

**Решение:**
1. Создайте новый токен
2. Убедитесь что выбрали права **repo** (полный доступ)

### Проблема 4: Workflow не запускается

**Причина:** Workflow может быть отключен

**Решение:**
1. Откройте: https://github.com/Grush-in/Grush-in.github.io/settings/actions
2. В "Actions permissions" выберите "Allow all actions and reusable workflows"
3. Проверьте что workflow включен в списке workflows

### Проблема 5: stats.json не обновляется

**Причина:** Ошибка в workflow или нет прав на запись

**Решение:**
1. Откройте логи workflow в GitHub Actions
2. Проверьте есть ли ошибки
3. Убедитесь что токен имеет права на запись

### Проблема 6: Сайт показывает старые данные

**Причина:** Кэш браузера

**Решение:**
1. Нажмите Ctrl+Shift+R (Windows) или Cmd+Shift+R (Mac)
2. Очистите кэш браузера
3. Подождите 30 секунд и обновите страницу

---

## 📊 Мониторинг

### Логи бота

Смотрите вывод в терминале где запущен бот:
```bash
cd bot_telegram
python main.py
```

### GitHub Actions Logs

1. Откройте: https://github.com/Grush-in/Grush-in.github.io/actions
2. Кликните на последний run
3. Кликните на job "update-stats"
4. Смотрите подробные логи каждого шага

### Консоль браузера

1. Откройте сайт
2. Нажмите F12
3. Перейдите на вкладку Console
4. Смотрите сообщения о загрузке статистики

---

## 🎯 Итоговый чеклист

- [ ] Создан GitHub Personal Access Token
- [ ] Токен имеет права **repo**
- [ ] Обновлен `config.py` (добавлены GITHUB_*)
- [ ] Обновлен `stats_plugin.py` (заменен метод `_send_to_website`)
- [ ] Обновлен `.env` (добавлены GITHUB_TOKEN, GITHUB_REPO_*)
- [ ] Бот перезапущен
- [ ] В логах бота: "✅ Статистика отправлена в GitHub Actions"
- [ ] В GitHub Actions появился workflow run
- [ ] Workflow выполнился успешно (зеленая галочка)
- [ ] `stats.json` обновился в репозитории
- [ ] Сайт отображает данные
- [ ] Нет ошибок в консоли браузера

---

## 🎉 Готово!

Поздравляю! Теперь статистика автоматически обновляется через GitHub Actions!

**Как это работает:**
1. 🤖 Бот собирает статистику каждые 5 минут
2. 📡 Отправляет событие в GitHub через API
3. ⚙️ GitHub Actions запускается автоматически
4. 📝 Обновляет `stats.json` в репозитории
5. 🌐 Сайт загружает свежие данные каждые 30 секунд

**Преимущества GitHub Actions:**
- ✅ Полностью бесплатно
- ✅ Не нужны внешние сервисы
- ✅ Все в одном репозитории
- ✅ 2000 минут в месяц бесплатно (более чем достаточно)

---

## 📞 Нужна помощь?

Если что-то не работает:
1. Проверьте раздел "Возможные проблемы" выше
2. Проверьте логи (бот + GitHub Actions)
3. Убедитесь что все шаги выполнены
4. Проверьте что токен правильный и не истек

**Удачи! 🚀**

