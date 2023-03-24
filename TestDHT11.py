import Adafruit_DHT

# Set sensor type : DHT11
sensor = Adafruit_DHT.DHT11

# Set GPIO pin number
pin = 4

# Read temperature and humidity from sensor
humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)

# Check if reading was successful
if humidity is not None and temperature is not None:
    print('Temperature={0:0.1f}*C  Humidity={1:0.1f}%'.format(temperature, humidity))
else:
    print('Failed to read sensor data')
