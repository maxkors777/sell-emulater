"""Эмулятор оболочки ОС. Этап 1: REPL."""
import tkinter as tk
from tkinter import scrolledtext


class ShellError(Exception):
    pass


def parse(line):
    tokens, cur = [], []
    in_token = False
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


class Shell:
    def __init__(self):
        self.exit_requested = False

    @staticmethod
    def _stub(name, args):
        return "%s: args = [%s]" % (name, ", ".join("<%s>" % a for a in args))

    def execute(self, line):
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


class EmulatorWindow:
    def __init__(self, root):
        self.root = root
        self.shell = Shell()
        self.prompt = "user@vfs:~$ "
        self.history, self.hpos = [], 0

        root.title("Emulator — [vfs]")
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
        self.println(self.prompt + line)
        try:
            out = self.shell.execute(line)
            if out:
                self.println(out)
        except ShellError as e:
            self.println("error: %s" % e)
        if self.shell.exit_requested:
            self.root.destroy()

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


def main():
    root = tk.Tk()
    EmulatorWindow(root)
    root.mainloop()


if __name__ == "__main__":
    main()