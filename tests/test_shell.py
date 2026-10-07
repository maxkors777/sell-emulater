import unittest

from emulater import Shell, ShellError


class ShellTests(unittest.TestCase):
    def setUp(self):
        self.sh = Shell()

    def test_ls_without_args(self):
        self.assertEqual(self.sh.execute("ls"), "ls: args = []")

    def test_ls_with_args(self):
        self.assertEqual(self.sh.execute('ls -l "My Documents"'),
                         "ls: args = [<-l>, <My Documents>]")

    def test_cd_one_arg(self):
        self.assertEqual(self.sh.execute("cd /home"), "cd: args = [</home>]")

    def test_cd_without_args(self):
        self.assertEqual(self.sh.execute("cd"), "cd: args = []")

    def test_cd_too_many_args(self):
        with self.assertRaises(ShellError) as cm:
            self.sh.execute("cd a b")
        self.assertIn("too many arguments", str(cm.exception))

    def test_unknown_command(self):
        with self.assertRaises(ShellError) as cm:
            self.sh.execute("foo bar")
        self.assertIn("foo: command not found", str(cm.exception))

    def test_empty_line_is_ok(self):
        self.assertEqual(self.sh.execute("   "), "")
        self.assertFalse(self.sh.exit_requested)

    def test_exit(self):
        self.assertEqual(self.sh.execute("exit"), "")
        self.assertTrue(self.sh.exit_requested)

    def test_exit_with_args(self):
        with self.assertRaises(ShellError):
            self.sh.execute("exit now")
        self.assertFalse(self.sh.exit_requested)

    def test_parse_error_is_reported(self):
        with self.assertRaises(ShellError):
            self.sh.execute('ls "abc')


if __name__ == "__main__":
    unittest.main()
