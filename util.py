import datetime
import simplejson as json
import os

from bottle import response

TEMPLATES = os.path.join(os.path.dirname(__file__), 'data/templates/')

# Convert datetimes to ISO format before casting to JSON
DATETIME_HANDLER = lambda x: x.strftime('%A, %d. %B %Y %I:%M%p') \
                    if isinstance(x, datetime.datetime) else None

def to_json(results):
    """Change content type and cast results to JSON"""
    response.content_type = 'application/json'
    return json.dumps(results, default=DATETIME_HANDLER)

def get_templates():
    """Returns a list of all templates."""
    templates = []
    for root, dirs, files in os.walk(TEMPLATES):
        for f in files:
            if f.endswith('.json'):
                # Open file
                data_file = open(os.path.join(root, f))

                # Append JSON to templates
                templates.append(json.load(data_file))

                # Close file
                data_file.close()
    return to_json(templates)
