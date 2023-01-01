#!/usr/bin/python3
# coding: utf-8

import re
import sys
import time
import urllib.parse
from datetime import datetime  # needed to convert academic years to unix timestamps
from ics import (Calendar, Event)  # needed to save calendar in .ics format (iCalendar)

# import custom modules
import connect
import parse
import utils

# Declare global variables.
reg = '"([^"]*)"'
filename = "Calendario"  # Can be changed through "-o" flag.


def commence(msg):
    print(f"{msg}...", end=" ", flush=True)
    return time.time()


def finalize(init):
    print("✓ (%.3fs)" % (time.time() - init))


class Class:
    def __init__(self, uid, title, start, end, location, description, classType, subject):
        self.uid = uid
        self.title = title
        self.start_raw = start
        self.end_raw = end
        self.location = location
        self.description = description
        self.classType = classType
        self.subject = subject

        self.date = start.split(' ')[0]
        self.start = start.split(' ')[1]
        self.end = end.split(' ')[1]


# Function to send the first GET request using the cookie provided.
def getFirstRequest(jsessionid):
    init = commence("Sending initial payload")

    r = connect.firstRequest(jsessionid)
    if r.status_code != 200: raise Exception("Unexpected response code")

    finalize(init)
    return r.text


# Function to extract the cookies necessary to make the POST request, from the server response of the first request.
def extractCookies(response):
    init = commence("Extracting cookies")

    # Iterate the response lines to search the cookies, and save them in variables.
    found_first, found_second, found_third = False, False, False
    for line in response.split('\n'):
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

    if 'source' not in locals():  # If the variable 'source' is not defined, the cookie was probably not valid.
        raise Exception("Invalid JSESSIONID")

    finalize(init)
    return [source, viewstate, submit]  # Return a list that contains the extracted parameters.


# Function that sends the HTTP POST request to the server and retrieves the raw data of the calendar.
# The raw text response is returned.
def postCalendarRequest(jsessionid, cookies):
    init = commence("Obtaining raw calendar data")

    e = datetime.now()
    start = int(datetime.timestamp(datetime(e.year if e.month >= 9 else e.year - 1, 9, 1)) * 1000)
    end = int(datetime.timestamp(datetime(e.year + 1 if e.month >= 9 else e.year, 6, 1)) * 1000)

    # start = 1598914597000
    # end = 1693522597000

    source = cookies[0]
    view = cookies[1]
    submit = cookies[2]

    # Creating the body with the parameters extracted before, with the syntax required by the server.
    calendarPayload = f"javax.faces.partial.ajax=true&javax.faces.source={source}&javax.faces.partial.execute={source}&javax.faces.partial.render={source}&{source}={source}&{source}_start={start}&{source}_end={end}&{submit}_SUBMIT=1&javax.faces.ViewState={view}"

    # Send the POST request.
    result = connect.postRequest(calendarPayload, jsessionid).text

    # Basic response verification.
    if result.split('<')[-1] != "/partial-response>":
        raise Exception("Invalid response")

    # extract a sample event id from the first event.
    # used to craft the payload for the second request.
    # if there are no ids, the calendar is empty.
    try: sampleId = re.search(r'[a-z0-9]{8}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{12}', result).group(0)
    except AttributeError: raise AttributeError("Empty calendar")

    locations = {}
    if enableLocationParsing or enableLinks:
        # obtain links for each event location.
        # links are used to obtain room codes, which include city, building and other important info.
        locationPayload = f"javax.faces.partial.ajax=true&javax.faces.source={source}&javax.faces.partial.execute={source}&javax.faces.partial.render={source[:10:]}eventDetails+{source[:10:]}aulas_url&javax.faces.behaviour.event=eventSelect&javax.faces.partial.event=eventSelect&{source}_selectedEventId={sampleId}&{submit}_SUBMIT=1&javax.faces.ViewState={view}"
        locationInfo = connect.postRequest(locationPayload, jsessionid).text

        # process response and filter out html code and garbage.
        removeCharacters = ['\t', '\n', 'class="enlaceUniovi"', '</li>', '</a>', '<a href=', 'target="_blank">', '"']
        for char in removeCharacters:
            locationInfo = locationInfo.replace(char, '')

        locationInfo = locationInfo.split('<li>')[1:]
        locationInfo[-1] = locationInfo[-1].split('</ul>')[0]

        # save each link in a dictionary.
        for location in locationInfo:
            locations[location.split('  ')[1].lower()] = location.split('  ')[0]

    finalize(init)
    return result, locations


