#!/usr/bin/python3
# coding: utf-8

import argparse
import json
import re
import sys
import time
import urllib.parse
from datetime import datetime  # needed to convert academic years to unix timestamps
from ics import (Calendar, Event)  # needed to save calendar in .ics format (iCalendar)

# import custom modules
import connect
import cookie
import parse

__version__ = "249"


class ApplicationError(Exception):
    # Base class for exceptions in this module.
    pass


class ResponseError(ApplicationError):
    # Invalid response from the server.
    pass


class BadCookieError(ApplicationError):
    # Invalid cookie introduced by the user.
    pass


def commence(msg):
    global status
    status = msg
    print(f"{msg} [ ]", end="\r", flush=True)
    return time.time()


def finalize(init):
    print(f"{status} [✓] ({(time.time() - init):.3f}s)")


class Class:
    def __init__(self, uid, title, start, end, location, description, class_type, subject):
        self.uid = uid
        self.title = title
        self.start_raw = start
        self.end_raw = end
        self.location = location
        self.description = description
        self.class_type = class_type
        self.subject = subject

        self.date = start.split(' ')[0]
        self.start = start.split(' ')[1]
        self.end = end.split(' ')[1]


# Function to send the first GET request using the cookie provided.
def get_first_request(jsessionid):
    init = commence("Sending initial payload")

    r = connect.first_request(jsessionid)
    if r.status_code != 200: raise ResponseError("Unexpected response code")

    finalize(init)
    return r.text


# Function to extract the cookies necessary to make the POST request, from the server response of the first request.
def extract_cookies(response):
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
        raise BadCookieError("Invalid JSESSIONID")

    finalize(init)
    return [source, viewstate, submit]  # Return a list that contains the extracted parameters.


# Function that sends the HTTP POST request to the server and retrieves the raw data of the calendar.
# The raw text response is returned.
def post_request(jsessionid, cookies, options):
    init = commence("Obtaining raw calendar data")

    if options["years"] == "auto":
        e = datetime.now()
        start = int(datetime.timestamp(datetime(e.year if e.month >= 9 else e.year - 1, 9, 1)) * 1000)
        end = int(datetime.timestamp(datetime(e.year + 1 if e.month >= 9 else e.year, 6, 1)) * 1000)
    elif options["years"] == "all":
        start = int(datetime.timestamp(datetime(2000, 9, 1)) * 1000)
        end = int(datetime.timestamp(datetime(2100, 6, 1)) * 1000)
    else:
        years = options["years"].split('-')
        start = int(datetime.timestamp(int(f"20{years[0]}"), 9, 1) * 1000)
        end = int(datetime.timestamp(int(f"20{years[1]}"), 6, 1) * 1000)

    if options["terms"].lower() == "q1": end -= 13042800000
    elif options["terms"].lower() == "q2": start += 10544400000

    source = cookies[0]
    view = cookies[1]
    submit = cookies[2]

    # Creating the body with the parameters extracted before, with the syntax required by the server.
    payload = f"javax.faces.partial.ajax=true&javax.faces.source={source}&javax.faces.partial.execute={source}&javax.faces.partial.render={source}&{source}={source}&{source}_start={start}&{source}_end={end}&{submit}_SUBMIT=1&javax.faces.ViewState={view}"

    # Send the POST request.
    result = connect.post_request(payload, jsessionid).text

    # Basic response verification.
    if result.split('<')[-1] != "/partial-response>":
        raise ResponseError("Invalid response (no partial-response)")

    # extract a sample event id from the first event.
    # used to craft the payload for the second request.
    # if there are no ids, the calendar is empty.
    try: sample_id = re.search(r'[a-z0-9]{8}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{12}', result).group(0)
    except AttributeError: raise AttributeError("Empty calendar")

    locations = {}
    if options["locationParsing"] or options["links"]:
        # obtain links for each event location.
        # links are used to obtain room codes, which include city, building and other important info.
        loc_payload classType= f"javax.faces.partial.ajax=true&javax.faces.source={source}&javax.faces.partial.execute={source}&javax.faces.partial.render={source[:10:]}eventDetails+{source[:10:]}aulas_url&javax.faces.behaviour.event=eventSelect&javax.faces.partial.event=eventSelect&{source}_selectedEventId={sample_id}&{submit}_SUBMIT=1&javax.faces.ViewState={view}"
        loc_info = connect.post_request(loc_payload, jsessionid).text

        # process response and filter out html code and garbage.
        chars_to_remove = ['\t', '\n', 'class="enlaceUniovi"', '</li>', '</a>', '<a href=', 'target="_blank">', '"']
        for char in chars_to_remove:
            loc_info = loc_info.replace(char, '')

        loc_info = loc_info.split('<li>')[1:]
        loc_info[-1] = loc_info[-1].split('</ul>')[0]

        # save each link in a dictionary.
        for location in loc_info:
            locations[location.split('  ')[1].lower()] = location.split('  ')[0]

    finalize(init)
    return result, locations


