from datetime import date
import requests, json

def parse_date(d: date | str) -> date:
    if type(d) is date:
        return d

    split = d.split("/")
    return date(
        month=int(split[0]),
        day=int(split[1]),
        year=int(split[2])
    )

class Edition:
    def __init__(self, name: str, start: date | str, end: date | str):
        self.name = name
        self.start = parse_date(start)
        self.end = parse_date(end)

    def days_difference(self):
        now = date.today()

        if now < self.start:
            return (self.start - now).days

        if now > self.end:
            return (self.end - now).days

        return 0

    def format_text(self):
        diff = self.days_difference()

        if diff < 0:
            return "It ended " + str(-diff) + " days ago"
        if diff > 0:
            return "It starts in " + str(diff) + " days"
        return "It is now!"

def load_edition(url):
    r = requests.get(url)
    j = json.loads(r.text)
    return Edition(j['edition'], j['start'], j['end'])