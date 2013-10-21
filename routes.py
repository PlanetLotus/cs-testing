"""
Bottle routes
"""
import simplejson as json
import os

from util import *
from bottle import abort, request, route, static_file

MAX_FILE_SIZE = 8192

# Static file paths
CLASSES = os.path.join(os.path.dirname(__file__), 'data/classes/')
CSS = os.path.join(os.path.dirname(__file__), 'css')
EXEC = os.path.join(os.path.dirname(__file__), 'data/exec/')
FONTS = os.path.join(os.path.dirname(__file__), 'fonts')
IMG = os.path.join(os.path.dirname(__file__), 'img')
JS = os.path.join(os.path.dirname(__file__), 'js')
TEMPLATES = os.path.join(os.path.dirname(__file__), 'data/templates/')

#
# Static file routes
#
@route('/testing/')
def automated_testing():
    """ Serves index file """
    return static_file('testing.html', '')

@route('/testing/data/classes/<filename>')
def classes(filename):
    """ Serves all classes files """
    return static_file(filename, root=CLASSES)

@route('/testing/css/<filename>')
def css(filename):
    """ Serves all CSS files """
    return static_file(filename, root=CSS)

@route('/testing/fonts/<filename>')
def fonts(filename):
    """ Serves all fonts """
    return static_file(filename, root=FONTS)

@route('/testing/img/<filename>')
def img(filename):
    """ Serves all image files """
    return static_file(filename, root=IMG)

@route('/testing/js/<filename>')
def js(filename):
    """ Serves all JS files """
    return static_file(filename, root=JS)

@route('/testing/data/templates/<filename>')
def tpls(filename):
    """ Serves all template files """
    return static_file(filename, root=TEMPLATES)

#
# Dynamic routes
#
@route('/testing/json/templates/')
def templates():
    """ Returns all JSON templates. """
    return get_templates()

@route('/testing/add-template/', method="POST")
def add_template():
    """ Convert template into JSON and write to file. """
    try:
        template_name = request.forms.get('template-name') or None                  # Required
        required_filenames = request.forms.get('required-files').split(',') or None # Required
        key_file = request.files.get('output-key') or None                          # Required
        script_file = request.files.get('input-script') or None
        diff_file = request.files.get('diff-file') or None

        var_check = request.forms.get('var-check') or ''
        comment_check = request.forms.get('comment-check') or ''
        indent_check = request.forms.get('indent-check') or ''

        # This is really sloppy because I don't know how to pass along an array
        # of files through Bottle. If this is possible, this could be a lot
        # cleaner.
        instructor_files_count = int(request.forms.get('instructor-files-count'))
        instructor_files = []
        instructor_files_names = []
        for x in range(instructor_files_count):
            try:
                this_file = request.files.get('instructor-files' + str(x))
                instructor_files.append(this_file)
                instructor_files_names.append(this_file.filename)
            except:
                break
    except:
        raise

    # Package code review parameters into a list
    review_params = {}
    review_params['var_check'] = (var_check == 'true')
    review_params['comment_check'] = (comment_check == 'true')
    review_params['indent_check'] = (indent_check == 'true')

    # Make sure required pieces are present
    if required_filenames == None or key_file == None or template_name == None:
        raise Exception(required_filenames, key_file, template_name)

    # Make sure template name doesn't already exist
    # This might be necessary later when deciding if we're updating a template
    # rather than creating a new one
    #templates = json.loads(get_templates())
    #for t in templates:
    #    if t['filename'] == template_name:
    #        raise Exception(template_name)

    # Rename files (except instructor files) for consistency
    # This way any previous files will be overwritten if the template is being edited
    key_file.filename = 'output-key'
    if script_file: script_file.filename = 'input-script'
    if diff_file: diff_file.filename = 'diff'

    # If necessary, create template directory
    save_path = TEMPLATES + template_name
    print save_path
    try:
        if not os.path.exists(save_path):
            os.makedirs(save_path)
    except OSError:
        # Used to prevent race condition between path.exists and os.makedirs.
        # Unfortunately, this catches more than just that error, so it's not
        # perfect.
        pass

    # Construct and save the JSON template
    new_template = {}
    new_template['filename'] = template_name
    new_template['required_filenames'] = required_filenames
    new_template['key_file'] = key_file.filename

    if script_file: new_template['script_file'] = script_file.filename
    else: new_template['script_file'] = ''

    if diff_file: new_template['diff_file'] = diff_file.filename
    else: new_template['diff_file'] = ''

    new_template['instructor_files'] = instructor_files_names
    new_template['review_params'] = review_params
    template_file = open(save_path + '/' + template_name + '.json', 'w')
    json.dump(new_template, template_file)
    template_file.close()

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

@route('/testing/json/students/')
def students():
    """ Returns list of classes and student names. """

    # There's probably a fancier way of doing this same thing with one call of
    # os.walk instead, but this is probably more readable

    # Build list of classes
    classes = {}
    for dirname in os.listdir(CLASSES):
        if os.path.isdir(os.path.join(CLASSES, dirname)):
            classes[dirname] = []

    # From list of classes, build list of students
    # Could put this inside the loop above, but this looks cleaner
    for c in classes:
        for dirname in os.listdir(CLASSES + c):
            if os.path.isdir(os.path.join(CLASSES, c, dirname)):
                classes[c].append(dirname)

    # 'classes' is a class-to-students mapping
    return to_json(classes)

@route('/testing/run-program/', method="POST")
def run_program():
    """ Runs a student's program and returns the results. """
    try:
        template = request.json['template']
        student_names = request.json['students']
    except:
        raise

    # Keep local reference to template attributes
    # Shorter, and easier to update if the attribute names get modified
    print template
    required = template['required_filenames']
    review = template['review_params']
    instructor_filenames = template['instructor_files']
    diff_filename = template['diff_file']
    key_filename = template['key_file']
    script_filename = template['script_file']
    required_filenames = template['required_filenames']

    results = []    # One entry per student
    # Loop through each student, compiling their results
    for name in student_names:
        # Check for required files
        student_files = os.listdir(CLASSES + name)
        if not all(x in student_files for x in required_filenames):
            raise Exception(required_filenames)

        # Copy student files to exec directory

        # Copy instructor files to exec dir
        # Overwrites student files of same name

    return results
