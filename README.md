# Raspberry-Pi-weather-window

Golas:

Here is the idea for implementing the project:
The temperature sensor measures the temperature and - if possible - also the humidity inside the room.
If the indoor temperature or humidity exceeds a certain value or range, a servo motor opens the window for ventilation.
 
The current weather forecast (e.g. possible via the OpenWheatherMap database) is used to monitor the weather.
 
However, the window is only opened
a) if it is not currently snowing or raining according to the weather API, the window is opened completely.
b) if it is currently snowing or raining according to the weather API, only in the tilt position.
c) if it is currently thunderstorming according to the weather API, the window remains closed.
 
 
