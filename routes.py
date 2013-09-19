"""
Bottle routes
"""
import json
import os

from util import *
from bottle import abort, request, route, static_file

MAX_FILE_SIZE = 8192

# Static file paths
CLASSES = os.path.join(os.path.dirname(__file__), 'data/classes')
CSS = os.path.join(os.path.dirname(__file__), 'css')
IMG = os.path.join(os.path.dirname(__file__), 'img')
JS = os.path.join(os.path.dirname(__file__), 'js')
TEMPLATES = os.path.join(os.path.dirname(__file__), 'data/templates')

#
# Static file routes
#
@route('/testing/')
def automated_testing():
    """ Serves index file """
    return static_file('testing.html', '')

@route('/testing/data/classes/<filename>')
def css(filename):
    """ Serves all classes files """
    return static_file(filename, root=CLASSES)

@route('/testing/css/<filename>')
def css(filename):
    """ Serves all CSS files """
    return static_file(filename, root=CSS)

@route('/testing/img/<filename>')
def img(filename):
    """ Serves all image files """
    return static_file(filename, root=IMG)

@route('/testing/js/<filename>')
def js(filename):
    """ Serves all JS files """
    return static_file(filename, root=JS)

@route('/testing/data/templates/<filename>')
def css(filename):
    """ Serves all template files """
    return static_file(filename, root=TEMPLATES)

#
# Dynamic routes
#
@route('/testing/json/templates/')
def templates():
    """ Returns all JSON templates. """

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

@route('/testing/add-template/', method="POST")
def add_template():
    """ Convert template into JSON and write to file. """
    try:
        template_name = request.forms.get('template-name') or None          # Required
        required_filenames = request.forms.get('required-files') or None    # Required
        key_file = request.files.get('output-key') or None                  # Required
        script_file = request.files.get('input-script') or None
        diff_file = request.files.get('diff-file') or None
        review_params = request.forms.get('review-params') or None

        # This is really sloppy because I don't know how to pass along an array
        # of files through Bottle. If this is possible, this could be a lot
        # cleaner.
        instructor_files_count = int(request.forms.get('instructor-files-count'))
        instructor_files = []
        for x in range(instructor_files_count):
            try:
                instructor_files.append(request.files.get('instructor-files' + str(x)))
            except:
                break
    except:
        raise

    # Make sure required pieces are present
    if required_filenames == None or key_file == None or template_name == None:
        raise Exception(required_filenames, key_file, template_name)

    # Rename files (except instructor files) for consistency
    # This way any previous files will be overwritten if the template is being edited
    key_file.filename = 'output-key'
    if script_file: script_file.filename = 'input-script'
    if diff_file: diff_file.filename = 'diff'

    # If necessary, create template directory
    save_path = TEMPLATES + '/' + template_name
    print save_path
    try:
        if not os.path.exists(save_path):
            os.makedirs(save_path)
    except OSError:
        # Used to prevent race condition between path.exists and os.makedirs.
        # Unfortunately, this catches more than just that error, so it's not
        # perfect.
        pass

    # Construct a list of files to save
    save_files = [key_file, script_file, diff_file]
    for f in instructor_files:
        save_files.append(f)

    # Save each file
    for f in save_files:
        if f != None:
            file_path = "{}/{}".format(save_path, f.filename)
            print file_path
            open_file = open(file_path, 'w')            # Will overwrite existing files of same name
            open_file.write(f.file.read(MAX_FILE_SIZE)) # Will stop reading at MAX_FILE_SIZE bytes
            open_file.close()
