# 📊 Руководство по интеграции плагина статистики

## 🎯 Обзор

Этот проект теперь интегрирован с плагином статистики из вашего Telegram бота. Статистика автоматически отображается на сайте в секции **"Рабочие сервисы" → "VPN Service"**.

### Что отображается:
- 👥 **Пользователи онлайн** - активные пользователи прямо сейчас
- 👤 **Всего пользователей** - общее количество зарегистрированных
- 🔑 **Активные подписки** - количество активных VPN ключей
- 💰 **Выручка сегодня** - доход за текущий день
- 📊 **Транзакции** - количество транзакций за день
- 🆕 **Новые пользователи** - регистрации за сегодня

---

## 🚀 Быстрый старт

### Шаг 1: Настройте бота

В вашем боте (папка `bot_telegram`) плагин статистики уже установлен. Убедитесь, что в файле `.env` есть следующие настройки:

```env
# Включить плагин статистики
STATS_ENABLED=true

# URL для отправки статистики (обновите после создания API)
STATS_WEBSITE_URL=https://your-api-endpoint.vercel.app/api/stats

# Опционально: уведомления в Telegram
STATS_TELEGRAM_BOT_TOKEN=your_bot_token
STATS_TELEGRAM_CHAT_ID=your_chat_id

# Интервал отправки (300 секунд = 5 минут)
STATS_SEND_INTERVAL=300
```

### Шаг 2: Создайте API endpoint

Так как GitHub Pages поддерживает только статические файлы, вам нужен внешний API endpoint для приема статистики от бота.

#### Вариант A: Использование Vercel (Рекомендуется)

1. **Установите Vercel CLI:**
```bash
npm install -g vercel
```

2. **Создайте новую директорию для API:**
```bash
mkdir vpn-stats-api
cd vpn-stats-api
npm init -y
```

3. **Создайте файл `api/stats.js`:**
```javascript
// api/stats.js
import { Octokit } from '@octokit/rest';

const octokit = new Octokit({
  auth: process.env.GITHUB_TOKEN
});

export default async function handler(req, res) {
  // CORS headers
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  if (req.method === 'OPTIONS') {
    return res.status(200).end();
  }

  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  try {
    const stats = req.body;
    
    console.log('📊 Получена статистика:', {
      online: stats.online_users,
      total: stats.total_users,
      keys: stats.active_keys,
      revenue: stats.revenue_today
    });

    // Сохраняем в GitHub репозиторий
    const owner = 'Grush-in'; // Ваш GitHub username
    const repo = 'Grush-in.github.io'; // Ваш репозиторий
    const path = 'stats.json';
    
    // Получаем текущий SHA файла
    let sha;
    try {
      const { data } = await octokit.repos.getContent({
        owner,
        repo,
        path,
      });
      sha = data.sha;
    } catch (error) {
      // Файл не существует, создаем новый
      sha = null;
    }

    // Обновляем файл
    const content = Buffer.from(JSON.stringify(stats, null, 2)).toString('base64');
    
    await octokit.repos.createOrUpdateFileContents({
      owner,
      repo,
      path,
      message: `Update VPN stats: ${new Date().toISOString()}`,
      content,
      sha,
    });

    console.log('✅ Статистика сохранена в GitHub');
    
    return res.status(200).json({ 
      success: true,
      message: 'Stats updated successfully'
    });
    
  } catch (error) {
    console.error('❌ Ошибка:', error);
    return res.status(500).json({ 
      error: 'Internal server error',
      message: error.message
    });
  }
}
```

4. **Создайте `package.json`:**
```json
{
  "name": "vpn-stats-api",
  "version": "1.0.0",
  "dependencies": {
    "@octokit/rest": "^20.0.2"
  }
}
```

5. **Создайте `.env` файл:**
```env
GITHUB_TOKEN=your_github_personal_access_token
```

6. **Деплой на Vercel:**
```bash
vercel --prod
```

7. **Получите URL и обновите настройки бота:**
```env
STATS_WEBSITE_URL=https://your-project.vercel.app/api/stats
```

