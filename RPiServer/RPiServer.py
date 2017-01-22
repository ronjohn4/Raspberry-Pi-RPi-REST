import RPi.GPIO as GPIO
from flask import Flask, jsonify
from flask_restful import Api

app = Flask(__name__)
api = Api(app)
GPIO.setmode(GPIO.BCM)

# List of pins, name, direction and pull_up_down are assumed to be be static and based on the hardware
pins = {
    18 : {'name' : 'GPIO 18', 'state' : GPIO.HIGH, 'direction' : GPIO.IN, 'pull_up_down' : GPIO.PUD_UP},
    23 : {'name' : 'GPIO 23', 'state' : GPIO.LOW, 'direction' : GPIO.OUT, 'pull_up_down' : None},
    24 : {'name' : 'GPIO 24', 'state' : GPIO.LOW, 'direction' : GPIO.OUT, 'pull_up_down' : None}
}


# Initialize pins at startup
for pin in pins:
    GPIO.setup(pin, pins[pin]['direction'])
    if pins[pin]['direction'] == GPIO.OUT:
        GPIO.setup(pin, pins[pin]['direction'])
        GPIO.output(pin, pins[pin]['state'])
    else:
        GPIO.setup(pin, GPIO.IN, pull_up_down=pins[pin]['pull_up_down'])


class InvalidUsage(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv

@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


@app.route('/gpio/api/v1.0/pins/getstate')
def get_state():
    for pin in pins:
        pins[pin]['state'] = GPIO.input(pin)

    return jsonify(pins)


@app.route('/gpio/api/v1.0/pins/<int:getPin>')
def get_pin(getPin):
    if getPin not in list(pins.keys()):
        raise InvalidUsage("pin={0} in not valid".format(getPin), status_code=410)

    if pins[getPin]['direction'] != GPIO.IN:
        raise InvalidUsage("pin {} isn't set for input".format(getPin), status_code=410)

    for pin in pins:
        pins[pin]['state'] = GPIO.input(pin)

    return jsonify({'value' : pins[pin]['state']})


@app.route('/gpio/api/v1.0/pins/<int:changePin>/<int:value>')
def set_pin(changePin, value):
    if changePin not in list(pins.keys()):
        raise InvalidUsage("pin={0} in not valid".format(changePin), status_code=410)

    if pins[changePin]['direction'] != GPIO.OUT:
        raise InvalidUsage("pin {} isn't set for output".format(changePin), status_code=410)

    if value == GPIO.HIGH or value == GPIO.LOW:
        GPIO.output(changePin, value)
    else:
        raise InvalidUsage("pin {} can't be set to value={1}".format(changePin, value), status_code=410)

    return jsonify(status = 'success')
    # return jsonify({'status' : 'success'})


if __name__ == '__main__':
    app.run(host='10.0.0.11', port=80, debug=True)