def obtainEvents(rawResponse, locations):

    init = commence("Parsing events")

    # Separate the events from its XML context.
    text = rawResponse.split('<')
    events = text[5].split('{')
    del events[0:2]

    classes = []  # create the calendar object.

    # Each field of the event is separated by commas.
    for event in events:
        data = []
        for field in event.split(','):  # obtain raw data.
            if field.strip(): data.append(field)

        # Save in variables the fields needed to build the CSV line of the event.
        uid = data[0].replace('"id": "', '')[0:-1]
        title = data[1].replace('"title": "', '')[0:-1]
        start = data[2].replace('"start": "', '')[0:-1].replace('T', ' ').split('+')[0]
        end = data[3].replace('"end": "', '')[0:-1].replace('T', ' ').split('+')[0]
        description = data[7].replace('"description":"', '').replace(r'\n', '').replace('"}', '').replace(']}]]>', '')

        titleSplit = title.split(" - ")
        classType = parse.parseClassType(titleSplit[1]) if enableClassTypeParsing else titleSplit[1]
        title = f"{titleSplit[0]} ({classType})"

        loc = description.split(" - ")[1]
        code = locations[loc.lower()].split('?codEspacio=')[1] if enableLinks or enableLocationParsing else {}
        location = parse.parseLocation(loc, code) if enableLocationParsing else loc
        if enableLinks: description += f" ({locations[loc.lower()]})"

        classes.append(Class(uid, title, start, end, location, description, classType, titleSplit[0]))

    finalize(init)
    return classes


def generateOutput(classes):
    init = commence("Generating output")

    if icsMode: c = Calendar()
    else:
        g = open(filename + ".csv", "w")
        g.write("Subject,Start Date,Start Time,End Date,End Time,Location,Description\n")

    for event in classes:
        if icsMode:
            e = Event(name=event.title, begin=event.start_raw, end=event.end_raw, description=event.description, location=event.location, uid=event.uid)
            c.events.add(e)
        else:
            csv_line = f"{event.title},{event.date},{event.start},{event.date},{event.end},{event.location},{event.description}\n"
            g.write(csv_line)

    if icsMode:
        with open(filename + ".ics", "w") as f:
            for i in c.serialize_iter():
                if "DTSTART" in i.strip() or "DTEND" in i.strip():
                    f.write(i.replace('Z', ''))
                else: f.write(i)
    else: g.close()

    finalize(init)


def printStats(classes):
    stats = {
        "hours": 0,
        "days": {},
        "classTypes": {},
        "locations": {},
        "subjects": {},
        "perHours": {},
        "Q1": [0, 0],
        "Q2": [0, 0]
    }

    for event in classes:
        start = event.start
        end = event.end
        date = event.date
        location = event.location
        classType = event.classType
        subject = event.subject

        hours = int(end.split(':')[0]) - int(start.split(':')[0])
        minutes = int(end.split(':')[1]) - int(start.split(':')[1])
        hours = hours + minutes / 60
        stats["hours"] += hours

        if classType not in stats["classTypes"]:
            stats["classTypes"][classType] = [0, 0]

        if location not in stats["locations"]:
            stats["locations"][location] = [0, 0]

        if date not in stats["days"]:
            stats["days"][date] = 0

        if subject not in stats["subjects"]:
            stats["subjects"][subject] = [0, 0]

        if hours not in stats["perHours"]:
            stats["perHours"][hours] = 0

        stats["classTypes"][classType][0] += 1
        stats["classTypes"][classType][1] += hours
        stats["locations"][location][0] += 1
        stats["locations"][location][1] += hours
        stats["days"][date] += hours
        stats["subjects"][subject][0] += 1
        stats["subjects"][subject][1] += hours
        stats["perHours"][hours] += 1

        if int(date.split('-')[1]) >= 9:
            stats["Q1"][0] += 1
            stats["Q1"][1] += hours
        else:
            stats["Q2"][0] += 1
            stats["Q2"][1] += hours

    # Sort the class types and locations by number of occurrences.
    stats["classTypes"] = sorted(stats["classTypes"].items(), key=lambda x: x[1], reverse=True)
    stats["locations"] = sorted(stats["locations"].items(), key=lambda x: x[1], reverse=True)

    print("\nStatistics:")
    print("\tTotal hours: %.2f" % stats["hours"])
    print("\tDays of attendance: %d" % len(stats["days"]))

    print("\tAverage hours per day: %.2f" % (stats["hours"] / len(stats["days"])))
    print("\tMax hours per day: %.2f" % max(stats["days"].values()))

    print("\tFirst quarter: %d classes (%.2f hours)" % (stats["Q1"][0], stats["Q1"][1]))
    print("\tSecond quarter: %d classes (%.2f hours)" % (stats["Q2"][0], stats["Q2"][1]))

    print("\n\tClasses per number of hours:")
    for hour in sorted(stats["perHours"].keys()):
        print("\t\t%d: %d" % (hour, stats["perHours"][hour]))

    print("\n\tClass types:")
    for classType in stats["classTypes"]:
        print("\t\t%s: %d (%.2fh)" % (classType[0], classType[1][0], classType[1][1]))

    print("\n\tLocations:")
    for location in stats["locations"]:
        print("\t\t%s: %d (%.2fh)" % (location[0], location[1][0], location[1][1]))

    print("\n\tSubjects:")
    for subject in stats["subjects"]:
        print("\t\t%s: %d (%.2fh)" % (subject, stats["subjects"][subject][0], stats["subjects"][subject][1]))


