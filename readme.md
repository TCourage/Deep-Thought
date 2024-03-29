# Welcome to Deep Thought!
## The modular, self-hosted, open-source Discord bot.
### Introduction

Deep Thought is exactly what the subtitle suggests - it's a modular, self-hosted, python-based open-source Discord bot. This project was made possible with the use of [Discord.py](https://discordpy.readthedocs.io/en/latest/).

### Dependencies

#### Main bot and extensions (mandatory)

1. [Discord.py](https://discordpy.readthedocs.io/en/latest/)

#### Extra extensions (optional, remove modules from `extras/` folder)

1. dt-extra_minecraft - [MCStatus](https://github.com/Dinnerbone/mcstatus)

### Installation and Execution

Getting started with Deep Thought;

1. You must be either the server owner, or a server administrator, to add the bot to the server.
1. Ensure the above dependencies are met, then clone this repo.
1. You will need to setup a new [Discord Bot Application](https://discord.com/developers/applications).
1. Go to the `Bot` tab and select `Add New`. Enter a username (and image if desired), and enable both Presence Intent and Server Members Intent. Under `Bot Permissions` ensure `Administrator` is selected.
1. Click to reveal your token, and copy it. It is recommended you save this token in a secure location.
1. Run the program using `python3 bot.py`. When prompted paste your token and press Return, then enter your preferred prefix (default is `!`). The bot should now load extensions and log in.
1. Go to the `OAuth2` tab, under `Scopes` select `bot` and under `Bot Permissions` select `Administrator`. Copy the link and paste it in a new tab to invite the bot to your server.
1. To verify the bot is working simply run `!help` in your server and it should return a list of loaded modules.
1. To finish setup, run `!setup` on your server. This will create and populate the databases. **FAILURE TO PERFORM THIS STEP MAY CAUSE THE BOT TO FAIL!**
1. Note the token and prefix are not required to be entered when the bot is restarted. To reset either of these values, delete `server.db`, and you will be asked to provide those details on next launch.

#### Note for macOS Users

Something in the way Python interacts with macOS prevents SSL certificates from being used without first importing them. In order for the bot to log in, we must first install the required SSL certs to the Python library paths. Fortunately, this is very simple. If you installed Python from the website using a .pkg, navigate to `/Applications/Python 3.x` and run `Install Certificates.command`. If you installed Python using Brew or Ports, run `pip install --upgrade certificates`. Once this is finished the bot will run and successfully login.

### Adding Extensions

If you would like to add your own extensions to Deep Thought, simply add them to the `extras/` folder. When Deep Thought launches it will automatically attempt to load any Python files. Any errors will be output to the console, and that extension will not be loaded.