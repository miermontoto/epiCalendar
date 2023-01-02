import os
import uuid

from flask import Flask, render_template, request, send_file
from flask_talisman import Talisman

import epiCalendar
import utils

app = Flask(__name__, static_folder='./build', static_url_path='/', template_folder='./build')
Talisman(app, content_security_policy=None)

debug = os.environ.get('FLASK_ENV') == 'development'


@app.route('/', methods=['GET'])
def index():
    return serve()


@app.route('/', methods=['POST'])
def form_post():
    if debug: print(f"[DEBUG] POST data received from React: {request.form}")

    jsessionid = request.form['jsessionid']
    filename = request.form['filename']
    location = request.form['location'] == "true"
    classType = request.form['class-type'] == "true"
    extension = request.form['extension']

    if debug:
        print(f"[DEBUG] Calendar info: {jsessionid} → {filename}{extension}")
        print(f"[DEBUG] Location parsing: {location}")
        print(f"[DEBUG] Class type parsing: {classType}")
        print(f"[DEBUG] iCalendar mode: {extension == '.ics'}")

    if not utils.verifyCookieExpiration(jsessionid):
        print("[DEBUG] [ERROR] Expired cookie submited.")
        return serve(slug="ERROR: cookie inválida.")

    uuidStr = str(uuid.uuid4())
    argv = [jsessionid, '--location', 'on' if location else 'off', '--class-type', 'on' if classType else 'off', '-o', uuidStr, '--format', extension[1:]]

    backendFilename = uuidStr + extension
    downloadFilename = filename + extension

    if debug:
        print(f"[DEBUG] UUID: {uuidStr}")
        print(f"[DEBUG] Arguments: {argv}")

    exitCode = epiCalendar.main(argv)
    if os.path.exists(backendFilename) and exitCode == 0:
        if debug: print(f"[DEBUG] Attempting to serve {backendFilename} as {downloadFilename}.")
        target = send_file(backendFilename, as_attachment=True, attachment_filename=downloadFilename)
        if os.path.exists(backendFilename): os.remove(backendFilename)
        if debug: print("[DEBUG] File served.")
        return target
    elif exitCode == 2:
        if debug: print("[DEBUG] [ERROR] ¿No calendar events?")
        return serve(slug="ERROR: No hay eventos en el calendario.")

    if debug: print("[DEBUG] [ERROR] Script failed to generate file.")
    return serve(slug="ERROR: No se pudo generar el calendario.")


@app.errorhandler(404)
def serve(slug=""):
    return render_template('index.html', slug=slug)
