#!/usr/bin/python3
# coding: utf-8

import argparse
import json
import re
import sys
import time
import traceback
import urllib.parse
from datetime import datetime  # needed to convert academic years to unix timestamps
from ics import (Calendar, Event)  # needed to save calendar in .ics format (iCalendar)

# import custom modules
import connect
import parse
import utils


def commence(msg):
    global status
    status = msg
    print(f"{msg} [ ]", end="\r", flush=True)
    return time.time()


def finalize(init):
    print(f"{status} [✓] ({(time.time() - init):.3f}s)")


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
    reg = '"([^"]*)"'
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
    if locationParsing or links:
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

    data = json.loads(rawResponse.split('[{"events" : ')[1].split('}]]')[0])
    classes = []

    for event in data:
        start = event['start'].replace('T', ' ').split('+')[0]
        end = event['end'].replace('T', ' ').split('+')[0]
        desc = event['description'].replace('\n', '')

        titleSplit = event['title'].split(" - ")
        subject = titleSplit[0]
        classType = parse.parseClassType(titleSplit[1]) if classTypeParsing else titleSplit[1]
        title = f"{subject} ({classType})"

        loc = desc.split(" - ")[1]
        code = locations[loc.lower()].split('?codEspacio=')[1] if links or locationParsing else {}
        location = parse.parseLocation(loc, code) if locationParsing else loc
        if links: desc += f" ({locations[loc.lower()]})"

        classes.append(Class(event['id'], title, start, end, location, desc if description else "", classType, subject))

    finalize(init)
    return classes


def generateOutput(classes, filename):
    init = commence(f"Generating output ({filename}.{'ics' if icsMode else 'csv'})")

    # Generate the output file.
    if icsMode: c = Calendar()
    else:
        g = open(filename + ".csv", "w")
        g.write("Subject,Start Date,Start Time,End Date,End Time,Location,Description\n")

    # Write each event to the file.
    for event in classes:
        if icsMode:
            e = Event(name=event.title, begin=event.start_raw, end=event.end_raw, description=event.description, location=event.location, uid=event.uid)
            c.events.add(e)
        else:
            csv_line = f"{event.title},{event.date},{event.start},{event.date},{event.end},{event.location},{event.description}\n"
            g.write(csv_line)

    # Write the file to disk.
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
    global locationParsing, classTypeParsing, stats, icsMode, links, dryRun, separate, description

    parser = argparse.ArgumentParser()
    parser.add_argument("session", metavar="JSESSIONID", help="JSESSIONID cookie value.")
    parser.add_argument("--location", choices=["on", "off"], default="on", help="Enables or disables the parsing of the location of the class. Default is 'on'.")
    parser.add_argument("--class-type", choices=["on", "off"], default="on", help="Enables or disables the parsing of the class type of the class. Default is 'on'.")
    parser.add_argument("--links", choices=["on", "off"], default="on", help="Enables or disables placing links of rooms in the description of the events. Default is 'on'.")
    parser.add_argument("--statistics", "-s", "--stats", choices=["on", "off"], default="off", help="Returns various statistics about all the events collected. Default is 'off'.")
    parser.add_argument("--format", choices=["csv", "ics"], default="ics", help="Sets the output file format. Default is 'ics'.")
    parser.add_argument("--dry-run", action='store_true', help="Disables the generation of files.")
    parser.add_argument("--output-file", "-o", "--filename", "-f", default="Calendario", help="Sets the name of the output file.")
    parser.add_argument("--separate-by", choices=["subject", "classType"], help="Creates separate files depending on the option selected. Default is 'off'.")
    parser.add_argument("--description", choices=["on", "off"], default="on", help="Enables or disables the description of the events. Default is 'on'.")

    args = parser.parse_args()

    locationParsing = args.location == "on"
    classTypeParsing = args.class_type == "on"
    links = args.links == "on"
    stats = args.statistics == "on"
    icsMode = args.format == "ics"
    dryRun = args.dry_run
    filename = args.output_file
    session = args.session
    separate = args.separate_by
    description = args.description == "on"

    # If the JSESSIONID is not valid, exit.
    if not utils.verifyCookieStructure(session):
        print("Invalid JSESSIONID.")
        return 1

    try:
        cookies = extractCookies(getFirstRequest(session))
        rawResponse, locations = postCalendarRequest(session, cookies)
        classes = obtainEvents(rawResponse, locations)
        if not dryRun:
            if separate is not None:
                for element in list(set([getattr(c, separate) for c in classes])):
                    generateOutput([c for c in classes if getattr(c, separate) == element], filename + "_" + element.replace(' ', ''))
            else: generateOutput(classes, filename)
    except Exception as e:
        print(f"{status} [×]")
        traceback.print_exc()
        return 2 if e.__class__ == AttributeError else 1

    print("\nScript finished, %d events parsed." % len(classes))

    if stats: printStats(classes)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
