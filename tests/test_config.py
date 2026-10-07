import os
import subprocess
import sys
import tempfile
import unittest

import emulater
from emulater import Config, parse_args

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EMULATOR = os.path.join(ROOT, "emulater.py")


def run_cli(*args):
    """Запускает эмулятор как процесс; возвращает (код выхода, stderr)."""
    p = subprocess.run([sys.executable, EMULATOR] + list(args),
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                       universal_newlines=True, timeout=30)
    return p.returncode, p.stderr


class ConfigTests(unittest.TestCase):
    def test_default_vfs_name(self):
        self.assertEqual(Config().vfs_name, "vfs")

    def test_vfs_name_from_path(self):
        self.assertEqual(Config(vfs=os.path.join("a", "myvfs")).vfs_name, "myvfs")

    def test_debug_string_not_set(self):
        s = Config().debug_string()
        self.assertIn("[debug] vfs", s)
        self.assertIn("[debug] script", s)
        self.assertEqual(s.count("<not set>"), 2)

    def test_debug_string_shows_values(self):
        s = Config(vfs="myvfs", script="start.txt").debug_string()
        self.assertIn("myvfs", s)
        self.assertIn("start.txt", s)

    def test_parse_args_ok(self):
        with tempfile.TemporaryDirectory() as d:
            cfg = parse_args(["--vfs", d, "--script", "start.txt"])
        self.assertEqual(cfg.script, "start.txt")
        self.assertEqual(cfg.vfs, d)

    def test_parse_args_empty(self):
        cfg = parse_args([])
        self.assertIsNone(cfg.vfs)
        self.assertIsNone(cfg.script)


class CommandLineErrorTests(unittest.TestCase):
    def test_unknown_option(self):
        code, err = run_cli("--bogus")
        self.assertEqual(code, 2)
        self.assertIn("error:", err)

    def test_option_without_value(self):
        code, _ = run_cli("--vfs")
        self.assertEqual(code, 2)

    def test_missing_vfs(self):
        code, err = run_cli("--vfs", os.path.join(ROOT, "no_such_vfs_dir"))
        self.assertEqual(code, 2)
        self.assertIn("does not exist", err)


if __name__ == "__main__":
    unittest.main()
