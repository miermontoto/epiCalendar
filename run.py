import os
import uuid

from flask import Flask, render_template, request, send_file
from flask_talisman import Talisman

import epiCalendar
import cookie

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
    class_type = request.form['class-type'] == "true"
    extension = request.form['extension']

    if debug:
        print(f"[DEBUG] Calendar info: {jsessionid} → {filename}{extension}")
        print(f"[DEBUG] Location parsing: {location}")
        print(f"[DEBUG] Class type parsing: {class_type}")
        print(f"[DEBUG] iCalendar mode: {extension == '.ics'}")

    if not cookie.verify_expiration(jsessionid):
        print("[DEBUG] [ERROR] Expired cookie submited.")
        return serve(slug="ERROR: cookie inválida.")

    uuid_string = str(uuid.uuid4())
    argv = [jsessionid, '--location', 'on' if location else 'off', '--class-type', 'on' if class_type else 'off', '-o', uuid_string, '--format', extension[1:]]

    backend_filename = uuid_string + extension
    download_filename = filename + extension

    if debug:
        print(f"[DEBUG] UUID: {uuid_string}")
        print(f"[DEBUG] Arguments: {argv}")

    exit_code = epiCalendar.main(argv)
    if os.path.exists(backend_filename) and exit_code == 0:
        if debug: print(f"[DEBUG] Attempting to serve {backend_filename} as {download_filename}.")
        target = send_file(backend_filename, as_attachment=True, download_name=download_filename)
        if os.path.exists(backend_filename): os.remove(backend_filename)
        if debug: print("[DEBUG] File served.")
        return target
    elif exit_code == 2:
        if debug: print("[DEBUG] [ERROR] ¿No calendar events?")
        return serve(slug="ERROR: No hay eventos en el calendario.")

    if debug: print("[DEBUG] [ERROR] Script failed to generate file.")
    return serve(slug="ERROR: No se pudo generar el calendario.")


@app.errorhandler(404)
def serve(slug=""):
    return render_template('index.html', slug=slug)
