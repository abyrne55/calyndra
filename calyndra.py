import argparse
import os
import re
from datetime import timedelta

import arrow
from dotenv import load_dotenv
from ics import Calendar

from util import events_in_month, total_waking_hours, waking_hours

load_dotenv()

TZ = os.getenv("TZ")
FMT = "ddd MMM DD hh:mma"

parser = argparse.ArgumentParser(
    description='Analyze your calendar to determine time spent on/between certain people or events'
)

parser.add_argument('event_regex', metavar="EVENT-REGEX", type=str,
                    help="regular expression used to select events by name")
parser.add_argument('ics_path', metavar="ICS-PATH", type=argparse.FileType('r'),
                    help="path to the ICS file being analyzed")
parser.add_argument('--months', metavar="'MONTH YEAR'", type=str, nargs="+", default=[arrow.now().format("MMMM YYYY")],
                    help="months to be analyzed, space-separated list of quoted strings like 'January 2024' (default: current month)")
parser.add_argument("-v", "--verbose", action="store_true", help="print each event being analyzed")
args = parser.parse_args()

event_name_re = re.compile(args.event_regex)

c = Calendar(args.ics_path.read())
for month in args.months:
    our_dates = [ev for ev in events_in_month(c, arrow.get(month, 'MMMM YYYY')) if event_name_re.search(ev.name)]
    if args.verbose:
        for ev in our_dates:
            print(f"{ev.name}: {ev.begin.to(TZ).format(FMT)} - {ev.end.to(TZ).format(FMT)} ({waking_hours(ev)})")

    print(str(total_waking_hours(our_dates) / timedelta(hours=1)) + " waking hours in " + month)
