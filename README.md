# DaniAi Telegram Bot

Телеграм‑бот на базе [Aiogram](https://github.com/aiogram/aiogram) для сбора заявок.

## Запуск

Используется `poetry` для управления зависимостями и виртуальным окружением.

```bash
poetry install
# Запустить бот можно так:
poetry run python -m bot
# либо явно указать модуль main
poetry run python -m bot.main
```

Не забудьте указать переменные окружения `BOT_TOKEN` и `ADMIN_ID`.
Если `ADMIN_ID` совпадает с ID пользователя, то при команде `/start` он увидит админское меню.

