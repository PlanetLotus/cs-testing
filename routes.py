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

@route('/testing/json/add-template/', method="POST")
def add_template():
    """ Convert template into JSON and write to file. """
    try:
        required_filenames = request.forms.get('required-files') or None    # Required
        key_file = request.files.get('output-key') or None                         # Required
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

    # Make sure required files are present
    if required_filenames == None or key_file == None:
        raise Exception(required_filenames, key_file)

    print instructor_files
    print request.files
    return

    # Validate file uploads and input
    # This isn't ideal. It should limit the file size before just saving it.

    # If necessary, create template directory
    try:
        if not os.path.exists(TEMPLATES + '/' + template_name):
            os.makedirs(TEMPLATES + '/' + template_name)
    except OSError:
        # Used to prevent race condition between path.exists and os.makedirs.
        # Unfortunately, this catches more than just that error, so it's not
        # perfect.
        pass
