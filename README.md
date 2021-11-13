# AI Help Bot
A simple Telegram bot to keep you up-to-date with news from AI industry. Currently bot sends new blog posts scraped from:
* `Facebook AI` blog web-page
* `Google AI` blog web-page
* `OpenAI` blog web-page
  

<!-- Add buttons here -->
[![Licence](https://img.shields.io/github/license/payonear/ai-help-bot?label=license)]()
[![Python Version](https://img.shields.io/badge/python-3-blue)]()
[![python-telegram-bot](https://img.shields.io/badge/python--telegram--bot-v13.7-blue)]()

## Table of contents
- [AI Help Bot](#ai-help-bot)
  - [Table of contents](#table-of-contents)
  - [Demo-Preview](#demo-preview)
  - [Installation](#installation)
        - [Locally](#locally)
        - [Hosting on Heroku](#hosting-on-heroku)
  - [Usage](#usage)

## Demo-Preview
![img](https://github.com/payonear/ai-help-bot/blob/main/img/info_message.jpg)
![img](https://github.com/payonear/ai-help-bot/blob/main/img/example.jpg)

## Installation
There are two ways to host the bot:
* locally
* on `Heroku` cloud

##### Locally
If you want to host the bot on your local machine - all you need is to follow few simple steps:
*  Talk to [@BotFather](https://telegram.me/botfather) and generate an [Access Token](https://core.telegram.org/bots#6-botfather)
*  `git clone` the repo
*  Run `pip install -r requirements.txt`
*  Go to `src` folder and run command `python bot.py`
*  Bot will ask you to provide Access Token. After you do - the bot is running, go to your bot and check it with command `/info`

##### Hosting on Heroku
In case you want to host the Bot on cloud you may consider doing it using Heroku. Follow the steps below:
* Repeat two first steps from the aboves instructions
* Login or [create](https://signup.heroku.com/dc) a Heroku account.
* Install [Heroku CLI](https://devcenter.heroku.com/articles/getting-started-with-python#set-up)
* Run command `heroku login` from your terminal and login in your browser
* To create new webapp on heroku just run `heroku create YOUR_APP_NAME` from the terminal. Replace YOUR_APP_NAME with the name you want. Otherwise heroku assigns a random name. Heroku will assign the link to your webapp, which should have a format like <https://YOUR_APP_NAME.herokuapp.com/>. Below it's referenced as YOUR_APP_LINK.
* Next, in your command line run the following commands as below (remember to replace YOUR_APP_NAME, YOUR_TOKEN and YOUR_APP_NAME with respective values):
```
    heroku git:remote -a YOUR_APP_NAME
    heroku buildpacks:add heroku/chromedriver
    heroku buildpacks:add heroku/google-chrome
    git commit --allow-empty -m "Empty Commit"
    heroku config:set TOKEN="YOUR_TOKEN"
    heroku config: set SERVER_LINK="YOUR_APP_LINK"
```

* Finally, using command `git push heroku main` you can run your bot.
* Wait a couple of minutes till the webapp is deployed abd go to your bot to check it with command `/info`

*NOTE:* By default Heroku is using free pricing model. It means, that the bot will sleep after apx. 30 min of inactivity and probably stop responding after about 24 hours of inactivity. In the first case it means you may need to wait longer till bot's response, in the second case you need to run the app again. Still, in both cases bot will not be able to send you notifications. So, to use the bot you should choose different pricing option.


## Usage
After the bot is installed and responding to you, you may run command `/start` to make bot sending you messages if new blog posts appear. If, in some reason, you want to stop receiving messages, just give command `/stop`. When bot finishes active jobs it will stop sending you notifications (after `/stop` command you may still receive messages if bot had an active scheduled job in the moment when the command was received).