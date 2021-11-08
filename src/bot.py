import logging

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (  # CallbackQueryHandler,; Filters,; MessageHandler,; PicklePersistence,
    CommandHandler,
    Updater,
)

from scrapper import Scraper

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)


def get_todays(update, context):
    scraper = Scraper()
    posts = scraper.scrape_all()
    for post in posts:
        message, link = post
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=message,
            parse_mode="MarkdownV2",
            # disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton(text="Go to post", url=link)]]
            ),
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
