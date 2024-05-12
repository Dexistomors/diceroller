import unittest
import pathlib

def run_tests(tests_path):
    suites = unittest.TestLoader().discover(tests_path, pattern='test_*.py')
    unittest.TestSuite((suites))
    runner = unittest.TextTestRunner()
    runner.run(suites)

def main():
    tests_path = pathlib.Path('tests')
    print("\nTesting {}...".format(tests_path.absolute()))
    run_tests(tests_path)

if __name__ == '__main__':
    main()