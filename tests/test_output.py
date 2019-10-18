import unittest

from selective_linter.output import LintError


class TestOutput(unittest.TestCase):
    
    def test_lint_errors(self):
        error = ("/Full/Path To/SwiftFile.swift:29:1: "
                 "warning: Trailing Whitespace Violation: "
                 "Lines should not have trailing whitespace. (trailing_whitespace)")
        lint_error = LintError(error)
        self.assertEqual(lint_error.file, "/Full/Path To/SwiftFile.swift")
        self.assertEqual(lint_error.line, "29")
        self.assertEqual(lint_error.character, "1")
        self.assertEqual(lint_error.error_type, "warning")
        self.assertEqual(lint_error.description, "Trailing Whitespace Violation")
        self.assertEqual(lint_error.code, "Lines should not have trailing whitespace. (trailing_whitespace)")

    def test_str(self):
        error = ("/Full/Path To/SwiftFile.swift:29:1: "
                 "warning: Trailing Whitespace Violation: "
                 "Lines should not have trailing whitespace. (trailing_whitespace)")
        lint_error = LintError(error)
        self.assertEqual(lint_error.__str__(),
                         ("/Full/Path To/SwiftFile.swift:29: warning: "
                          "Trailing Whitespace Violation"))

if __name__ == '__main__':
    unittest.main()