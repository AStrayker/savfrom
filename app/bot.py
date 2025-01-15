import asyncio
from telegram import Update, Bot
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from tiktok.api import TikTokAPI
from settings import settings  # Предположим, что settings.py остаётся без изменений

async def handle_tiktok_request(update: Update, context: CallbackContext) -> None:
    message = update.message
    entries = [
        message.text[e.offset : e.offset + e.length]
        for e in message.entities or []
        if message.text is not None
    ]

    urls = [
        u if u.startswith("http") else f"https://{u}"
        for u in filter(lambda e: "tiktok.com" in e, entries)
    ]

    async for tiktok in TikTokAPI.download_tiktoks(urls):
        if not tiktok.video:
            continue

        video = tiktok.video
        caption = tiktok.caption if settings.with_captions else None

        if settings.reply_to_message:
            await context.bot.send_video(chat_id=message.chat_id, video=video, caption=caption, reply_to_message_id=message.message_id)
        else:
            await context.bot.send_video(chat_id=message.chat_id, video=video, caption=caption)

async def welcome(update: Update, context: CallbackContext) -> None:
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Добро пожаловать! Я бот для скачивания TikTok видео. Отправьте мне ссылку на видео TikTok.")

def main():
    updater = Updater(settings.api_token, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", welcome))
    
    # Фильтры для сообщений с URL
    filters = Filters.text & (Filters.entity("url") | Filters.entity("text_link"))
    if settings.allowed_ids:
        filters &= Filters.chat(chat_id=settings.allowed_ids)
    dp.add_handler(MessageHandler(filters, handle_tiktok_request))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    asyncio.run(main())
