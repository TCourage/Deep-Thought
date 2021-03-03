# Welcome to Deep Thought!
## The modular, self-hosted, open-source Discord bot.
### Introduction

Deep Thought is exactly what the subtitle suggests - it's a modular, self-hosted, python-based open-source Discord bot. This project was made possible with the use of [Discord.py](https://discordpy.readthedocs.io/en/latest/).

### Dependencies

1. [Discord.py](https://discordpy.readthedocs.io/en/latest/)

### Installation and Execution

Getting started with Deep Thought;

1. You must be either the server owner, or an administrator to add the bot to the server.
1. You will need to setup a new [Discord Bot Application](https://discord.com/developers/applications). Your bot will require Admin privileges to operate properly.
1. To ensure the database works correctly, please ensure you enable both Presence Intent and Server Members Intents under the `bot` tab.
1. Once your bot is created, you will want to navigate to the OAuth2 tab and get an invite link, set the Scopes to `bot` and Permissions to `Administrator`, copy the link, paste in a new tab, and add your bot to the server of your choice.
1. Next go back to the Bot tab, and under the Username, click to reveal your token, and keep note of it (but keep it safe and secret!).
1. Now you can clone this git repository. On first launch you will be prompted to enter the token you obtained in the previous step, then a command prefix. The prefix is whatever you want to use to "signal" the bot to listen to your command (i.e. if you want to run Deep Thought commands like `?kick` or `#ban` you would enter `?` or `#` at this step). Default is `!`.
1. With the token in place, you can now run `python3 bot.py` in the root of the directory. The bot will load any extensions, and log in. To verify the bot is working simply run `prefix+help` in your server and you should receive a response.

#### Note for macOS Users

Something in the way Python interacts with macOS prevents SSL certificates from being used without first importing them. In order for the bot to log in, we must first install the required SSL certs to the Python library paths. Fortunately, this is very simple. If you installed Python from the website using a .pkg, navigate to `/Applications/Python 3.x` and run `Install Certificates.command`. If you installed Python using Brew or Ports, run `pip install --upgrade certificates`. Once this is finished the bot will run and successfully login.

### Adding Extensions

If you would like to add your own extensions to Deep Thought, please follow the guide below. It is a relatively simple process.

1. Create a new file at the root of the Deep Though directory call `extra-extensions.txt`.
1. Create a new folder in the root of the Deep Thought directory, and add your extension(s) to that folder. Ensure your extensions use a .py file format.
1. Open your newly-created `extra-extensions.txt` file and add your extension to the list, using the following format: `foldername.filename` - do not include the .py file extension.
1. You can take a look at the `main-extensions.txt` file for an example, but **please do not edit this file**.