def obtain_events(raw_response, locations, options):
    init = commence("Parsing events")

    description = options['description']
    links = options['links']
    type_parsing = options['classTypeParsing']
    loc_parsing = options['locationParsing']

    data = json.loads(raw_response.split('[{"events" : ')[1].split('}]]')[0])
    classes = []

    for event in data:
        start = event['start'].replace('T', ' ').split('+')[0]
        end = event['end'].replace('T', ' ').split('+')[0]
        desc = event['description'].replace('\n', '')

        title_split = event['title'].split(" - ")
        subject = title_split[0]
        class_type = parse.parse_class_type(title_split[1]) if type_parsing else title_split[1]
        title = f"{subject} ({class_type})"

        loc = " - ".join(desc.split(" - ")[1:])  # allow for multiple ' - ' in the description
        code = locations[loc.lower()].split('?codEspacio=')[1] if links or loc_parsing else {}
        location = parse.parse_location(loc, code) if loc_parsing else loc
        if links: desc += f" ({locations[loc.lower()]})"

        classes.append(Class(event['id'], title, start, end, location, desc if description else "", class_type, subject))

    finalize(init)
    return classes


def generate_output(classes, filename, format):
    name = f"{filename}.{format}"
    init = commence(f"Generating output ({name})")

    ics = format == "ics"

    # Generate the output file.
    if ics: c = Calendar()
    else:
        g = open(name, "w")
        g.write("Subject,Start Date,Start Time,End Date,End Time,Location,Description\n")

    # Write each event to the file.
    for event in classes:
        if ics:
            c.events.add(Event(name=event.title, begin=event.start_raw, end=event.end_raw,
                               description=event.description, location=event.location, uid=event.uid))
        else:
            g.write(f"{event.title},{event.date},{event.start},{event.date},{event.end},{event.location},{event.description}\n")

    # Write the file to disk.
    if ics:
        with open(name, "w") as f:
            for i in c.serialize_iter():
                if bool(re.search(r'DT((START)|(END)):', i.strip())): f.write(i.replace('Z', ''))  # remove Z from timestamps
                else: f.write(i)
    else: g.close()

    finalize(init)


def print_stats(classes):
    stats = {
        "hours": 0,
        "days": {},
        "days_gaps": {},
        "classTypes": {},
        "locations": {},
        "subjects": {},
        "Q1": [0, 0],
        "Q2": [0, 0]
    }

    for event in classes:
        date = event.date
        location = event.location
        class_type = event.class_type
        subject = event.subject

        hours = int(event.end.split(':')[0]) - int(event.start.split(':')[0])
        minutes = int(event.end.split(':')[1]) - int(event.start.split(':')[1])
        hours = hours + minutes / 60
        stats["hours"] += hours

        for key, value in [("classTypes", class_type), ("locations", location), ("subjects", subject)]:
            if value not in stats[key]: stats[key][value] = [0, 0]
            stats[key][value][0] += 1
            stats[key][value][1] += hours

        if date not in stats["days"]: stats["days"][date] = 0
        stats["days"][date] += hours

        quarter = "Q1" if int(date.split('-')[1]) >= 9 else "Q2"
        stats[quarter][0] += 1
        stats[quarter][1] += hours

    # Sort the class types and locations by number of occurrences.
    for key in ["classTypes", "locations"]:
        stats[key] = sorted(stats[key].items(), key=lambda x: x[1][0], reverse=True)

    # Sort the days by date.
    stats["days"] = dict(sorted(stats["days"].items(), key=lambda x: x[0]))

    # Sort the subjects alphabetically.
    stats["subjects"] = dict(sorted(stats["subjects"].items(), key=lambda x: x[0]))

    for day in stats["days"].keys():
        events = [c for c in classes if c.date == day]

        earliest = min(events, key=lambda x: x.start_raw)
        latest = max(events, key=lambda x: x.end_raw)

        earliest_hours = int(earliest.start.split(':')[0]) + int(earliest.start.split(':')[1]) / 60
        latest_hours = int(latest.end.split(':')[0]) + int(latest.end.split(':')[1]) / 60
        time = latest_hours - earliest_hours
        stats["days_gaps"][day] = time

    print("\nStatistics:")
    print(f"\tTotal hours: {stats['hours']}h pure, {sum(stats['days_gaps'].values())}h total")
    print(f"\tAttendance: {len(stats['days'])} days, {sum(stats['days_gaps'].values()) / len(stats['days']):.2f}h on average")
    print(f"\tMax hours per day: {max(stats['days_gaps'].values())}h ({', '.join([c for c in stats['days_gaps'] if stats['days_gaps'][c] == max(stats['days_gaps'].values())])})")
    print(f"\tFirst quarter: {stats['Q1'][0]} classes, {stats['Q1'][1]}h")
    print(f"\tSecond quarter: {stats['Q2'][0]} classes, {stats['Q2'][1]}h")

    print("\n\tClass types:")
    for class_type in stats["classTypes"]:
        print(f"\t\t{class_type[0]}: {class_type[1][0]} ({class_type[1][1]}h)")

    print("\n\tLocations:")
    for location in stats["locations"]:
        print(f"\t\t{location[0]}: {location[1][0]} ({location[1][1]}h)")

    print("\n\tSubjects:")
    for subject in stats["subjects"]:
        print(f"\t\t{subject}: {stats['subjects'][subject][0]} ({stats['subjects'][subject][1]}h)")


