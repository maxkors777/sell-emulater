import unittest

from emulater import parse, ShellError


class ParserTests(unittest.TestCase):
    def test_plain_words(self):
        self.assertEqual(parse("ls -l /home"), ["ls", "-l", "/home"])

    def test_extra_spaces_and_tabs(self):
        self.assertEqual(parse("  ls \t a   b  "), ["ls", "a", "b"])

    def test_empty_line(self):
        self.assertEqual(parse(""), [])
        self.assertEqual(parse("   "), [])

    def test_double_quotes(self):
        self.assertEqual(parse('cd "My Documents"'), ["cd", "My Documents"])

    def test_single_quotes(self):
        self.assertEqual(parse("ls 'a b' c"), ["ls", "a b", "c"])

    def test_empty_argument(self):
        self.assertEqual(parse('ls ""'), ["ls", ""])

    def test_quote_inside_word(self):
        self.assertEqual(parse('a"b c"d'), ["ab cd"])

    def test_escaped_space(self):
        self.assertEqual(parse("ls a\\ b"), ["ls", "a b"])

    def test_escaped_quote_in_double_quotes(self):
        self.assertEqual(parse('ls "a\\"b"'), ["ls", 'a"b'])

    def test_other_quote_kept_inside_quotes(self):
        self.assertEqual(parse("""ls "it's" 'say "hi"'"""), ["ls", "it's", 'say "hi"'])

    def test_unclosed_double_quote(self):
        with self.assertRaises(ShellError) as cm:
            parse('ls "abc')
        self.assertIn("unclosed quote", str(cm.exception))

    def test_unclosed_single_quote(self):
        with self.assertRaises(ShellError):
            parse("ls 'abc")


if __name__ == "__main__":
    unittest.main()
