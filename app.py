import logging
from flask import Flask, render_template
from markupsafe import escape

logger = logging.getLogger('app')
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s [%(name)s] %(levelname)s: %(message)s')
handler = logging.StreamHandler()
handler.setLevel(logging.DEBUG)
handler.setFormatter(formatter)
logger.addHandler(handler)

_GPIO = True

try:
    import RPi.GPIO as GPIO
except RuntimeError:
    logger.warning('No GPIO')
    _GPIO = False

app = Flask('romiblue')

if _GPIO:
    light_gpio = 6
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(light_gpio, GPIO.OUT)
    GPIO.output(light_gpio, 0)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/light/<mode>', methods=['GET', 'POST'])
def light(mode):
    if mode == 'on':
        logger.info('light on.')
        if _GPIO:
            GPIO.output(light_gpio, 1)
        return {'status': 'on'}, 200
    elif mode == 'off':
        logger.info('light off.')
        if _GPIO:
            GPIO.output(light_gpio, 0)
        return {'status': 'off'}, 200
    else:
        logger.warning(f'light "{escape(mode)}" is not a valid mode.')
        return {'error': 'Invalid mode'}, 400


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5000)
