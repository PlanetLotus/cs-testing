import datetime
import simplejson as json
import os
import subprocess
import shutil

from bottle import response

# Static file paths
CLASSES = os.path.join(os.path.dirname(__file__), 'data/classes/')
CSS = os.path.join(os.path.dirname(__file__), 'css')
EXEC = os.path.join(os.path.dirname(__file__), 'data/exec/')
FONTS = os.path.join(os.path.dirname(__file__), 'fonts')
IMG = os.path.join(os.path.dirname(__file__), 'img')
JS = os.path.join(os.path.dirname(__file__), 'js')
TEMPLATES = os.path.join(os.path.dirname(__file__), 'data/templates/')

MAX_FILE_SIZE = 8192

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

def prepare_exec(student_name, template_name, instructor_filenames):
    """ A helper that makes sure the exec dir is present and then copies
    student and instructor files to the dir. """

    # Make sure exec directory exists
    try:
        if not os.path.exists(EXEC):
            os.makedirs(EXEC)
    except OSError:
        pass

    # Copy student files to exec directory
    student_files = os.listdir(CLASSES + student_name)
    for f in student_files:
        full_filename = os.path.join(CLASSES, student_name, f)
        if (os.path.isfile(full_filename)):
            shutil.copy2(full_filename, EXEC)

    # Copy instructor files to exec dir
    # Overwrites student files of same name
    for f in instructor_filenames:
        full_filename = os.path.join(TEMPLATES + template_name + '/' + f)
        if (os.path.isfile(full_filename)):
            shutil.copy2(full_filename, EXEC)

def get_files(template, student_name):
    """ Returns the contents of student's code, instructor's code, diff file,
    and key file. """

    template_name = template['filename']

    student_file_contents = {}      # Filename : contents
    instructor_file_contents = {}   # Filename : contents
    diff_contents = ''
    key_contents = ''

    ## Might cause issues if object files are in the directory
    ## e.g. .pyc, .o
    ## TODO: Find a way to not include non-ASCII or non-Unicode files, NOT
    ## based on file extension

    # Student files
    student_files = os.listdir(CLASSES + student_name)
    for f in student_files:
        full_filename = os.path.join(CLASSES, student_name, f)
        if os.path.isfile(full_filename) and not f.startswith('.'):
            with open(full_filename, 'r') as open_file:
                contents = open_file.read(MAX_FILE_SIZE)
                student_file_contents[f] = contents

    # Instructor files
    instructor_filenames = template['instructor_files']
    for f in instructor_filenames:
        full_filename = os.path.join(TEMPLATES + template_name + '/' + f)
        if os.path.isfile(full_filename) and not f.startswith('.'):
            with open(full_filename, 'r') as open_file:
                contents = open_file.read(MAX_FILE_SIZE)
                instructor_file_contents[f] = contents

    # Diff file
    if template['diff_file']:
        full_filename = os.path.join(TEMPLATES + template_name + '/' + template['diff_file'])
        if os.path.isfile(full_filename) and not f.startswith('.'):
            with open(full_filename, 'r') as open_file:
                contents = open_file.read(MAX_FILE_SIZE)
                diff_contents = contents

    # Key file
    if template['key_file']:
        full_filename = os.path.join(TEMPLATES + template_name + '/' + template['key_file'])
        if os.path.isfile(full_filename) and not f.startswith('.'):
            with open(full_filename, 'r') as open_file:
                contents = open_file.read(MAX_FILE_SIZE)
                key_contents = contents

    return student_file_contents, instructor_file_contents, diff_contents, key_contents

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
