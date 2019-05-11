"""
Assumptions made in this script:
1) The port authority will only list events for the current year.
    This is the historical pattern. If this assumption becomes false
    at some point, the event dates would become untrustworthy.
"""
# proof-of-concept to prepare the dynamic portions of event data structures
import re                           # regular expressions
from html.parser import HTMLParser  # clean up HTML

# returns true if text contains a string of the form "may 17"
# used to read one row of the event html table and determine if that row
# is describing and event
def _contains_month_and_day(text):
    regular_expression = "(january|february|march|april|may|june|july|august|september|october|november|december) \d+"
    return re.search(regular_expression, text.lower()) != None

# Helper class for strip_tags
class MLStripper(HTMLParser):
    # original author: eloff
    # source: https://stackoverflow.com/questions/753052/strip-html-from-strings-in-python
    def __init__(self):
        self.reset()
        self.strict = False
        self.convert_charrefs = True
        self.fed = []

    def handle_data(self, d):
        self.fed.append(d)

    def get_data(self):
        return ''.join(self.fed)

# Accepts an html string, returns a string without any html tags.
# For example, strip_tags("<h1>foo</h1>") will return just "foo".
def strip_tags(html):
    # original author: eloff
    # source: https://stackoverflow.com/questions/753052/strip-html-from-strings-in-python
    s = MLStripper()
    s.feed(html)
    return s.get_data()

# accepts an html table cell and returns the text held within
def get_cell_value(cell):
    cleaned_cell = strip_tags(cell)             # remove html tags
    cell_value = re.sub('\n','',cleaned_cell) # remove line breaks
    return cell_value

file = open('raw_data.html', 'r') # cached html blob
raw_text = file.read()
raw_rows = raw_text.split("<tr>")
cleaned_rows = []
for row in raw_rows:
    if _contains_month_and_day(row):
        raw_row = row.split("/td>")
        title = get_cell_value(raw_row[0])
        time = get_cell_value(raw_row[1])
        date = get_cell_value(raw_row[2])
        cleaned_row = [title,time,date]
        cleaned_rows.append(cleaned_row)

print(str(len(cleaned_rows)) + " events found:")
# print event information
for row in cleaned_rows:
    print("The " + row[0] + " will meet on " + row[2] + " at " + row[1])
