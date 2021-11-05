import logging

# from telegram import ParseMode, InlineKeyboardButton, InlineKeyboardMarkup,
from telegram.ext import (  # CallbackQueryHandler,; Filters,; MessageHandler,; PicklePersistence,
    CommandHandler,
    Updater,
)
from telegram.utils.helpers import escape_markdown

from scrapper import Scraper

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)


def get_todays(update, context):
    scraper = Scraper()
    posts = scraper.scrap_all()
    for post in posts:
        (org, domen, date, title, descr, link) = (escape_markdown(el, version=2) for el in post)
        message = f"__{domen}__\n{org} - {date}\n*{title}*\n_{descr}_\n[Go to blog post]({link})"
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=message,
            parse_mode="MarkdownV2",
            disable_web_page_preview=True,
        )


def main():
    token = input("Please enter telegram bot token:\n")

    # define updater and dispatcher
    updater = Updater(token=token, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("get_todays", get_todays))

    updater.start_polling()


if __name__ == "__main__":
    main()
