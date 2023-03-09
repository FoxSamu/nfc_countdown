from bottle import route, run, template, static_file, response, HTTPError

from generator import Generator
import config
import log
import json
import traceback

cfg = config.load_config("./config.json")
log.info("Config loaded")
gen = Generator(cfg)

@route('/info.json')
def info():
    response.set_header('Cache-Control', 'no-store')
    response.content_type = "application/json"
    return json.dumps(gen.generate_info())

@route('/banner_1920.png')
def banner_1920():
    try:
        gen.generate()
    except Exception as e:
        return HTTPError(500, body="Failed to generate", exception=e)
    response = static_file('daystonfc_1920.png', root='./generated/')
    response.set_header('Cache-Control', 'no-store')
    return response

@route('/banner_800.png')
def banner_800():
    try:
        gen.generate()
    except Exception as e:
        return HTTPError(500, body="Failed to generate", exception=e)
    response = static_file('daystonfc_800.png', root='./generated/')
    response.set_header('Cache-Control', 'no-store')
    return response

@route('/banner_400.png')
def banner_400():
    try:
        gen.generate()
    except Exception as e:
        return HTTPError(500, body="Failed to generate", exception=e)
    response = static_file('daystonfc_400.png', root='./generated/')
    response.set_header('Cache-Control', 'no-store')
    return response

@route('/banner_200.png')
def banner_200():
    try:
        gen.generate()
    except Exception as e:
        return HTTPError(500, body="Failed to generate", exception=e)
    response = static_file('daystonfc_200.png', root='./generated/')
    response.set_header('Cache-Control', 'no-store')
    return response

run(host='localhost', port=3000)