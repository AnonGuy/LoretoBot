import discord
import sys, traceback
from discord.ext import commands
# Functions required for the bot to respond to commands, and produce error tracebacks

def get_prefix(bot, message):
    '''Callable prefixes for my bot'''
    prefixes = ['>', 'py!']
    # These prefixes can be used interchangeably
    return commands.when_mentioned_or(*prefixes)(bot, message)
    # My commands will be run either when the bot is mentioned, or when a prefix is used.

initial_extensions = ['cogs.intranet']
# Load my extensions (located in the ./cogs folder)

bot = commands.Bot(command_prefix=get_prefix, description='LoretoBot: easily manage your college intranet!')
# Create the Bot object, using the command prefix I created above, with a custom description

if __name__ == '__main__':
    # If this is the file being run directly, not imported
    for extension in initial_extensions:
        # Load every extension that I have described
        try:
            bot.load_extension(extension)
        except Exception as e:
            # If an error occured:
            print('Failed to load extension {}.'.format(extension), file=sys.stderr)
            # Output the error using the traceback module
            traceback.print_exc()

@bot.event
# Decorator for a bot event - on_ready is run when the Bot is loaded
async def on_ready():
    print('\n\nLogged in as: {0} - {1}\nVersion: {2}\n'.format(bot.user.name, bot.user.id, discord.__version__))
    # Print a short summary of my Bot, as well as the current API version
    await bot.change_presence(game=discord.Game(name='with loreto.py'))
    # Add a custom 'playing:' game presence to the Bot
    print('LoretoBot is up!')
    # Print a message to notify the user that the Bot is online

bot.run('<BOT TOKEN>', bot=True, reconnect=True)
# Use my Bot token (created when I created a Bot application) to login to the API
