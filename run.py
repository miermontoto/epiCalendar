import epiCalendar
import os
import uuid
import utils
import re
import msal
import app_config
import requests
import connect

from flask import Flask, render_template, request, send_file, session, redirect, url_for
from flask_session import Session
from flask_talisman import Talisman

app = Flask(__name__)
app.config.from_object(app_config)
Talisman(app, content_security_policy=None)
Session(app)

defaultFilename = epiCalendar.filename
debug = os.environ.get('FLASK_ENV') == 'development'

@app.route("/", methods = ['GET'])
def index():
    if not session.get("user"):
        return redirect(url_for("login"))
    return render_template('index.html', user=session["user"])

@app.route("/login")
def login():
    # Technically we could use empty list [] as scopes to do just sign in,
    # here we choose to also collect end user consent upfront
    if session.get("user"):
        return authorized()
    session["flow"] = _build_auth_code_flow(scopes=app_config.SCOPE)
    return render_template("login.html", auth_url=session["flow"]["auth_uri"], version=msal.__version__)

@app.route(app_config.REDIRECT_PATH)  # Its absolute URL must match your app's redirect_uri set in AAD
def authorized():
    try:
        cache = _load_cache()
        result = _build_msal_app(cache=cache).acquire_token_by_auth_code_flow(
            session.get("flow", {}), request.args)
        if "error" in result:
            return render_template("auth_error.html", result=result)
        session["user"] = result.get("id_token_claims")
        _save_cache(cache)
    except ValueError:  # Usually caused by CSRF
        pass  # Simply ignore them
    return redirect(url_for("index"))

@app.route("/logout")
def logout():
    session.clear()  # Wipe out user and its token cache from session
    return redirect(  # Also logout from your tenant's web session
        app_config.AUTHORITY + "/oauth2/v2.0/logout" +
        "?post_logout_redirect_uri=" + url_for("index", _external=True))

@app.route("/graphcall")
def graphcall():
    token = _get_token_from_cache(app_config.SCOPE)
    if not token:
        return redirect(url_for("login"))
    graph_data = requests.get(  # Use token to call downstream service
        app_config.ENDPOINT,
        headers={'Authorization': 'Bearer ' + token['access_token']},
        ).json()
    return render_template('display.html', result=graph_data)


def _load_cache():
    cache = msal.SerializableTokenCache()
    if session.get("token_cache"):
        cache.deserialize(session["token_cache"])
    return cache

def _save_cache(cache):
    if cache.has_state_changed:
        session["token_cache"] = cache.serialize()

def _build_msal_app(cache=None, authority=None):
    return msal.ConfidentialClientApplication(
        app_config.CLIENT_ID, authority=authority or app_config.AUTHORITY,
        client_credential=app_config.CLIENT_SECRET, token_cache=cache)

def _build_auth_code_flow(authority=None, scopes=None):
    return _build_msal_app(authority=authority).initiate_auth_code_flow(
        scopes or [],
        redirect_uri=url_for("authorized", _external=True))

def _get_token_from_cache(scope=None):
    cache = _load_cache()  # This web app maintains one cache per session
    cca = _build_msal_app(cache=cache)
    accounts = cca.get_accounts()
    if accounts:  # So all account(s) belong to the current signed-in user
        result = cca.acquire_token_silent(scope, account=accounts[0])
        _save_cache(cache)
        return result

app.jinja_env.globals.update(_build_auth_code_flow=_build_auth_code_flow)  # Used in template

if __name__ == "__main__":
    app.run()

@app.route('/', methods = ['POST'])
def form_post():
    if debug: print(f"[DEBUG] POST data received from React: {request.form}")

    if request.form.get('logout') == 'true':
        logout()
        return index()


    idToken = str(session['token_cache']).split('"secret": "')[2].split('"')[0]
    payload = f"id_token={idToken}"
    print(payload)
    print(requests.post(connect.cassiUrl, data=payload, headers={'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'}))
    return index()

    filename = request.form['filename']
    location = request.form['location'] == "true"
    classType = request.form['class-type'] == "true"
    extension = request.form['extension']

    if debug:
        print(f"[DEBUG] Calendar info: {jsessionid} → {filename}{extension}")
        print(f"[DEBUG] Location parsing: {location}")
        print(f"[DEBUG] Class type parsing: {classType}")
        print(f"[DEBUG] iCalendar mode: {extension == '.ics'}")

    if utils.verifyCookieExpiration(jsessionid):

        argv = ['epiCalendar.py', jsessionid]

        if not location: argv.append('--disable-location-parsing')
        if not classType: argv.append('--disable-class-type-parsing')

        uuidStr = str(uuid.uuid4())
        argv.append('-o')
        argv.append(uuidStr)

        backendFilename = uuidStr + extension
        downloadFilename = filename + extension
        if extension == ".csv": argv.append('--csv')

        if debug:
            print(f"[DEBUG] UUID: {uuidStr}")
            print(f"[DEBUG] Arguments: {argv}")

        exitCode = epiCalendar.main(argv)
        if os.path.exists(backendFilename) and exitCode == 0:
            if debug: print(f"[DEBUG] Attempting to serve {backendFilename} as {downloadFilename}.")
            target = send_file(backendFilename, as_attachment=True, attachment_filename=downloadFilename)
            if os.path.exists(backendFilename): os.remove(backendFilename)
            if debug: print(f"[DEBUG] File served.")
            return target
        elif exitCode == 2:
            if debug: print("[DEBUG] [ERROR] ¿No calendar events?")
            return serve(slug="ERROR: No hay eventos en el calendario.")
        if debug: print("[DEBUG] [ERROR] Script failed to generate file.")
        return serve("ERROR: No se pudo generar el calendario.")

    elif debug:
        print("[DEBUG] [ERROR] Expired cookie submited.")

    return serve(slug="ERROR: cookie inválida.")


@app.errorhandler(404)
def serve(slug=""):
    return render_template('index.html', slug=slug)
