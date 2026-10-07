#!/usr/bin/env python3
"""
Эмулятор оболочки ОС (этапы 1-2) в одном файле, GUI на tkinter.

Запуск:  python emulator.py [--vfs <путь>] [--script <путь>]
"""
import argparse
import os
import sys
import tkinter as tk
from tkinter import scrolledtext


# ---------- Ошибка выполнения ----------
class ShellError(Exception):
    pass


# ---------- Парсер: "..." '...' и \-экранирование ----------
def parse(line):
    tokens, cur = [], []
    in_token = False          # отличает пустой аргумент "" от отсутствия аргумента
    quote = None
    i, n = 0, len(line)
    while i < n:
        c = line[i]
        if quote:
            if c == quote:
                quote = None
            elif c == "\\" and quote == '"' and i + 1 < n and line[i + 1] in ('"', "\\"):
                i += 1
                cur.append(line[i])
            else:
                cur.append(c)
        elif c in ('"', "'"):
            quote = c
            in_token = True
        elif c == "\\" and i + 1 < n:
            i += 1
            cur.append(line[i])
            in_token = True
        elif c.isspace():
            if in_token:
                tokens.append("".join(cur))
                cur, in_token = [], False
        else:
            cur.append(c)
            in_token = True
        i += 1
    if quote:
        raise ShellError("parse error: unclosed quote " + quote)
    if in_token:
        tokens.append("".join(cur))
    return tokens


# ---------- Ядро: выполнение команд ----------
class Shell:
    def __init__(self):
        self.exit_requested = False

    @staticmethod
    def _stub(name, args):
        return "%s: args = [%s]" % (name, ", ".join("<%s>" % a for a in args))

    def execute(self, line):
        """Возвращает вывод команды или бросает ShellError."""
        tokens = parse(line)
        if not tokens:
            return ""
        cmd, args = tokens[0], tokens[1:]
        if cmd == "ls":
            return self._stub("ls", args)
        if cmd == "cd":
            if len(args) > 1:
                raise ShellError("cd: too many arguments")
            return self._stub("cd", args)
        if cmd == "exit":
            if args:
                raise ShellError("exit: too many arguments")
            self.exit_requested = True
            return ""
        raise ShellError("%s: command not found" % cmd)


# ---------- Параметры командной строки ----------
class Config:
    def __init__(self, vfs=None, script=None):
        self.vfs = vfs
        self.script = script

    @property
    def vfs_name(self):
        if not self.vfs:
            return "vfs"
        return os.path.basename(os.path.abspath(self.vfs)) or "vfs"

    def debug_string(self):
        vfs = os.path.abspath(self.vfs) if self.vfs else "<not set>"
        script = os.path.abspath(self.script) if self.script else "<not set>"
        return "[debug] vfs    = %s\n[debug] script = %s" % (vfs, script)


class _Parser(argparse.ArgumentParser):
    def error(self, message):            # единый формат ошибки, код выхода 2
        sys.stderr.write("error: %s\n" % message)
        sys.exit(2)


def parse_args(argv):
    p = _Parser(prog="emulator.py", description="Shell emulator")
    p.add_argument("--vfs", metavar="PATH", help="путь к физическому расположению VFS")
    p.add_argument("--script", metavar="PATH", help="путь к стартовому скрипту")
    ns = p.parse_args(argv)
    if ns.vfs is not None and not os.path.exists(ns.vfs):
        sys.stderr.write("error: VFS path does not exist: %s\n" % ns.vfs)
        sys.exit(2)
    return Config(ns.vfs, ns.script)


# ---------- GUI ----------
class EmulatorWindow:
    def __init__(self, root, config):
        self.root = root
        self.config = config
        self.shell = Shell()
        self.prompt = "Ввод:"
        self.history, self.hpos = [], 0

        root.title("Emulator — [%s]" % config.vfs_name)
        root.geometry("800x500")

        self.output = scrolledtext.ScrolledText(
            root, state="disabled", wrap="word", bg="black", fg="#cccccc",
            font=("Courier", 12), insertbackground="white")
        self.output.pack(fill="both", expand=True)

        bottom = tk.Frame(root, bg="black")
        bottom.pack(fill="x")
        tk.Label(bottom, text=" " + self.prompt, bg="black", fg="#55ff55",
                 font=("Courier", 12)).pack(side="left")
        self.entry = tk.Entry(bottom, bg="black", fg="white", insertbackground="white",
                              font=("Courier", 12), relief="flat")
        self.entry.pack(side="left", fill="x", expand=True)
        self.entry.focus_set()
        self.entry.bind("<Return>", self.on_enter)
        self.entry.bind("<Up>", self.on_up)
        self.entry.bind("<Down>", self.on_down)

    def println(self, text):
        self.output.configure(state="normal")
        self.output.insert("end", text + "\n")
        self.output.configure(state="disabled")
        self.output.see("end")

    def run_line(self, line):
        """Выполняет строку; True, если без ошибки."""
        self.println(self.prompt + line)
        ok = True
        try:
            out = self.shell.execute(line)
            if out:
                self.println(out)
        except ShellError as e:
            self.println("error: %s" % e)
            ok = False
        if self.shell.exit_requested:
            self.root.destroy()
        return ok

    def on_enter(self, _event):
        line = self.entry.get()
        self.entry.delete(0, "end")
        if line.strip():
            self.history.append(line)
        self.hpos = len(self.history)
        self.run_line(line)

    def on_up(self, _event):
        if self.hpos > 0:
            self.hpos -= 1
            self.entry.delete(0, "end")
            self.entry.insert(0, self.history[self.hpos])

    def on_down(self, _event):
        self.entry.delete(0, "end")
        if self.hpos < len(self.history) - 1:
            self.hpos += 1
            self.entry.insert(0, self.history[self.hpos])
        else:
            self.hpos = len(self.history)

    def show_debug(self):
        self.println(self.config.debug_string())

    def run_startup_script(self):
        """Ввод и вывод видны; остановка на первой ошибке."""
        path = self.config.script
        if not path:
            return
        try:
            with open(path, encoding="utf-8") as f:
                lines = f.read().splitlines()
        except OSError as e:
            self.println("script error: cannot read '%s': %s" % (path, e))
            return
        self.println("--- running startup script: %s ---" % path)
        for num, line in enumerate(lines, 1):
            t = line.strip()
            if not t or t.startswith("#"):
                continue
            if not self.run_line(line):
                self.println("script error: execution stopped at line %d: %s" % (num, line))
                return
            if self.shell.exit_requested:
                return
        self.println("--- startup script finished ---")


def main():
    config = parse_args(sys.argv[1:])
    print(config.debug_string())          # отладочный вывод параметров
    root = tk.Tk()
    win = EmulatorWindow(root, config)
    win.show_debug()
    root.after(100, win.run_startup_script)
    root.mainloop()


if __name__ == "__main__":
    main()
