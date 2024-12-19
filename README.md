В файле *config.json* вставить свой API, пути к файлам.

## Как установить?

```bash
python -m venv /path/to/new/virtual/environment
```

```bash
source path/bin/activate
```

```bash
 cd path/ 
```
```bash
git clone https://github.com/Hecker76RUS/mapantenky-bot.git
```
Либо скачать данный релиз и распаковать его в venv

```bash
cd mapantenky-bot
pip install -r requirements.txt

mv -r TelegramAPI /home/user/path/to/venv
mv activate_ bot.py /home/user/path/to/venv
cd ..
rm -rf mapantenky-bot
```

## Запуск

python activate_bot.py