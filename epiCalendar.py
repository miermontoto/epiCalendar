#!/usr/bin/python3
# coding: utf-8

import re
import requests
import sys
import urllib.parse
import os
import time
import utils

# Declare global variables.
url = 'https://sies.uniovi.es/serviciosacademicos/web/expedientes/calendario.xhtml'
reg = '"([^"]*)"'
csvFile = "Calendario.csv" # Can be changed through "-o" flag.
rSession = requests.Session()

# Toggle location and class type parsing using the following global variables.
# If all special parsing is disabled, this script behaves almost exactly as the original one.
# If you intend to use this script for a non-EPI calendar, you should disable them all.
# This options can be easily toggled through argument flags.
enableLocationParsing = True
enableClassTypeParsing = True
enableStatistics = False


# Function to send the first GET request using the cookie provided.
def getFirstRequest(session_token):

    print("Sending initial payload...", end=" ", flush=True)
    initTime = time.time()

    payload = {
        'JSESSIONID': session_token,
        'cookieconsent_status': 'dismiss'
    }

    r = rSession.get(url, cookies=payload)
    print("✓ (%.3fs)" % (time.time() - initTime))

    return r.text

# Function to extract the cookies necessary to make the POST request, from the server response of the first request.
def extractCookies(get_response):
    print("Extracting cookies...", end=" ", flush=True)
    initTime = time.time()

    # Iterate the response lines to search the cookies, and save them in variables.
    found_first, found_second, found_third = False, False, False
    for line in get_response.split('\n'):
        if '<div id="j_id' in line and not found_first:
            source = urllib.parse.quote(re.findall(reg, line.split('<')[1])[0])
            found_first = True

        if 'javax.faces.ViewState' in line and not found_second:
            viewstate = urllib.parse.quote(re.findall(reg, line.split(' ')[12])[0])
            found_second = True

        if 'action="/serviciosacademicos/web/expedientes/calendario.xhtml"' in line and not found_third:
            submit = re.findall(reg, line.split(' ')[3])[0]
            found_third = True

        if found_first and found_second and found_third: break

    if not 'source' in locals(): # If the variable 'source' is not defined, the cookie was probably not valid.
        print("× (¿Invalid JSESSIONID?)")
        exit(1)

    print("✓ (%.3fs)" % (time.time() - initTime))
    return [source, viewstate, submit] # Return a list that contains the extracted parameters.

# Function that sends the HTTP POST request to the server and retrieves the raw data of the calendar.
# The raw text response is returned.
def postCalendarRequest(jsessionid, ajax, source, view, start, end, submit) -> str:

    print("Obtaining raw calendar data...", end=" ", flush=True)
    initTime = time.time()

    payload = {
        'JSESSIONID': jsessionid,
        'cookieconsent_status': 'dismiss'
    }

    # Define variables of the request.
    string_start = source + "_start"
    string_end = source + "_end"
    string_submit = submit + "_SUBMIT"

    # Creating the body with the parameters extracted before, with the syntax required by the server.
    body_payload = f"javax.faces.partial.ajax={ajax}&javax.faces.source={source}&javax.faces.partial.execute={source}&javax.faces.partial.render={source}&{source}={source}&{string_start}={start}&{string_end}={end}&{string_submit}=1&javax.faces.ViewState={view}"

    # Send the POST request.
    r = rSession.post(url, data=body_payload, headers={'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'}, cookies=payload)

    # Basic response verification.
    if r.text.split('<')[-1] != "/partial-response>":
        print("× (Invalid response)")
        exit(1)

    print("✓ (%.3fs)" % (time.time() - initTime))
    return r.text

