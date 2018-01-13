import discord
from discord.ext import commands
# Discord modules needed for the API
import requests
from bs4 import BeautifulSoup
# My favourite modules for http requests and parsing html
import sqlite3
# Needed for connecting to my user database
from prettytable import PrettyTable
# For pretty output of the user's timetable, mainly
import custom_out
# My own module for sending various forms of external communication
# e.g. SMS, email and more coming soon!
import sys
sys.path.append('/home/pi/LoretoBot')
# For importing modules from another directory:
import pitronics
# Sometimes I may connect an LCD to test the electronic capabilities of the RPi.
# This module contains various functions for my electronic components

auth_path = '<PATH TO AUTH.DB>'
# The database cotaining user's authentication
auth_db   = sqlite3.connect(auth_path)
cursor    = auth_db.cursor()
# Initialise the database, and set the cursor for executing commands

class User:
    '''My cool intranet user class'''
    def __init__(self, username, password, number, soup):
        '''Initialise variables of the User class'''
        self.username  = username 
        self.password  = password
        # The user's username and password, for assorted signins
        self.number = number # An optional variable for the user's phone number (for sms)
        self.soup   = soup   # A BeautifulSoup containing the html of my.loreto.ac.uk

    def timetable(self):
        '''Return a markdown-formatted string of the user's timetable'''
        table = PrettyTable()
        # Initialise a PrettyTable, for pretty printing of the timetable
        table.field_names = ['Period','Room','Lesson']
        time_tags = self.soup.findAll('div',{'class':'todayTimetableEntry'})
        # Get the tags for timetable entries using the BeautifulSoup class
        contents  = [tag.text.strip() for tag  in time_tags]
        contents  = [entry.split('\n') for entry in contents]
        contents  = [[x for x in y if x] for y in contents]
        # A couple lines of list comprehension to format the contents list correctly
        # I'm not proud of it, but it does the job!
        for i,item in enumerate(contents):
            # Go through 'contents', obtaining indexes simultaneously
            item[-1] = item[-1].split(' - ')
            item[-1] = item[-1][0]
            # Remove the teacher's name, since it's not really needed anyway
            contents[i] = item
            # Finally use the index to set the correct item in the list
        if contents:
            # If there was anything there in the first place:
            for row in contents:
                # Add each row in contents
                table.add_row(row)
            table = table.get_string()
            # Get the pretty-formatted string, since there's more to do!
            return '```'+table+'```'
            # Finally return the string in a mardown codeblock, preserving monospacing
        return "```You don't have any lessons today!```"
        # 'return' ends a function, so there's no need for an 'else' statement

    def notify(self, body):
        '''Use my customised sms client to send a formatted sms to the user'''
        lines = body.split('\n')
        # Split by carriage returns
        lens  = [len(line) for line in lines] + [31]
        lines = [line.center(max(lens)) for line in lines]
        # Centres the lines based on the max line size
        titles = ['--= LoretoBot Notification: =--',
                  '-------------------------------'] 
        # Array for formatting the message
        body = '{0}\n{1}\n{2}'.format(titles[0], '\n'.join(lines), titles[1])
        # Centre the lines almost perfectly
        if self.number:
            # If the number exists:
            custom_out.send_ifttt(self.number, body)
            # Use my own ifttt function to send a message routed through my mobile

def load_user(id_):   
    '''Take a Discord ID, and return my User class containing needed variables, and html'''
    try:
        cursor.execute('SELECT username, password, number FROM userauth WHERE id=?', (str(id_),))
        # Get all the user attributes from my .db file that matches the id
        auth   = cursor.fetchone()
        # Get the last result
        result = requests.get('http://my.loreto.ac.uk', auth=auth[:-1])
        # Send a get request to the intranet homepage, with the authentication as (username, password)
        soup   = BeautifulSoup(result.text, 'html.parser')
        # Make a BeautifulSoup from the homepage source to make parsing html easier
        return User(*auth, soup)
        # Return my own User class, with the attributes I got in the function
    except:
        # If the loading failed, return False
        return False

class Intranet:
    '''A custom cog to access the college intranet'''
    def __init__(self, bot):
        # Initialise the Cog class
        self.bot = bot

    @commands.command()
    # Decorator for commands.command: These functions are run when the user enters a command
    # (See ../main.py for more)
    async def timetable(self, ctx):
        # Add an asynchronous function to run when the command is used
        user = load_user(ctx.author.id)
        # Try to load a user using the id of the user
        if user:
            await ctx.send(user.timetable())
            # If the user exists (no errors were produced in load, see above)
        else:
            await ctx.send('You aren\'t signed in to LoretoBot services!')
            # If False was returned by the load_user function

def setup(bot):
    # Add the cog to the bot
    bot.add_cog(Intranet(bot))
