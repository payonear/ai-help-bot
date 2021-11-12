import logging
import os

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CommandHandler, PicklePersistence, Updater

from scrapper import Scraper

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

# define directory for message history
history_dir = "../bot_history"
os.makedirs(history_dir, exist_ok=True)


def get_new_posts(context):
    scraper = Scraper()
    posts = scraper.scrape_all()

    for post in posts:
        message, link = post

        with open(os.path.join(history_dir, "received.txt"), "a+") as file:
            file.seek(0)
            history = file.read().split()

        if link in history:
            continue
        else:
            history.append(link)
            context.bot.send_message(
                chat_id=context.job.context,
                text=message,
                parse_mode="MarkdownV2",
                reply_markup=InlineKeyboardMarkup(
                    [[InlineKeyboardButton(text="Go to post", url=link)]]
                ),
            )

            with open(os.path.join(history_dir, "received.txt"), "w") as file:
                file.writelines(" ".join(history[-100:]))


def schedule_requests(update, context):
    context.job_queue.run_repeating(
        get_new_posts, interval=90, first=10, context=update.message.chat_id
    )


def get_history(update, context):
    history = context.user_data
    context.bot.send_message(chat_id=update.effective_chat.id, text=f"Chat history:\n{history}")


def main():
    if os.environ.get("TOKEN"):
        token = os.environ.get("TOKEN")
    else:
        token = input("Please enter telegram bot token:\n")
        os.environ["TOKEN"] = token

    # define updater and dispatcher
    updater = Updater(token=token, use_context=True)
    dispatcher = updater.dispatcher

    # register commands
    dispatcher.add_handler(CommandHandler("start", schedule_requests, pass_job_queue=True))
    dispatcher.add_handler(CommandHandler("history", get_history))

    # start bot
    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