# Parse the correct class name for each entry.
def parseLocation(loc):

    if not enableLocationParsing: return loc

    # Parse Aula AS-1 through Aula AS-11. (sometimes Aula As-X instead of Aula AS-X)
    asResult = re.search(r'A[Ss]-\d\d?', loc)
    if bool(asResult):
        return asResult.group(0).upper()

    # Parse 'Sala Informática Px', 'Aula de Informática Bx' and 'Aula Informática Sx'
    anResult = re.search(r'[PBS]\d', loc)
    if bool(anResult):
        return f"AN-{anResult.group(0)}"

    # Parse rooms from Edificio Polivalente using their code (format: X.X.XX)
    epResult = re.search(r'\d\.\d\.\d\d', loc)
    if bool(epResult):
        return f"EP-{epResult.group(0)}"

    # Parse 'Aula DE-1' through 'Aula DE-8'.
    deResult = re.search(r'DE-\d', loc)
    if bool(deResult):
        return f"{deResult.group(0)}"

    # Parse 'Aula DO-1' through 'Aula DO -17'
    doResult = re.search(r'DO[ ]?-\d\d?', loc)
    if bool(doResult):
        doFinal = doResult.group(0).replace(' ', '')
        if doFinal[-2:] == "10": # DO-10 can be DO-10A or DO-10B.
            return f"{doFinal}{loc[-1]}"
        return doFinal

    # Parse rooms from Departamental Oeste (Bajo cubierta) using their code (format: X.BC.XX)
    # Very similar codes to the EP rooms, can be difficult to parse.
    doResult = re.search(r'(\d.BC.\d\d)|(\d.S.\d\d)|(\d.B.\d\d)', loc)
    if bool(doResult):
        return f"DO-{doResult.group(0)}"

    # Parse 'Aula A' through 'Aula E'.
    # Has to be last because it is very generic and could match other locations.
    aeResult = re.search(r'Aula [A-E]', loc)
    if bool(aeResult):
        return f"AN-{aeResult.group(0)[-1]}"

    return loc

# Parse the correct "class type" for each entry.
# Also parses the group for each entry except for "Clase Expositiva".
# AFAIK there are only "Teoría (CEX)", "Prácticas de Aula (PAx)", "Prácticas de Laboratorio (PLx)" and "Teorías Grupales (TGx)".
def parseClassType(type):

    if not enableClassTypeParsing: return type
    classGroup = type.replace('.','').replace('-', ' ').rsplit()[-1].strip('0').upper()

    if "Teoría" in type: return f"CEX"
    if "Tutoría" in type or "Grupal" in type: return f"TG{classGroup}"
    if "Aula" in type: return f"PA{classGroup}"
    if "Laboratorio": return f"PL{classGroup}"

    return type # If the class type is not recognized, return the original string.

