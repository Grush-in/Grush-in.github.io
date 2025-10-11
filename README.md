# 🌐 Grush-in.github.io - Portfolio & VPN Stats

Персональное портфолио с интеграцией реальной статистики VPN бота.

## ✨ Особенности

- 🎨 **Современный дизайн** - Cyberpunk-стиль с энергетическими эффектами
- 📱 **Адаптивная верстка** - Отлично работает на всех устройствах
- 📊 **Живая статистика** - Реальные данные от VPN бота
- 🚀 **GitHub Pages** - Бесплатный хостинг
- ⚡ **Быстрая загрузка** - Оптимизированный код

## 🎯 Секции

1. **Обо мне** - Hard Skills, образование, интересы
2. **Pet-проекты** - Автоматическая загрузка из GitHub
3. **Сервисы** - Живая статистика VPN Service
4. **Roadmap** - Планы развития

## 📊 VPN Stats Integration

Сайт автоматически отображает статистику от Telegram бота:

- 👥 Пользователи онлайн
- 🔑 Активные подписки
- 💰 Выручка за сегодня
- 📈 Транзакции

### Как это работает:

1. **Бот собирает статистику** каждые 5 минут
2. **Отправляет на API endpoint** (Vercel или GitHub Actions)
3. **API сохраняет в stats.json** в этом репозитории
4. **Сайт загружает stats.json** каждые 30 секунд

## 🚀 Быстрый старт

### Для просмотра сайта:

Просто откройте: https://grush-in.github.io

### Для интеграции своей статистики:

1. **Прочитайте руководство:**
   - [Быстрый старт](QUICK_START.md) - Начните здесь ⚡
   - [Полная документация](STATS_INTEGRATION_GUIDE.md) - Детальное руководство 📖

2. **Выберите способ:**
   - [Vercel API](vercel-api-example/) - Рекомендуется 🌟
   - [GitHub Actions](.github/workflows/update-stats.yml) - Бесплатная альтернатива

3. **Настройте за 15 минут:**
   - Создайте API endpoint
   - Обновите настройки бота
   - Проверьте что все работает

## 📁 Структура проекта

```
.
├── index.html                          # Главная страница
├── stats.json                          # Текущая статистика
├── api_stats_receiver.html             # Демо-страница для тестирования
├── QUICK_START.md                      # Быстрый старт (начните здесь!)
├── STATS_INTEGRATION_GUIDE.md          # Полная документация
├── fonts/                              # Кастомные шрифты
├── images/                             # Изображения
├── vercel-api-example/                 # Пример API для Vercel
│   ├── api/stats.js                   # API endpoint
│   ├── package.json                   # Зависимости
│   └── README.md                      # Инструкции по деплою
└── .github/
    └── workflows/
        └── update-stats.yml            # GitHub Actions workflow
```

## 🛠️ Технологии

- **Frontend:** HTML5, CSS3, JavaScript (Vanilla)
- **Дизайн:** Cyberpunk UI, энергетические эффекты
- **API:** Vercel Serverless Functions / GitHub Actions
- **Хостинг:** GitHub Pages
- **Интеграция:** GitHub API, Octokit

## 🎨 Кастомизация

### Изменить информацию "Обо мне"

Отредактируйте `index.html`, секция `<div class="hero">`:
- Имя и должность
- Hard Skills
- Образование
- Интересы

### Изменить GitHub проекты

В `index.html` найдите:
```javascript
const GITHUB_USER = 'Grush-in';  // Ваш GitHub username
```

### Изменить дизайн

CSS переменные в `index.html`:
```css
:root{
  --bg:#0d0f14;           /* Фон */
  --primary:#a855f7;      /* Основной цвет */
  --primary-2:#3bb7ff;    /* Второй цвет */
  --ok:#18cc8b;           /* Успех */
  --danger:#ff5577;       /* Ошибка */
}
```

## 📊 Формат статистики

`stats.json` имеет следующий формат:

```json
{
  "app_name": "RunaVPN Bot",
  "timestamp": "2025-10-11T15:30:00.000000",
  "online_users": 42,
  "total_users": 1234,
  "active_keys": 89,
  "transactions_today": 12,
  "revenue_today": 1234.56,
  "new_users_today": 5,
  "uptime_seconds": 86400.0
}
```

## 🔒 Безопасность

- ✅ HTTPS везде
- ✅ API авторизация через Bearer token
- ✅ Токены в environment variables
- ✅ Валидация данных на сервере

## 📈 Roadmap

- [x] v0.1 - Базовый лендинг
- [x] v0.2 - Интеграция статистики VPN
- [ ] v0.3 - Графики и аналитика
- [ ] v0.4 - Темная/светлая тема
- [ ] v0.5 - i18n (RU/EN)

## 📝 Лицензия

MIT License - используйте свободно для личных проектов

## 🤝 Контакты

- **GitHub:** [@Grush-in](https://github.com/Grush-in)
- **Telegram:** @yourhandle
- **Email:** your@email.dev

## 🙏 Благодарности

- [GitHub Pages](https://pages.github.com/) - Бесплатный хостинг
- [Vercel](https://vercel.com/) - Serverless Functions
- [GitHub Actions](https://github.com/features/actions) - CI/CD

---

**Создано с ❤️ в 2025**

**Время работы:** v1.0.0  
**Последнее обновление:** Октябрь 2025
