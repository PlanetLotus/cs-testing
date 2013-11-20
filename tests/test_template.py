import unittest
import os, sys
import shutil

# This isn't the Python way, but I couldn't figure out another way
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import routes

CLASSES = os.path.join(os.path.dirname(__file__), '../data/classes/')
EXEC = os.path.join(os.path.dirname(__file__), '../data/exec/')
TEMPLATES = os.path.join(os.path.dirname(__file__), '../data/templates/')

class TestTemplate(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Create templates
        template1 = {
            'template_name': 'unittest_template1',
            'required_filenames': ['testreq1', 'testreq2'],
            'key_file': 'output-key',
            'script_file': 'input-script',
            'diff_file': 'diff',
            'instructor_files': ['instructor_files1.txt', 'instructor_files2.txt'],
            'review_params': [True, True, True]
        }

        # Create template directories
        if not os.path.exists(TEMPLATES + template1['template_name']):
            os.makedirs(TEMPLATES + template1['template_name'])

        # Create necessary files
        key_file1 = open(TEMPLATES + template1['template_name'] + '/output-key', 'w')
        key_file1.write('test1')
        key_file1.close()
        script_file1 = open(TEMPLATES + template1['template_name'] + '/input-script', 'w')
        script_file1.write('print "test1"')
        script_file1.close()
        instructor_file1 = open (TEMPLATES + template1['template_name'] + '/instructor_files1.txt', 'w')
        instructor_file1.write('instructor file1 test')
        instructor_file1.close()
        instructor_file2 = open (TEMPLATES + template1['template_name'] + '/instructor_files2.txt', 'w')
        instructor_file2.write('instructor file1 test')
        instructor_file2.close()

    @classmethod
    def tearDownClass(cls):
        # Delete template directories
        shutil.rmtree(TEMPLATES + 'unittest_template1')

    def test_add_template(self):
        # Use these three functions to test various pieces of the add_template route
        self.assertEqual(0, 0)
        self.assertTrue(1==1)
        with self.assertRaises(ZeroDivisionError):
            this_will_break = 5/0
