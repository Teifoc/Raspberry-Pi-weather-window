import RPi.GPIO as GPIO
import time
import requests
import json
import dht11

# Set up the DHT11 temperature and humidity sensor
instance = dht11.DHT11(pin=4)

# Set up the servo motor
servo_pin = 18
GPIO.setmode(GPIO.BCM)
GPIO.setup(servo_pin, GPIO.OUT)
pwm = GPIO.PWM(servo_pin, 50)
pwm.start(0)

# Define the temperature and humidity thresholds
temp_threshold = 25.0
humidity_threshold = 60.0

# Define the weather API key and location
weather_api_key = 'YOUR_API_KEY_HERE'
weather_location = 'YOUR_LOCATION_HERE'

# Define the API endpoint for the current weather data
weather_url = f'https://api.openweathermap.org/data/2.5/weather?q={weather_location}&appid={weather_api_key}'

# Define the servo angle values for different window positions
closed_angle = 0
tilt_angle = 45
open_angle = 90

# Function to get the current weather data from the API
def get_weather_data():
    response = requests.get(weather_url)
    data = json.loads(response.text)
    return data

# Function to determine the window position based on the current weather data
def get_window_position(weather_data):
    weather_conditions = weather_data['weather'][0]['main']
    if weather_conditions == 'Rain' or weather_conditions == 'Snow':
        return tilt_angle
    elif weather_conditions == 'Thunderstorm':
        return closed_angle
    else:
        return open_angle

# Main loop
while True:
    # Read the temperature and humidity values from the sensor
    result = instance.read()
    if result.is_valid():
        temperature = result.temperature
        humidity = result.humidity
        # Check if the temperature or humidity exceeds the thresholds
        if temperature > temp_threshold or humidity > humidity_threshold:
            window_position = get_window_position(get_weather_data())
            pwm.ChangeDutyCycle(2 + (window_position / 18))
            time.sleep(1)
        else:
            pwm.ChangeDutyCycle(0)
            time.sleep(1)
    else:
        print("Error: %d" % result.error_code)






# Sourcecode for the servo:
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)

pwm = GPIO.PWM(18, 50)
pwm.start(0)

def set_angle(angle):
    duty_cycle = angle / 18 + 2
    GPIO.output(18, True)
    pwm.ChangeDutyCycle(duty_cycle)
    time.sleep(1)
    GPIO.output(18, False)
    pwm.ChangeDutyCycle(0)

# set the servo motor to 0 degrees
set_angle(0)

# wait for 1 second
time.sleep(1)

# set the servo motor to 90 degrees
set_angle(90)

# wait for 1 second
time.sleep(1)

# set the servo motor to 180 degrees
set_angle(180)

# stop the PWM signal
pwm.stop()

# clean up the GPIO pins
GPIO.cleanup()
