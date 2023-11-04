import datetime
import requests
import json
import logging
from smtplib import *
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from rain_app_creds import PASSWORD, FROM_ADDRESS, TO_ADDRESS, API_KEY


# --------------------------- LOGGING CONFIGURATION -----------------------------------
# Create and configure logger
logging.basicConfig(filename='script_logs.log',
                    format='%(asctime)s %(message)s',
                    filemode='a')

# Creating an object
logger = logging.getLogger()

# Setting the threshold of logger to DEBUG
logger.setLevel(logging.DEBUG)


# --------------------------- SNMP VARIABLES -----------------------------------

GMAIL_SERVER = "smtp.gmail.com"
FROM_ADDRESS = FROM_ADDRESS
TO_ADDRESS = TO_ADDRESS
PASSWORD = PASSWORD
SUBJECT = "This is a Python E-Message."
CURRENT_TIME = datetime.datetime.now()

# --------------------------- API VARIABLES -----------------------------------
API_KEY = API_KEY
OPEN_WEATHER_ENDPOINT = 'https://api.openweathermap.org/data/3.0/onecall'

CURRENT_WEATHER_PARAMS = {
    "lat": 32.84,
    "lon": -97.225,
    "appid": API_KEY,
    "exclude": 'current,minutely,daily'
}

# --------------------------- API CALL -----------------------------------
# GET REQUEST FOR WEATHER
try:
    current_weather = requests.get(OPEN_WEATHER_ENDPOINT, params=CURRENT_WEATHER_PARAMS)
    http_status = current_weather.status_code
    weather_dict = current_weather.json()
except:
    logger.info(f'{http_status}: Error in Script. Please Verify.')
    exit()
# --------------------------- PRE STRUCTURE -----------------------------------
# This is Purely to Print a JSON File for outputs.
weather_info_12_hours_list = []
rain_today = False

# --------------------------- FETCH GET DATA STRUCTURE -----------------------------------

# Check if the 'hourly' data exists in the 'weather_dict'
if 'hourly' in weather_dict:
    # Get data for the next 12 hours or less if it's not available
    weather_slice = weather_dict['hourly'][:12]

    # Loop through each dictionary in the 'weather_slice'
    for each_dict in weather_slice:
        # Check for the 'weather' key in the dictionary
        if 'weather' in each_dict:
            # Extend the 'weather_info_12_hours_list' with the weather information
            weather_info_12_hours_list.extend(each_dict['weather'])

            # Check if the 'id' in each weather element is less than 700 (indicating rain)
            for elem in each_dict['weather']:
                if 'id' in elem and elem['id'] < 700:
                    rain_today = True

    logger.info('Script Ran Successfully.')
else:
    logger.warning('No hourly data found in weather_dict.')

# --------------------------- FINAL WEATHER CHECK -----------------------------------
weather_alert_message = ''
if rain_today:
    print(f'Code: {http_status}: Rain Expected Today. \N{Cloud with Rain}')
    weather_alert_message = 'Rain Expected Today. \N{Cloud with Rain}'
else:
    print(f'Code: {http_status}: No Umbrella Needed Today. \N{sun with face}')
    weather_alert_message = f'No Umbrella Needed Today. \N{sun with face}'


# --------------------------- SNMP STRUCTURE -----------------------------------

# EMAIL MESSAGE STRUCTURE IN HTML
MESSAGE = f"""
<h2>Weather Today:</h2>
<h3>{weather_alert_message}</h3>
<br>


<h4>Powered by www.pythonanywhere.com!</h4>
<b>Code Status {http_status}: Ran on {CURRENT_TIME} </b>
"""

# Send Email with Rain Status for the Day
with SMTP(GMAIL_SERVER, port=587) as connection:
    connection.starttls()
    connection.login(FROM_ADDRESS, PASSWORD)

    msg = MIMEMultipart()

    msg['From'] = FROM_ADDRESS
    msg['To'] = TO_ADDRESS
    msg['Subject'] = SUBJECT

    # add in the message body
    msg.attach(MIMEText(MESSAGE, 'html'))
    connection.send_message(msg)

    print(msg)
    connection.quit()

# --------------------------- OUTPUT FILE -----------------------------------
# Output Data into a JSON File
with open('weather.json', 'w') as output:
    output.write(json.dumps(weather_info_12_hours_list, indent=4))
