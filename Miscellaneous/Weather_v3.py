# Imported Modules
import os
import requests
from dotenv import load_dotenv
from flask import Flask, request

load_dotenv()

# For this app you will need a .env with your signalwire credentials, SW phone number, and open-weather API key.
projectID = os.getenv('SIGNALWIRE_PROJECT')
authToken = os.getenv('SIGNALWIRE_TOKEN')
spaceURL = os.getenv('SIGNALWIRE_SPACE')
OPENWEATHER_API = os.getenv('OPENWEATHER_API')

# Initialize the Flask object
app = Flask(__name__)


@app.route('/get_weather', methods=['POST'])
def get_weather():
    if request.method == 'POST':
        post_data = request.get_json()
        print(post_data)
        argument = post_data['weather']
        argument = argument.replace(" ", ", ")
        print(argument)
        url = f"https://api.openweathermap.org/data/2.5/weather?q={argument}&appid={OPENWEATHER_API}&units=imperial"
        url_res = requests.get(url).status_code
        if url_res == 200:
            data = requests.get(url).json()
            print(data)
            feels_like = data["main"]["feels_like"]
            temp = data["main"]["temp"]
            rain = data['weather'][0]['description']
            response_json  = f"The current temperature is {int(temp)} degrees fahrenheit and it also feels like {int(feels_like)} degrees fahrenheit. The current conditions are: {rain}"
            return response_json
        else:
            print(url_res)
            response = "Sorry, I was unable to get the weather for that city and state. Please try again."
            return response, url_res

if __name__ == '__main__':
    app.run(debug=True)
