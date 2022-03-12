# How to create and host your own Discord music bot for free
## Overview
This is a Python-based Heroku-ready Discord bot that can search and play videos from YouTube. Only the bare minimum is included here, but with a few simple changes you can easily run it locally or host it for free on [Heroku](https://www.heroku.com/platform). It's intended for personal use in a private server "for friends", although you can do whatever you want with it. It's also easily customizable if you know even a little Python. The almost ready-to-use code fixes *most* common issues encountered when trying to play music videos from YouTube.

Below are explained most of the steps required to make your own bot using this code and host it 24/7 for free.
## Downloading this repository
To get all files, simply click the green Code button near the top of the page and select the Download ZIP option. Extract the folder and rename it if you want. This is where you'll be working on the bot. Note: you don't need the LICENSE and README files.
## Creating a bot
If you haven't created a bot account, go to the [Discord Developer Hub](https://discord.com/developers/applications) and click on New Application. After naming it, go to the Bot entry in the menu and select Add Bot. This is where you can change its username, control its permissions and intents, and get your **token**. This token is used to control your bot, so don't show it to anyone.
## Setting up git
You need to [download](https://git-scm.com/downloads) and install git, a system for managing your work.

Go to your working directory (where all the bot files are) via the command line. On windows, this can be done more easily: go into the folder, type `cmd` into the navigation bar (located at the top of the window, left of the search bar) and hit enter.
Enter the `git init` command. If everything works, a new empty repository should be initialized.
To add files to the repository, use `git add <filename>` or simply `git add .` to add all files from the current directory. You'll need to add every file the bot needs.
If you've made any changes to these files, you'll need to commit them, i.e. change the files in git too. Use the command `git commit -m "message"` to do so. The message helps you track what you've commited.
## Setting up Heroku
If you want your bot to run on the cloud 24/7 for free, I'd recommend using [Heroku](https://www.heroku.com/platform).

Create a new account. Heroku offers **500 hours** (about 3 weeks) each month of free hosting. **You can increase that by another 500 hours** by providing your credit card information (you will not be charged).

When you have an account, go to the [apps tab](https://dashboard.heroku.com/apps) and create a new app. Choose its name and the region where it's going to be physically hosted. Go to settings and click on "Add buildpack", then select python and save. Then add the following two links the same way:
```
https://github.com/jonathanong/heroku-buildpack-ffmpeg-latest.git
https://github.com/xrisk/heroku-opus.git
```
Both of these have to do with getting the YouTube video and converting the sound, then passing it to the bot so it can play it.
## Connecting Heroku to your bot
Go to your working directory (where all the bot files are) via the command line. On windows, this can be done more easily: go into the folder, type `cmd` into the navigation bar (located at the top of the window, left of the search bar) and hit enter.
Execute the `heroku login` command and follow the steps.
Once you've logged in, type `heroku git:remote -a <app name>` and replace <app name> with the name of your Heroku app. 
## Getting your bot ready
Go to the Bot page of your [Developer application](https://discord.com/developers/applications). Click on Reset Token to generate a new token and then copy the string. It should look something like this: OTUyMTkzODU0NjAwMjU3NTM2.YiydoQ.jaEZkCI24j13dmdV_7cpyXS9m58

Put your token in the token.txt file and make sure it's the only string there. Save the file and close it.
  
**You'll need to provide youtube.com cookies to listen to certain songs**, mainly if the videos are only accessible with a verified account. This can be done in a variety of ways, most commonly via browser extensions. Download them (they're just a .txt file) and replace the old youtube.com_cookies.txt file from your working directory. Make sure the new one has the exact same name.
  
#### At this point you should be able to host the bot locally by running bot.py, provided you have all the required libraries installed.
### Optional: install the required libraries locally
You'll need to do so if you want to change the bot and test it locally.
The easiest way to install libraries is via pip. If you don't have pip, download and install it. If you're not sure if you have pip, enter "cmd" in the search bar on Windows to open the command interface. Once there, simply execute `pip` and hit enter. If you see a bunch of commands, you already have pip.

All of the libraries you need are listed in requirements.txt, because Heroku needs to install them too (that's done automatically). For example, the first library is called "discord.py". Enter the command `pip install discord.py` in the command interface. Repeat for each row in requirements.txt and change the version of the library (the numbers after the == signs) if you need a newer one.
## Uploading and hosting your bot on Heroku
After you've set up git and Heroku and connected them, as well as commited everything, you're ready to go.
Go to your working directory (where all the bot files are) via the command line. On windows, this can be done more easily: go into the folder, type `cmd` into the navigation bar (located at the top of the window, left of the search bar) and hit enter.
Execute `git push heroku master`. Some stuff should be loading so just wait for it to finish.
  
You can see the logs from your Heroku app page by clicking the "More" button and selecting "View logs". You should get a "Build succeeded" message if everything went well.
You can start/stop the worker which runs your bot from the Resources tab in your Heroku app page.
