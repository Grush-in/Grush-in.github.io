"""
Обновленный метод для stats_plugin.py для работы с GitHub Actions

ИНСТРУКЦИЯ:
1. Откройте bot_telegram/stats_plugin.py
2. Найдите метод _send_to_website (примерно строка 224)
3. ЗАМЕНИТЕ весь метод на код ниже
"""

async def _send_to_website(self, stats: Dict):
    """Отправить статистику через GitHub Actions"""
    try:
        import os
        
        # Импортируем настройки GitHub
        try:
            from config import GITHUB_TOKEN, GITHUB_REPO_OWNER, GITHUB_REPO_NAME
        except ImportError:
            logger.error("❌ Не найдены настройки GitHub в config.py")
            logger.error("   Добавьте в config.py:")
            logger.error("   GITHUB_TOKEN = os.getenv('GITHUB_TOKEN', '')")
            logger.error("   GITHUB_REPO_OWNER = os.getenv('GITHUB_REPO_OWNER', 'Grush-in')")
            logger.error("   GITHUB_REPO_NAME = os.getenv('GITHUB_REPO_NAME', 'Grush-in.github.io')")
            return
        
        # Проверяем что токен установлен
        if not GITHUB_TOKEN:
            logger.warning("⚠️  GITHUB_TOKEN не установлен в .env")
            logger.warning("    Установите GITHUB_TOKEN для отправки статистики")
            logger.warning("    Создайте токен: https://github.com/settings/tokens")
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
                    logger.error(f"   Создайте новый токен: https://github.com/settings/tokens")
                    return False
                elif response.status_code == 404:
                    logger.error(f"❌ Репозиторий не найден (404 Not Found)")
                    logger.error(f"   Проверьте GITHUB_REPO_OWNER и GITHUB_REPO_NAME в .env")
                    logger.error(f"   Текущие значения: {GITHUB_REPO_OWNER}/{GITHUB_REPO_NAME}")
                    return False
                elif response.status_code == 403:
                    logger.error(f"❌ Нет доступа (403 Forbidden)")
                    logger.error(f"   Убедитесь что токен имеет права 'repo'")
                    logger.error(f"   Создайте новый токен с правами 'repo'")
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
                logger.error(f"❌ Timeout при отправке в GitHub (10 секунд)")
                return False
            except requests.exceptions.RequestException as e:
                logger.error(f"❌ Ошибка отправки в GitHub: {e}")
                return False
            except Exception as e:
                logger.error(f"❌ Неожиданная ошибка: {e}")
                return False
        
        # Запускаем в отдельном потоке
        loop = asyncio.get_event_loop()
        success = await loop.run_in_executor(None, send_request)
        
        if success:
            logger.info(f"   Workflow должен запуститься в течение нескольких секунд")
            logger.info(f"   Проверьте: https://github.com/{GITHUB_REPO_OWNER}/{GITHUB_REPO_NAME}/actions")
    
    except Exception as e:
        logger.error(f"❌ Ошибка при отправке через GitHub Actions: {e}")
        import traceback
        logger.error(traceback.format_exc())

