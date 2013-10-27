import datetime
import simplejson as json
import os
import subprocess

from bottle import response

MAX_FILE_SIZE = 8192

TEMPLATES = os.path.join(os.path.dirname(__file__), 'data/templates/')
OUTPUT = os.path.join(os.path.dirname(__file__), 'data/output/')
EXEC = os.path.join(os.path.dirname(__file__), 'data/exec/')

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

def exec_py(filepath, input_script_path=None):
    """ Runs a Python program located at `filepath`.  Uses `input_script_path`
    as stdin if present. Assumes `input_script_path` is the full path. """

    # Set up command to be run
    cmd = ['python', filepath]

    # If script exists, open file
    script = None
    if input_script_path:
        script = open(input_script_path, 'r')

    # Run program and save output
    output = ''
    error = ''
    try:
        output = subprocess.check_output(cmd, stdin=script, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError, e:
        # Program returned an error. Save the error.
        error = e.output

    # Close file
    if script: script.close()

    # Return output and error text
    return output, error

def exec_c():
    pass

def exec_cpp():
    pass
