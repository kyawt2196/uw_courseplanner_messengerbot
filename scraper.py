#! /usr/bin/env python

# You may redistribute this program and/or modify it under the terms of
# the GNU General Public License as published by the Free Software Foundation,
# either version 3 of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import sys
import json
import requests
from bs4 import BeautifulSoup

def getSchedulePage(year, quarter, major, campus = "S"):
    """Fetches the time schedule for a particular major and quarter

    @param year     The year (format: 2014)
    @param quarter  The quarter (WIN, SPR, SUM, AUT). Must be upper case.
    @param major    The major (ie. css, bbio). Must be lower case.
    @param campus   Specify "S", "B" or "T" for Seattle (default), Bothell or
        Tacoma.

    @return A BeautifulSoup object of the timeschedule page, ready for parsing
    """

    baseURL = "https://www.washington.edu/students/timeschd/"

    if campus == "B" or campus == "T":
        baseURL +=  campus + "/"
    elif campus != "S":
        raise InvalidCampus

    if quarter not in ["SPR", "SUM", "AUT", "WIN"]:
        raise InvalidQuarter

    baseURL += "%s%s/%s.html" % (quarter, year, major)

    headers = {"User-Agent": "UW Courselist Scraper"}
    return BeautifulSoup(requests.get(baseURL, headers=headers).content)

def parseLine(line):
    """Parses a single line from the schedule and returns the output in a dict.

    @param  line    The line to parse.

    @return A dict object of the parsed data.
    """
    output = {}
    try:
        output['EnrlRestr'] = line[0:6].strip()
        output['SLN'] = line[7:13].strip()
        output['section'] = line[14]
        output['credit'] = line[15:23].strip()
        if "to be arranged" not in line[24:56]:
            output['meetings'] = {}
            output['meetings']['day'] = line[24:31].strip()
            output['meetings']['start'], output['meetings']['end'] = line[31:41].strip().split('-')
            output['meetings']['building'] = line[42:46:].strip()
            output['meetings']['room'] = line[47:56].strip()
        else:
            output['meetings'] = line[24:56].strip()
        output['professor'] = line[56:82].strip()
        output['status'] = line[83:90].strip()
        output['enrolled'] = line[89:95].strip()
        output['limit'] = line[96:100].strip()
        output['grades'] = line[101:107].strip()
        output['fee'] = line[108:114].strip()
        #output['other'] = line[115:].strip()
    except ValueError as e:
        print "==========================="
        print e
        print line
        print output
        print "==========================="
        sys.exit(1)
    return output

def getSchedule(year, quarter, major, campus = "S"):
    """Gets the schedule for the specified quarter, major and campus, parses
    it and returns a list of courses.

    @param year     The year to check. For example, 2014
    @param quarter  The quarter to check. Valid quarters are "SPR", "SUM",
    "AUT", and  "WIN".
    @param major    The major to check. Must be lower case.
    @param campus   The campus to check. Permitted values are "S" for Seattle
    campus (default), "B" for Bothell campus and "T" for Tacoma campus.

    @return A list of course dicts.
    """
    soup = getSchedulePage(year, quarter, major, campus)
    out= []
    currentCourse = {}
    for course in soup.find_all("table"):
        if "bgcolor" in course.attrs:
            if course.attrs['bgcolor'] == "#99ccff":
                links = course.find_all("a")
                courseid = links[0].get_text().strip().split(" ")
                currentCourse['courseName'] = links[1].get_text()
                currentCourse['major'] = courseid[0].strip()
                currentCourse['courseNumber'] = courseid[-1].strip()
        for section in course.find_all("pre"):
            if section.find("b") is None:
                line = parseLine(section.get_text())
                line.update(currentCourse)
                out.append(line)
    return out

def getMajors(year, quarter, campus="S"):
    """Gets a list of majors and their schedule for the specified year and
    quarter.

    @param  year    The year to get and parse. ie 2014
    @param  quarter The quarter to get and parse. Available options are "SPR",
    "SUM", "AUT" and "WIN"
    @param  campus  The campus to get the list of majors from. "S" for Seattle
    (default), "B" for Bothell or "T" for Tacoma.

    @return A dictionary of majors and their schedule for that quarter
    """

    output = {}
    url = "https://www.washington.edu/students/crscat"
    if campus == "B":
        url += "b/"
    elif campus == "T":
        url += "t/"
    elif campus != "S":
        raise InvalidCampus

    soup = BeautifulSoup(requests.get(url).content)
    for a in soup.find_all("a")[15:71]:
        if "href" in a.attrs:
            major = a.attrs['href'].split(".")[0]
            output[major] = getSchedule(year, quarter, major, campus)

    return output

class CampusNotSupported(Exception):
    pass

class InvalidCampus(Exception):
    pass

class InvalidQuarter(Exception):
    pass


if __name__ == "__main__":
    with open('data.txt', 'w') as outfile:
        json.dump(getMajors(2017, "WIN", "S"), outfile)

# vim: set textwidth=79
