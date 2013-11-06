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

def update_template(old, new):
    """Update attributes of a template that already exists."""

    # Update template attributes
    new_template = {}
    new_template['review_params'] = {}
    new_template['filename'] = old['filename']

    if not new['required_filenames']:
        return False    # Error

    new_template['required_filenames'] = new['required_filenames']
    new_template['review_params'] = new['review_params']
    new_template['key_file'] = 'output-key'

    if new['script_file']: new_template['script_file'] = 'input-script'
    else: new_template['script_file'] = old['script_file']

    if new['diff_file']: new_template['diff_file'] = 'diff'
    else: new_template['diff_file'] = old['diff_file']

    if new['instructor_files_names']: new_template['instructor_files'] = new['instructor_files_names']
    else: new_template['instructor_files'] = old['instructor_files']

    save_path = TEMPLATES + new_template['filename']
    template_file = open(save_path + '/' + new_template['filename'] + '.json', 'w')
    json.dump(new_template, template_file)
    template_file.close()

    # Add/overwrite new files
    save_files = []

    if new['key_file']:
        new['key_file'].filename = 'output-key'
        save_files.append(new['key_file'])

    if new['script_file']:
        new['script_file'].filename = 'input-script'
        save_files.append(new['script_file'])

    if new['diff_file']:
        new['diff_file'].filename = 'diff'
        save_files.append(new['diff_file'])

    if new['instructor_files']:
        # TODO: Delete old instructor files!
        for f in new['instructor_files']:
            save_files.append(f)

    # Save each file
    for f in save_files:
        if f != None:
            file_path = "{}/{}".format(save_path, f.filename)
            print file_path
            open_file = open(file_path, 'w')            # Will overwrite existing files of same name
            open_file.write(f.file.read(MAX_FILE_SIZE)) # Will stop reading at MAX_FILE_SIZE bytes
            open_file.close()

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
