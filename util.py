import datetime
import simplejson as json

from bottle import response

# Convert datetimes to ISO format before casting to JSON
DATETIME_HANDLER = lambda x: x.strftime('%A, %d. %B %Y %I:%M%p') \
                    if isinstance(x, datetime.datetime) else None

def to_json(results):
    """Change content type and cast results to JSON"""
    response.content_type = 'application/json'
    return json.dumps(results, default=DATETIME_HANDLER)
