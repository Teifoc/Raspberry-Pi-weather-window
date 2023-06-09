import RPi.GPIO as GPIO
import time
import requests
import json
import Adafruit_DHT
from functools import lru_cache

# Set up the DHT11 temperature and humidity sensor
sensor = Adafruit_DHT.DHT11
pin = 4

# Set up the servo motor
GPIO.setwarnings(False)
GPIO.cleanup()
servo_pin = 18
GPIO.setmode(GPIO.BCM)
GPIO.setup(servo_pin, GPIO.OUT)
pwm = GPIO.PWM(servo_pin, 50)
pwm.start(0)

# Define the temperature and humidity thresholds
temp_threshold = 12.0
humidity_threshold = 60.0

# Define the weather API key and location
weather_api_key = 'f9307df32efb3d34a029ad4cbf9ebdd2'
weather_lat = '62.79446'
weather_lon = '22.82822'

# Define the API endpoint for the current weather data
weather_url = f'https://api.openweathermap.org/data/2.5/weather?lat={weather_lat}&lon={weather_lon}&appid={weather_api_key}'

# Define the servo angle values for different window positions
closed_angle = 5#0
tilt_angle = 10 #45
open_angle = 45 #90


def get_ttl_hash(seconds=3600):
    """Return the same value withing `seconds` time period"""
    return round(time.time() / seconds)

# Function to get the current weather data from the API
@lru_cache()
def get_weather_data(ttl_hash=None):
    response = requests.get(weather_url)
    print("get_weather_data() executed")
    data = json.loads(response.text)
    print("Weather conditions: " + data['weather'][0]['main'] + "")
    return data

def get_temperature():
    # Read the temperature and humidity values from the sensor
    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)

    if temperature is not None:
        print("Temperature: " + str(temperature) + " C")
        return temperature
    else:
        print("Error reading DHT11 data.")

def get_humidity():
    # Read the temperature and humidity values from the sensor
    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)

    if humidity is not None:
        print("Humidity: " + str(humidity) + " %")
        return humidity      
    else:
        print("Error reading DHT11 data.")


# Function to determine the window position based on the current weather data
def get_window_position(weather_data, temperature, humidity):
    weather_conditions = weather_data['weather'][0]['main']
    if weather_conditions == 'Rain' or weather_conditions == 'Snow':
        return tilt_angle
    elif weather_conditions == 'Thunderstorm':
        return closed_angle
    elif temperature > temp_threshold or humidity > humidity_threshold:
        return open_angle
    else:
        return closed_angle

# Set the initial window position to closed
current_position = closed_angle

# Main loop
while True:
    temperature = get_temperature()
    humidity = get_humidity()
    weather_data = get_weather_data(ttl_hash=get_ttl_hash())
    # Check if the temperature or humidity exceeds the thresholds or if it's raining or snowing
    if temperature > temp_threshold or humidity > humidity_threshold or weather_data['weather'][0]['main'] == 'Rain' or weather_data['weather'][0]['main'] == 'Snow':
        window_position = get_window_position(weather_data, temperature, humidity)
        # Check if the desired position is different from the current position
        print("current position: " +str(current_position) +", window position: " +str(window_position))
        if window_position != current_position:
            # Set the servo to the desired position
            GPIO.output(servo_pin, True)
            duty_cycle = 2 + (window_position / 18)
            pwm.ChangeDutyCycle(duty_cycle)
            print("Window position: " + str(window_position) + " degrees")
            time.sleep(1)
            GPIO.output(servo_pin, False)
            pwm.ChangeDutyCycle(0)
            # Update the current position
            current_position = window_position
    else:
        # Check if the desired position is different from the current position
        if current_position != closed_angle:
            # Adjust the servo to the closed position
            GPIO.output(servo_pin, True)
            pwm.ChangeDutyCycle(2 + (closed_angle / 18))
            time.sleep(1)
            GPIO.output(servo_pin, False)
            pwm.ChangeDutyCycle(0)
            time.sleep(1)
            print("Window closed")
            # Update the current position
            current_position = closed_angle
    # Wait for some time before checking the conditions again
    time.sleep(5)
