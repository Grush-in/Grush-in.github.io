// API endpoint для приема статистики от VPN бота
// Сохраняет данные в GitHub репозиторий

import { Octokit } from '@octokit/rest';

const octokit = new Octokit({
  auth: process.env.GITHUB_TOKEN
});

// Конфигурация
const GITHUB_OWNER = 'Grush-in';
const GITHUB_REPO = 'Grush-in.github.io';
const STATS_FILE_PATH = 'stats.json';

export default async function handler(req, res) {
  // CORS headers
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization');

  // Handle preflight
  if (req.method === 'OPTIONS') {
    return res.status(200).end();
  }

  // Only allow POST
  if (req.method !== 'POST') {
    return res.status(405).json({ 
      error: 'Method not allowed',
      message: 'Only POST requests are accepted'
    });
  }

  try {
    // Опциональная авторизация
    if (process.env.STATS_API_KEY) {
      const authHeader = req.headers.authorization;
      const expectedAuth = `Bearer ${process.env.STATS_API_KEY}`;
      
      if (authHeader !== expectedAuth) {
        return res.status(401).json({ 
          error: 'Unauthorized',
          message: 'Invalid API key'
        });
      }
    }

    // Получаем статистику из тела запроса
    const stats = req.body;
    
    // Валидация данных
    if (!stats || typeof stats !== 'object') {
      return res.status(400).json({
        error: 'Bad request',
        message: 'Invalid stats data'
      });
    }

    console.log('📊 Получена статистика:', {
      app: stats.app_name,
      online: stats.online_users,
      total: stats.total_users,
      keys: stats.active_keys,
      revenue: stats.revenue_today
    });

    // Получаем текущий SHA файла (нужен для обновления)
    let sha;
    try {
      const { data } = await octokit.repos.getContent({
        owner: GITHUB_OWNER,
        repo: GITHUB_REPO,
        path: STATS_FILE_PATH,
      });
      sha = data.sha;
      console.log('📄 Файл существует, обновляем...');
    } catch (error) {
      if (error.status === 404) {
        console.log('📄 Файл не существует, создаем новый...');
        sha = null;
      } else {
        throw error;
      }
    }

    // Подготавливаем контент
    const content = Buffer.from(JSON.stringify(stats, null, 2)).toString('base64');
    
    // Создаем или обновляем файл
    const result = await octokit.repos.createOrUpdateFileContents({
      owner: GITHUB_OWNER,
      repo: GITHUB_REPO,
      path: STATS_FILE_PATH,
      message: `📊 Update VPN stats: ${new Date().toISOString()}`,
      content,
      sha, // undefined для нового файла
    });

    console.log('✅ Статистика успешно сохранена в GitHub');
    console.log('   Commit:', result.data.commit.sha.substring(0, 7));
    
    return res.status(200).json({ 
      success: true,
      message: 'Stats updated successfully',
      commit: result.data.commit.sha.substring(0, 7),
      timestamp: new Date().toISOString()
    });
    
  } catch (error) {
    console.error('❌ Ошибка при обработке запроса:', error);
    
    return res.status(500).json({ 
      error: 'Internal server error',
      message: error.message,
      timestamp: new Date().toISOString()
    });
  }
}