def main(argv) -> int:
    global enableLocationParsing, enableClassTypeParsing, enableStatistics, filename, icsMode, enableLinks, dryRun
    enableLocationParsing = True
    enableClassTypeParsing = True
    enableLinks = True
    enableStatistics = False
    icsMode = True
    dryRun = False

    session = ""  # JSESSIONID cookie value.

    # Read flags from arguments.
    if "--help" in argv or "-h" in argv:
        print("Usage: python epiCalendar.py [JSESSIONID]")
        print("\nFLAGS:")
        print("\t[--disable-location-parsing]: Disables the parsing of the location of the class.")
        print("\t[--disable-class-type-parsing]: Disables the parsing of the class type of the class.")
        print("\t[--disable-links]: Disables placing links of rooms in the description of the events.")
        print("\t[--enable-statistics | -s | --stats]: Returns various statistics about all the events collected.")
        print("\t[--csv]: saves the calendar as a CSV file instead of an iCalendar file.")
        print("\t[--dry-run]: blocks any file from being created.")
        print("\t[--help], -h: shows this help message.")
        print("\t[--output-file | -o]: sets the name of the output file.")
        return 0

    for i in range(1, len(argv)):
        if argv[i] == "--disable-location-parsing": enableLocationParsing = False
        if argv[i] == "--disable-class-type-parsing": enableClassTypeParsing = False
        if argv[i] == "--disable-links": enableLinks = False
        if argv[i] == "--csv": icsMode = False
        if argv[i] == "-o" or argv[i] == "--output-file": filename = argv[i + 1]
        if argv[i] == "-s" or argv[i] == "--stats" or argv[i] == "--enable-statistics": enableStatistics = True
        if argv[i] == "--dry-run": dryRun = True
        if utils.verifyCookieStructure(argv[i]): session = argv[i]

    # If the required argument hasn't been provided, read from input.
    if session == "":
        try: session = input("Enter JSESSIONID: ")
        except (KeyboardInterrupt, EOFError): return 0

    # If the JSESSIONID is not valid, exit.
    if not utils.verifyCookieStructure(session):
        print("Invalid JSESSIONID.")
        return 1

    startTime = time.time()
    try:
        cookies = extractCookies(getFirstRequest(session))
        rawResponse, locations = postCalendarRequest(session, cookies)
        classes = obtainEvents(rawResponse, locations)
        if not dryRun: generateOutput(classes)
    except Exception as e:
        print(f"× ({e})")
        return 2 if e.__class__ == AttributeError else 1

    print("\n%s, took %.3fs (%d events parsed)" % ("Dry run completed" if dryRun else "Calendar generated", time.time() - startTime, len(classes)))
    if not dryRun: print(f"Saved as \"{filename}.{'ics' if icsMode else 'csv'}\"")
    if enableStatistics: printStats(classes)

    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
