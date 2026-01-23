import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def get_weather(city):
    # Get API key from environment variable
    api_key = os.getenv("WEATHER_API_KEY")
    
    if not api_key:
        return "Error: API key not found in .env file"
    
    url = "http://api.weatherapi.com/v1/current.json"
    
    params = {
        "q": city,
        "key": api_key
    }
    
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        temp = data['current']['temp_f']
        condition = data['current']['condition']['text']
        return f"Weather in {city}: {temp}°F, {condition}"
    else:
        return f"Error: {response.status_code}"

if __name__ == "__main__":
    # Test with different cities
    print(get_weather("Tokyo"))
    print(get_weather("London"))
    print(get_weather("New York"))

#hello = (input("hi how are you doing:"))
#def check(f):
 #   if f == "good":
  #     return "wow thats nice"
   # else:
    #   return "it will be better"
#moral = check(hello)
#print(moral)
#print("\n")
#print("feilling test")
