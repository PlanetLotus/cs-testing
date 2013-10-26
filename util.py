import datetime
import simplejson as json
import os
import subprocess

from bottle import response

MAX_FILE_SIZE = 8192

TEMPLATES = os.path.join(os.path.dirname(__file__), 'data/templates/')
OUTPUT = os.path.join(os.path.dirname(__file__), 'data/output/')

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

def exec_py(filepath):
    """ Runs a Python program located at `filepath`. """

    # Set up command to be run
    cmd = ['python', filepath]

    # Write to output file. Assumes OUTPUT exists.
    with open(OUTPUT + 'output.txt', 'w') as out, open(OUTPUT + 'error.txt', 'w') as err:
        return_code = subprocess.call(cmd, stdout=out, stderr=err)

    # Return output and error text
    output = ''
    errors = ''
    with open(OUTPUT + 'output.txt', 'r') as out, open(OUTPUT + 'error.txt', 'r') as err:
        output = out.read(MAX_FILE_SIZE)
        errors = err.read(MAX_FILE_SIZE)

    return output, errors

def exec_c():
    pass

def exec_cpp():
    pass