# Function that creates a CSV file readable by the applications, from the raw data previously retrieved.
def createCsv(rawResponse):

    print("Parsing data and generating new csv...", end=" ", flush=True)
    initTime = time.time()

    stats = {
        "hours": 0,
        "classes": 0,
        "classTypes": {},
        "locations": {}
    }

    g = open(csvFile, "w")

    # Write the headers in the first line.
    g.write("Asunto,Fecha de comienzo,Comienzo,Fecha de finalización,Finalización,Todo el día,Reminder on/off,Reminder Date,Reminder Time,Meeting Organizer,Required Attendees,Optional Attendees,Recursos de la reuniÃƒÂ³n,Billing Information,Categories,Description,Location,Mileage,Priority,Private,Sensitivity,Show time as\n")

    # Separate the events from its XML context.
    text = rawResponse.split('<')
    events = text[5].split('{')
    del events[0:2]

    # Each field of the event is separated by commas.
    for event in events:
        data = []
        for field in event.split(','):
            # Remove empty fields.
            if field.strip():
                data.append(field)
        # Save in variables the fields needed to build the CSV line of the event.
        title = data[1]
        start = data[2]
        end = data[3]
        description = data[7]

        # Make the necessary strings transformations to adapts the raw field data into a CSV readable file.
        title_csv = re.findall(reg, title.split(':')[1])[0]

        titleSplit = title_csv.split(" - ")
        classType = parseClassType(titleSplit[1])
        title = f"{titleSplit[0]} ({classType})"

        start_date = start.split(' ')[1].split('T')[0].split('"')[1]
        start_date_csv = start_date.split('-')[2]+'/'+start_date.split('-')[1]+'/'+start_date.split('-')[0]
        start_hour = start.split(' ')[1].split('T')[1].split('+')[0]
        end_date = end.split(' ')[1].split('T')[0].split('"')[1]
        end_date_csv = end_date.split('-')[2]+'/'+end_date.split('-')[1]+'/'+end_date.split('-')[0]
        end_hour = end.split(' ')[1].split('T')[1].split('+')[0]
        alert_date = start_date_csv
        alert_hour = str(int(start.split(' ')[1].split('T')[1].split('+')[0].split(':')[0]) - 1) + ':' + start.split(' ')[1].split('T')[1].split('+')[0].split(':')[1] + ':' + start.split(' ')[1].split('T')[1].split('+')[0].split(':')[2]
        event_creator = "Universidad de Oviedo"

        body = description.split('"')[3].replace(r'\n', '')
        info = body.replace(' - ', ' @ ')
        location = parseLocation(body.split(" - ")[1])

        # Write all the fields into a single line, and append it to the file.
        csv_line = f"{title},{start_date_csv},{start_hour},{end_date_csv},{end_hour},Falso,Falso,{alert_date},{alert_hour},{event_creator},,,,,,{info},{location},,Normal,Falso,Normal,2\n"
        g.write(csv_line)

        # Update the statistics.
        stats["classes"] += 1
        stats["hours"] += int(end_hour.split(':')[0]) - int(start_hour.split(':')[0])
        if classType not in stats["classTypes"]:
            stats["classTypes"] [classType] = 1
        else:
            stats["classTypes"][classType] += 1
        if location not in stats["locations"]:
            stats["locations"][location] = 1
        else:
            stats["locations"][location] += 1

    g.close()
    print("✓ (%.3fs)" % (time.time() - initTime))

    # Sort the class types and locations by number of occurrences.
    stats["classTypes"] = sorted(stats["classTypes"].items(), key=lambda x: x[1], reverse=True)
    stats["locations"] = sorted(stats["locations"].items(), key=lambda x: x[1], reverse=True)

    return stats


def main(argv) -> int:
    global enableLocationParsing, enableClassTypeParsing, enableStatistics, csvFile
    session = ""

    # Read flags from arguments.
    if not len(argv) == 1 and (argv[1] == "--help" or argv[1] == "-h"):
        print("Usage: python3 epiCalendar.py [JSESSIONID] [-o | --output-file <filename>] [--disable-location-parsing] [--disable-class-type-parsing]")
        exit(0)

    for i in range(1, len(argv)):
        if argv[i] == "--disable-location-parsing": enableLocationParsing = False
        if argv[i] == "--disable-class-type-parsing": enableClassTypeParsing = False
        if argv[i] == "-o" or argv[i] == "--output-file" : csvFile = argv[i+1]
        if argv[i] == "-s" or argv[i] == "--stats" or argv[i] == "--enable-statistics": enableStatistics = True
        if utils.verifyCookieStructure(argv[i]): session = argv[i]

    # If the required argument hasn't been provided, read from input.
    if session == "":
        try:
            session = input("Enter JSESSIONID: ")
        except (KeyboardInterrupt, EOFError):
            exit(0)

    # If the JSESSIONID is not valid, exit.
    if not utils.verifyCookieStructure(session):
        print("× Invalid JSESSIONID.")
        exit(1)

    startTime = time.time()
    cookies = extractCookies(getFirstRequest(session))
    stats = createCsv(postCalendarRequest(session, "true", cookies[0], cookies[1], "1630886400000", "1652054400000", cookies[2]))
    print("\nCalendar generated, took %.3fs" % (time.time() - startTime))
    print("Saved as \"%s\"" % csvFile)

    if enableStatistics:
        print("\nStatistics:")
        print("\tClasses: %d" % stats["classes"])
        print("\tHours: %d" % stats["hours"])
        print("\tClass types:")
        for classType in stats["classTypes"]:
            print("\t\t%s: %d" % (classType[0], classType[1]))
        print("\tLocations:")
        for location in stats["locations"]:
            print("\t\t%s: %d" % (location[0], location[1]))

    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv))
