# Room Temp Bot

This discord bot uses a Raspberry Pi running Raspbian Buster and a temperature and humidity sensor, like [this one](https://www.amazon.co.uk/gp/product/B078SVZB1X/ref=ppx_yo_dt_b_search_asin_title?ie=UTF8&psc=1), to send a discord message with the room temperature and humidity.

## Usage

To get the bot to output the temperature, send `!temp` in a channel the bot has access to:

![room-temp-bot-output](https://user-images.githubusercontent.com/36062479/77360623-9ba9f800-6d45-11ea-9b15-fb7c0281156b.png)

## Setup/Installation

Go to the discord developer portal applications page [(here)](https://discordapp.com/developers/applications) and create a new app
    
![discord create app](https://user-images.githubusercontent.com/36062479/77360622-99e03480-6d45-11ea-87ac-dd5e784577aa.png)

Generate an oauth2 link for the bot
    
![discord-bot-oauth](https://user-images.githubusercontent.com/36062479/77360608-977dda80-6d45-11ea-989a-1279b68a0b71.png)

Open that link in a new tab and authorise the bot on the server.

On your raspberry pi, run the following commands:

```bash
sudo apt update && sudo apt install git python3 python3-pip -y
cd ~
git clone https://github.com/henrywhitaker3/Room-Temp-Bot.git
mv Room-Temp-Bot/ bot
cd bot
cp .env.example .env
```

Now all the files are downloaded and in the right place. Copy your discord bot's token to your clipboard:

![discord-bot-token](https://user-images.githubusercontent.com/36062479/77360615-98af0780-6d45-11ea-9851-9f8f05dd772e.png)

Now, open up the `.env` file in a text editor (run `nano .env`) and fill in `DISCORD_TOKEN` with the token you just copied and `DISCORD_GUILD` with the name of your discord server.

Run `python3 bot.py` to start the bot.

## Running as a service

In the bot folder is a file called `temp-bot.service` which can be used to start the bot when your pi boots. Run the following commands:

```bash
sudo cp temp-bot.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable temp-bot.service
sudo systemctl start temp-bot.service
```

The bot will now start itself on reboot and is already running in the background.