#### Вариант B: Использование GitHub Actions (Альтернатива)

Если вы не хотите использовать Vercel, можно использовать GitHub Actions для обновления файла.

1. **Создайте `.github/workflows/update-stats.yml` в репозитории сайта:**

```yaml
name: Update VPN Stats

on:
  repository_dispatch:
    types: [update-stats]

jobs:
  update-stats:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v3

      - name: Update stats.json
        run: |
          echo '${{ github.event.client_payload.stats }}' > stats.json
          
      - name: Commit and push
        run: |
          git config user.name github-actions
          git config user.email github-actions@github.com
          git add stats.json
          git commit -m "Update VPN stats [skip ci]" || exit 0
          git push
```

2. **Создайте Personal Access Token:**
   - Перейдите на https://github.com/settings/tokens
   - Generate new token (classic)
   - Выберите права: `repo` (full control)
   - Сохраните токен

3. **Обновите плагин в боте для отправки через GitHub API:**

В файле `bot_telegram/stats_plugin.py` добавьте альтернативный метод:

```python
async def _send_to_github_actions(self, stats: Dict):
    """Отправить через GitHub Actions"""
    import requests
    
    url = "https://api.github.com/repos/Grush-in/Grush-in.github.io/dispatches"
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
    
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 204:
        logger.info("✅ Статистика отправлена через GitHub Actions")
    else:
        logger.warning(f"⚠️ GitHub API вернул статус {response.status_code}")
```

И в `.env` бота:
```env
GITHUB_TOKEN=your_personal_access_token
```

---

## 📁 Структура проекта

```
Grush-in.github.io/
├── index.html                      # Главная страница (обновлена для статистики)
├── stats.json                      # Файл с текущей статистикой
├── api_stats_receiver.html         # Демо-страница для тестирования
├── STATS_INTEGRATION_GUIDE.md      # Это руководство
└── .github/
    └── workflows/
        └── update-stats.yml        # (опционально) GitHub Actions workflow
```

```
bot_telegram/
├── main.py                         # Точка входа (плагин уже подключен)
├── stats_plugin.py                 # Плагин статистики
├── config.py                       # Конфигурация (содержит STATS_*)
└── .env                            # Переменные окружения
```

---

## 🔧 Конфигурация

### Переменные окружения бота (.env)

```env
# Обязательные
STATS_ENABLED=true
STATS_WEBSITE_URL=https://your-api.vercel.app/api/stats

# Опциональные
STATS_TELEGRAM_BOT_TOKEN=          # Токен для уведомлений в Telegram
STATS_TELEGRAM_CHAT_ID=            # Chat ID для уведомлений
STATS_SEND_INTERVAL=300            # Интервал отправки (секунды)
```

### Как работает интеграция

1. **Бот собирает статистику** каждые 5 минут (или по настройке)
2. **Отправляет POST запрос** на ваш API endpoint
3. **API сохраняет данные** в `stats.json` в GitHub репозитории
4. **Сайт загружает** `stats.json` каждые 30 секунд и обновляет отображение

---

## 🧪 Тестирование

### 1. Проверьте что плагин работает в боте:

```bash
cd bot_telegram
python main.py
```

В логах должно быть:
```
✅ VPN Stats Plugin инициализирован
   Приложение: RunaVPN Bot
   URL сайта: https://...
   Интервал отправки: 300с
🚀 Запуск VPN Stats Plugin...
```

### 2. Проверьте отправку данных:

Используйте https://webhook.site для тестирования:

В `.env` бота временно установите:
```env
STATS_WEBSITE_URL=https://webhook.site/your-unique-url
```

Перезапустите бота и через 5 минут проверьте на webhook.site что данные пришли.

### 3. Проверьте отображение на сайте:

1. Откройте `index.html` в браузере
2. Перейдите на вкладку **"Сервисы"**
3. Кликните на **"VPN Service"**
4. Проверьте что данные загружаются

Откройте консоль разработчика (F12) и посмотрите:
```
✅ VPN статистика загружена: {online_users: 0, total_users: 0, ...}
```

