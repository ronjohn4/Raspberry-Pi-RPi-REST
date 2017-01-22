import requests
import unittest
import json

class GPIO():
    LOW = 0
    HIGH = 1
    OUT = 0
    IN = 1
    PUD_UP = 22

url = 'http://10.0.0.11/gpio/api/v1.0/'

# Default config from RPiServer.py
pins = {
    18 : {'name' : 'GPIO 18', 'state' : GPIO.HIGH, 'direction' : GPIO.IN, 'pull_up_down' : GPIO.PUD_UP},
    23 : {'name' : 'GPIO 23', 'state' : GPIO.LOW, 'direction' : GPIO.OUT, 'pull_up_down' : None},
    24 : {'name' : 'GPIO 24', 'state' : GPIO.LOW, 'direction' : GPIO.OUT, 'pull_up_down' : None}
}

class TestRPi(unittest.TestCase):

    def setUp(self):
        for pin in pins:
            if pins[pin]['direction'] == GPIO.OUT:
                response = requests.get(url + 'pins/{0}/{1}'.format(pin, pins[pin]['state']))

    def test_getstate(self):
        response = requests.get(url + 'pins/getstate')
        self.assertEqual(json.dumps(pins, sort_keys=True), json.dumps(response.json(), sort_keys=True))

    def test_pins(self):
        response = requests.get(url + 'pins/getstate')
        pins_start = response.json()
        response = requests.get(url + 'pins/23/1')
        response = requests.get(url + 'pins/getstate')
        pins_stop = response.json()

        # change the json to reflect the change
        pins_start['23']['state'] = GPIO.HIGH

        self.assertEqual(json.dumps(pins_start, sort_keys=True), json.dumps(pins_stop, sort_keys=True))

    def tearDown(self):
        for pin in pins:
            if pins[pin]['direction'] == GPIO.OUT:
                response = requests.get(url + 'pins/{0}/{1}'.format(pin, pins[pin]['state']))


if __name__ == '__main__':
    unittest.main()


