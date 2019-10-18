import os
import shutil
import time
import unittest

from selective_linter.linter import SwiftLint

# This code has a lint error, but only if .swiftlint.yml is loaded
file_1 = """class TestClass {
    let value = [1, 2, 3].filter { $0 }.first { $0 == 3 }
}
"""

# This code has two lint errors
file_2 = """class TestClassTwo {


    let aDict: [String: Int] = ["Some":4]
}
"""

# This code doesn't has a lint error
file_3 = """enum TestClassThree {
    case noError(someConst:Int)
}
"""


class TestSwiftlint(unittest.TestCase):
    
    initial_dir = None

    def setUp(self):
        self.initial_dir = os.getcwd()
        try:
            os.mkdir('temp')
        except FileExistsError:
            shutil.rmtree('temp')
        os.chdir('temp')
        with open('test1.swift', 'w+') as swift_file:
            swift_file.write(file_1)
        with open('test2.swift', 'w+') as swift_file:
            swift_file.write(file_2)
        with open('test3.swift', 'w+') as swift_file:
            swift_file.write(file_3)

    def tearDown(self):
        os.chdir(self.initial_dir)
        shutil.rmtree('temp')

    def test_loads_custom_swiftlint_yml(self):
        # test1.swift doesn't have any lint errors if we ignore first_where
        test_file = os.path.join(os.getcwd(), 'test1.swift') 
        linter = SwiftLint(files=[test_file])
        self.assertEqual(linter.lint_errors, {})
        
        # write swiftlint.yml
        swiftlint_path = os.path.join(os.getcwd(), '.swiftlint.yml')
        with open(swiftlint_path, 'w+') as swiftlint_yml:
            swiftlint_yml.write("opt_in_rules:\n  - first_where")
        
        # Now, test1.swift should have a lint error
        linter = SwiftLint(files=[test_file])
        self.assertEqual(len(linter.lint_errors[test_file]), 1)
        os.remove('.swiftlint.yml')

    def test_lint_several_files(self):
        all_files = [os.path.join(os.getcwd(), file) 
                     for file in ['test1.swift', 'test2.swift', 'test3.swift']]
        error_files = all_files[1:]
        linter = SwiftLint(files=all_files)
        # Test that errors are recognized in files 2 and 3 but not 1.
        # Also test how many errors
        self.assertSetEqual(set(linter.lint_errors.keys()), set(error_files))
        self.assertEqual(len(linter.lint_errors[error_files[0]]), 2)
        self.assertEqual(len(linter.lint_errors[error_files[1]]), 1)


if __name__ == '__main__':
    unittest.main()
