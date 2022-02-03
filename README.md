# discord-memo-api
Send a message to the bot to write a new memo!

## project repository
- [API](https://github.com/CalicoCheese/discord-memo-api) written with Flask
- [UI](https://github.com/CalicoCheese/discord-memo-ui)
- [BOT](https://github.com/CalicoCheese/discord-memo-bot)

## api settings

### database connect
set your environment value like this
```text
SQLALCHEMY_URI = mysql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}
```



## dependency notice

### mysqlclient
check [this](https://github.com/PyMySQL/mysqlclient#install) page.

### gunicorn
'gunicorn' doesn't support **Windows**. use [waitress](https://github.com/Pylons/waitress) or WSL.
