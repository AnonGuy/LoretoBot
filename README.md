# LoretoBot
LoretoBot is a Discord Bot that allows you to: </br>

* Access the Loreto intranet
* View your timetable
* Notify yourself of lessons
* Upload files to your network </br>

With many more features to come!

# Requisites:
All of these requisites can be installed via the python package manager, `pip`. </br>
* LoretoBot requires the [Discord.py API](https://discordpy.readthedocs.io/en/rewrite/) to login. </br>
```
python3 -m pip install -U discord.py # for Linux
py -3 -m pip install -U discord.py   # for Windows
```
* For sending HTTP requests, I used the Requests module, and to parse the HTML, I used BeautifulSoup4:
```
... pip install requests
... pip install bs4
```
* To print out the timetables in a nice format, I used the PrettyTable module:
```
... pip install prettytable
```
* And, as a deprecated feature, I've added the [Twilio API](https://www.twilio.com/docs/libraries/python):
```
... pip install twilio
```
I say deprecated, as I've worked out a method to allow unlimited SMS messages without a trial, using my own mobile SMS contract. It uses an [IFTTT (If This, Then That)](https://ifttt.com/discover) recipe to send an SMS when a POST request is sent to my webhook URL.
# Installation:
LoretoBot is still in development! </br>
Watch out for `<VALUES IN ANGLE BRACKETS>`. These are tokens, emails and other sensitive data. make sure that you have signed up / set up the associated service, and change the values before starting the Bot. </br>
I am currently running it on a Raspberry Pi, explaining the `pytronics.py` file. However, the Bot should still work on any system with the requisites installed. Run `main.py` to start the Bot.
