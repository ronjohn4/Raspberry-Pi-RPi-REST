# RPi-REST

RPi-REST is a mimumun functionality REST wrapper for the GPIO library.  The hardware is the ultimate definition of pin configuration so the RPiServer.py defines the pin configuration.

## Routes
Routes are handled by flask.  The routes are:

### /gpio/api/v1.0/pins/getstate
returns the current state of all configured pins as json.

### /gpio/api/v1.0/pins/<int:getPin>
returns the state of <getPin>

### /gpio/api/v1.0/pins/<int:changePin>/<int:value>
sets <changePin> to state specified by <int:value>

## Architecture
On the raspberry pi RPiServer.py handles incomming requests.  Requests have a fair amount of validation and return informative fails.  Valid requests are passed on to GPIO natively to perform the request.

The Client is a simple Python command line program that lets the user enter specific commands (e.g. '23 on' will turn pin 23 on) and makes the REST call to the raspberry pi.

RPiClient-test.py is minimum set of unittests to ensure you have everything wired up.  The pins = {} definition should match the definition you are using in RPiServer.py.  RPiServer.py should defined the pins based on your specific hardware project.  A quick snapshot of the project used to test is below:

![pins](https://cloud.githubusercontent.com/assets/3393772/22186702/36a9f5f4-e0b7-11e6-942c-6a36234056e8.png)

## Helpful Commands
To install GPIO on your raspberry pi use:
sudo apt-get install python-rpi.gpio