def main(argv) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("session", metavar="JSESSIONID", help="JSESSIONID cookie value")
    parser.add_argument("--location", choices=["on", "off"], default="on", help="enables or disables the parsing of the location of the class (default: 'on')")
    parser.add_argument("--class-type", choices=["on", "off"], default="on", help="enables or disables the parsing of the class type of the class (default: 'on')")
    parser.add_argument("--links", choices=["on", "off"], default="on", help="enables or disables placing links of rooms in the description of the events (default: 'on')")
    parser.add_argument("--statistics", "-s", "--stats", action="store_true", help="returns various statistics about all the events collected (default: 'off')")
    parser.add_argument("--format", choices=["csv", "ics"], default="ics", help="sets the output file format (default: 'ics')")
    parser.add_argument("--dry-run", action='store_true', help="disables the generation of files (default: 'off')")
    parser.add_argument("--output-file", "-o", "--filename", "-f", default="Calendario", help="sets the name of the output file (default: 'Calendario')")
    parser.add_argument("--separate-by", choices=["subject", "class_typeclassType"], help="creates separate files depending on the option selected (default: 'off')")
    parser.add_argument("--description", choices=["on", "off"], default="on", help="enables or disables the description of the events (default: 'on')")
    parser.add_argument("-v", "--version", action="version", version=f"epiCalendar c{__version__} by Juan Mier (mier@mier.info)")
    parser.add_argument("--years", "-y", default="auto", help="sets the range of years to be parsed. format: yy-yy (default: auto, eg: 20-21)")
    parser.add_argument("--term", "-t", default="all", help="sets the terms to be parsed.", choices=["q1", "q2", "all"])

    args = parser.parse_args(argv)

    location = args.location == "on"
    class_type = args.class_type == "on"
    links = args.links == "on"
    stats = args.statistics
    file_format = args.format
    dry_run = args.dry_run
    filename = args.output_file
    session = args.session
    separate = args.separate_by
    description = args.description == "on"
    years = args.years
    terms = args.term

    options = {
        "locationParsing": location,
        "classTypeParsing": class_type,
        "links": links,
        "description": description,
        "years": years,
        "terms": terms
    }

    # If the JSESSIONID is not valid, exit.
    if not cookie.verify_structure(session):
        print("Invalid JSESSIONID.")
        return 1

    cookies = extract_cookies(get_first_request(session))
    raw_response, locations = post_request(session, cookies, options)
    classes = obtain_events(raw_response, locations, options)
    if not dry_run:
        if separate is not None:
            for element in list(set([getattr(c, separate) for c in classes])):
                generate_output([c for c in classes if getattr(c, separate) == element], f"{filename}_{element.replace(' ', '')}", file_format)
        else: generate_output(classes, filename, file_format)
    try:
        pass
    except Exception as e:
        print(f"{status} [×] ({e})")
        return 2 if e.__class__ == AttributeError else 1

    print("\nScript finished, %d events parsed." % len(classes))

    if stats: print_stats(classes)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
