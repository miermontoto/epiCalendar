import os
import uuid

from flask import Flask, request, send_file, jsonify
from flask_talisman import Talisman
from flask_cors import CORS

import epiCalendar
import cookie

app = Flask(__name__)
CORS(app)  # permitir todos los orígenes en desarrollo
Talisman(app, content_security_policy=None)
debug = os.environ.get('FLASK_ENV') == 'development'


@app.route('/api/generate', methods=['POST'])
def form_post():
    if debug: print(f"[DEBUG] POST data received from React: {request.form}")

    # validar que todos los campos requeridos estén presentes
    jsessionid = request.form.get('jsessionid')
    filename = request.form.get('filename')
    extension = request.form.get('extension')

    if not all([jsessionid, filename, extension]):
        return jsonify({"error": "Faltan campos requeridos"}), 400

    location = request.form.get('location') == "true"
    class_type = request.form.get('class-type') == "true"

    if debug:
        print(f"[DEBUG] Calendar info: {jsessionid} → {filename}{extension}")
        print(f"[DEBUG] Location parsing: {location}")
        print(f"[DEBUG] Class type parsing: {class_type}")
        print(f"[DEBUG] iCalendar mode: {extension == '.ics'}")

    if not cookie.verify_expiration(jsessionid):
        print("[DEBUG] [ERROR] Expired cookie submited.")
        return jsonify({"error": "Cookie inválida"}), 400

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
        return jsonify({"error": "No hay eventos en el calendario"}), 400

    if debug: print("[DEBUG] [ERROR] Script failed to generate file.")
    return jsonify({"error": "No se pudo generar el calendario"}), 500


@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({"status": "ok"})
