import smtplib
# Needed for the email client and functions
import requests
# Needed for sending POST, GET and HEAD requests
# Essential for webhooks as well as APIs
from twilio.rest import Client as SMSClient
# The twilio SMS API. Only really here since I made an account
# I've replaced it with my own function, send_ifttt

twilio_sid = '<TWILIO SID>'
twilio_tok = '<TWILIO SID>'
# Set the twilio SID and Token
twilio_client = SMSClient(twilio_sid, twilio_tok)
# Start an SMS Client
def send_twilio(number, notification):
    '''Send a Twilio SMS message. Deprecated since it also sends a trial bait message'''
    # "sent from a twilio trial account"
    if number[0] == '0':
        # If the number does not have a country code
        number = '+44'+number[1:]
        # Add the +44 country code
    message = twilio_client.messages.create(
            to = number,
            from_ = '<TWILIO NUMBER>',
            body = notification)
    # Send a message from my custom number, with the body entered into the function

email = smtplib.SMTP('smtp.gmail.com', 587)
# Set the port and gmail SMTP url
email.ehlo()
# Send a message to the gmail server to initiate an SMTP conversation
email.starttls()
# Initialise the SMTP service for sending messages
me = '<EMAIL ADDRESS>'
email.login(me,'<EMAIL PASSWORD>')
# Login to the bot's Gmail account
def send_email(address, body):
    '''Send an email using the SMTP configuration above'''
    body = 'Subject: LoretoBot Notification\n'+body
    email.sendmail(me, address, body)
    # Send an email with the arguments in the function. ez

def send_ifttt(number, message):
    '''Use the IFTTT (If This, Then That) service to route SMS traffic through my mobile phone'''
    report = {'value1': number, 'value2': message}
    # The payload to send with the post request. Value1 and Value2, the number and message,
    # Are posted to my maker webhook channel. This then triggers an IFTTT recipe on my mobile
    # That sends a message to {{Value1}} with a body of {{Value2}}.
    requests.post('<IFTTT MAKER WEBHOOK CHANNEL LINK>', data=report)
    # Send the post request, triggering the SMS recipe on my mobile

