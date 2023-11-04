# Python Weather Alert Script

This Python script is designed to retrieve weather data, send a weather alert email, and store the weather data in a JSON file. Below is a breakdown of the script:

## Prerequisites

Before running the script, ensure you have the required Python packages installed:

```bash
pip install requests
pip install python-dotenv
pip install smtplib
```

## Usage
1. Set up your email credentials and OpenWeatherMap API key in the rain_app_creds.py file.

2. Execute the script. It will fetch weather data for the next 12 hours, check for rain, and send an email alert if rain is expected.

## Configuration

Create a file with your CREDENTIALS rain_app_creds.py file, configure the following variables:

    PASSWORD: Your email account password.
    FROM_ADDRESS: Your email address.
    TO_ADDRESS: The recipient's email address.

## Logging

The script logs its status and errors to a script_logs.log file.

## API Variables

The following API variables can be customized according to your requirements:

    API_KEY: Your OpenWeatherMap API key.
    OPEN_WEATHER_ENDPOINT: The API endpoint for weather data.
    CURRENT_WEATHER_PARAMS: Parameters for the API request.

## Output Files

    weather.json: Stores weather data for the next 12 hours in JSON format.

## Email Message

<b>The email message is sent in HTML format and includes information about the script's status and the weather forecast.

Note: This script uses Gmail as the email service provider (GMAIL_SERVER). Ensure you allow less secure apps in your Gmail settings if you plan to use it.

Powered by www.pythonanywhere.com!
</b>