---

## 📊 Формат данных

API endpoint получает JSON в следующем формате:

```json
{
  "app_name": "RunaVPN Bot",
  "timestamp": "2025-10-11T15:30:00.123456",
  "online_users": 42,
  "total_users": 1234,
  "active_keys": 89,
  "transactions_today": 12,
  "revenue_today": 1234.56,
  "new_users_today": 5,
  "uptime_seconds": 86400.0
}
```

Этот же формат сохраняется в `stats.json` и читается сайтом.

---

## 🎨 Кастомизация отображения

### Изменить целевую выручку для прогресс-бара

В `index.html` найдите:

```javascript
const TARGET_REVENUE = 10000;
```

Измените на желаемую сумму (в рублях).

### Изменить интервал обновления на сайте

В `index.html` найдите:

```javascript
setInterval(loadVPNStats, 30000); // 30 секунд
```

Измените `30000` на желаемое значение в миллисекундах.

### Добавить больше метрик

1. Обновите `stats_plugin.py` в боте, добавив новые поля в метод `get_stats()`
2. Обновите отображение в `index.html`, добавив новые элементы

---

## 🛡️ Безопасность

### Рекомендации:

1. ✅ **Используйте HTTPS** для всех API endpoint
2. ✅ **Добавьте авторизацию** на API (Bearer token)
3. ✅ **Не коммитьте токены** в Git (используйте `.env`)
4. ✅ **Ограничьте rate limiting** на API (например, max 1 запрос в минуту)
5. ✅ **Валидируйте данные** на сервере перед сохранением

### Пример добавления авторизации:

В `.env` бота:
```env
STATS_API_KEY=your_secret_key_12345
```

В `config.py` бота:
```python
STATS_API_KEY = os.getenv('STATS_API_KEY', '')
```

В `stats_plugin.py` (метод `_send_to_website`):
```python
headers={
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {config.STATS_API_KEY}'
}
```

В `api/stats.js` (Vercel):
```javascript
const authHeader = req.headers.authorization;
const expectedAuth = `Bearer ${process.env.STATS_API_KEY}`;

if (authHeader !== expectedAuth) {
  return res.status(401).json({ error: 'Unauthorized' });
}
```

---

## 📝 FAQ

**Q: Как часто обновляется статистика на сайте?**  
A: Бот отправляет данные каждые 5 минут, сайт проверяет обновления каждые 30 секунд.

**Q: Что делать если статистика не обновляется?**  
A: 
1. Проверьте что бот запущен и STATS_ENABLED=true
2. Проверьте логи бота на наличие ошибок
3. Проверьте что API endpoint работает (используйте webhook.site)
4. Проверьте что stats.json существует и обновляется

**Q: Можно ли использовать без API endpoint?**  
A: Да, вы можете вручную обновлять `stats.json`, но это не будет автоматическим.

**Q: Как посмотреть что данные отправляются?**  
A: Откройте консоль бота и найдите строки:
```
📊 Статистика:
   👥 Онлайн: X
✅ Статистика отправлена на ...
```

**Q: Безопасно ли показывать статистику публично?**  
A: Это зависит от вашей бизнес-модели. Рекомендуем:
- Не показывать точную выручку
- Не показывать имена пользователей
- Показывать только агрегированные данные

---

## 🎉 Готово!

Теперь статистика вашего VPN бота автоматически отображается на сайте!

### Следующие шаги:

1. ✅ Создайте API endpoint (Vercel или GitHub Actions)
2. ✅ Обновите `.env` в боте с правильным URL
3. ✅ Перезапустите бота
4. ✅ Проверьте что данные появились на сайте
5. ✅ (Опционально) Настройте уведомления в Telegram

---

## 📞 Поддержка

Если возникли проблемы:

1. Проверьте логи бота
2. Проверьте консоль браузера (F12)
3. Проверьте что API endpoint отвечает
4. Проверьте что `stats.json` обновляется

---

**Версия:** 1.0.0  
**Дата:** Октябрь 2025  
**Автор:** Grush-in Project


