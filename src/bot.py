import logging
import os

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CommandHandler, Filters, MessageHandler, Updater

from scrapper import Scraper

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

# define directory for chat history
history_dir = "../bot_history"
os.makedirs(history_dir, exist_ok=True)

replies = {
    "info": """Hello, Sir\! My name is Jarvis\!
I\'ll keep you up to date with AI research\.
I\'ll send you new blog posts from Google AI, Facebook AI and OpenAI once added\.
Below You may find basic commands I understand currently\.
Commands:
/info \- show this info message
/start \- start sending me new blog posts
/stop \- stop sending me new blog posts""",
    "start": """Ok, Sir\. Starting sending You new blog posts\!
In case you want me to stop \- give me /stop \ command""",
    "stop": """Ok, Sir, I\'ve stopped sending you new blog posts\! 
In case you change your mind just give me /start \ command\.""",
    "not_started": """Oh, there is nothing to stop\! 
Make sure to give command /start \ before calling /stop \\. Check /info \ for more details\.""",
    "unknown": """Sorry, Sir, `message` is unknown command\. 
Please check available commands by writing /info \ to me\.""",
}


def info(update, context):
    text = replies["info"]
    context.bot.send_message(chat_id=update.effective_chat.id, text=text, parse_mode="MarkdownV2")


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
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=replies["start"],
        parse_mode="MarkdownV2",
    )
    context.job_queue.run_repeating(
        get_new_posts, interval=1800, first=10, context=update.message.chat_id
    )


def stop(update, context):
    jobs = context.job_queue.jobs()
    if len(jobs) > 0:
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=replies["stop"],
            parse_mode="MarkdownV2",
        )
        jobs[-1].schedule_removal()
    else:
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=replies["not_started"],
            parse_mode="MarkdownV2",
        )


def unknown(update, context):
    text = replies["unknown"].replace("message", update.message.text)
    context.bot.send_message(chat_id=update.effective_chat.id, text=text, parse_mode="MarkdownV2")


def main():
    if os.environ.get("TOKEN"):
        TOKEN = os.environ.get("TOKEN")
    else:
        TOKEN = input("Please enter telegram bot token:\n")
        os.environ["TOKEN"] = TOKEN

    # define updater and dispatcher
    updater = Updater(token=TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # register commands
    dispatcher.add_handler(CommandHandler("start", schedule_requests, pass_job_queue=True))
    dispatcher.add_handler(CommandHandler("info", info))
    dispatcher.add_handler(CommandHandler("stop", stop))
    dispatcher.add_handler(MessageHandler(Filters.text & (~Filters.command), unknown))

    # start bot
    if os.environ.get("SERVER_LINK"):
        PORT = int(os.environ.get("PORT", 5000))
        SERVER_LINK = os.environ.get("SERVER_LINK")
        updater.start_webhook(listen="0.0.0.0", port=PORT, url_path=TOKEN)
        updater.bot.setWebhook(SERVER_LINK + TOKEN)
    else:
        updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
