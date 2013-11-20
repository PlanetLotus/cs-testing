import sys, os, unittest

def run_text():
    """
    Runs the tests using the standard TextTestRunner.
    """
    path = os.path.dirname(__file__)
    tests = unittest.defaultTestLoader.discover(path)
    unittest.TextTestRunner().run(tests)

if __name__ == "__main__":
    sys.path.insert(0, os.path.dirname(__file__))
    run_text()
