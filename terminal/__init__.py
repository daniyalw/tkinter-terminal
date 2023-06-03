from tkinter import * # for the rest of tkinter
from tkinter.scrolledtext import * # for the terminal widget
import sys # to make Multiplatform
import os # for fun
import subprocess # for running commands

class Terminal(ScrolledText):
    def __init__(self, root):
        self.root = root
        self.path = os.getcwd()
        self._show = self.path + '>'
        self._command = ""
        self._count = 0
        self.colors = {"bg":"white", "fg":"black", "insertbackground":"black"} # set widget colors
        self._all_output = list()
        self._all_commands = list()
        self.nocommand = False
        self.customcommands = {}
        self.custom = False
        self.is_dark = False
        ScrolledText.__init__(self, root)
        ScrolledText.insert(self, END, self._show)
        ScrolledText.bind(self, "<Return>", self._on_enter) # set on enter func
        ScrolledText.bind(self, "<BackSpace>", self._on_back) # set backspace func
        ScrolledText.bind(self, "<Button-1>", self._on_left)

    def _on_left(self, event):
        if self._count != 0:
            return 'break'
        self._count += 1
        return

    def __index(self, i, d):
        c = 0
        for x in d:
            if i == c:
                return x, d[x]
            c += 1

    def _on_back(self, event): # on backspace
        # do checks to make sure the user doesn't delete output or self._show
        if ScrolledText.get(self, ScrolledText.index(self, INSERT).split('.')[0]+'.0', ScrolledText.index(self, INSERT)) == self._show:
            return 'break'
        if ScrolledText.get(self, '1.0', END).split('\n')[int(ScrolledText.index(self, INSERT).split('.')[0])-1].startswith(self._show):
            if float(ScrolledText.index(self, INSERT).split('.')[1]) < len(self._show) + 1:
                if int(ScrolledText.index(self, INSERT).split('.')[0]) == len(ScrolledText.get(self, '1.0', END).split()):
                    return 'break'
        else:
            return 'break'

    def cls(self):
        self.clear_screen()

    def clear_screen(self):
        ScrolledText.delete(self, '1.0', END) # clear screen
        self._show_dir(cls=True)

    def disable_commands(self):
        self.nocommand = true

    def _show_dir(self, cls=False):
        if cls:
            ScrolledText.insert(self, END, self._show)
        else:
            ScrolledText.insert(self, END, "\n" + self._show)
        ScrolledText.mark_set(self, 'insert', 'end-1c')
        ScrolledText.see(self, 'end-1c')
        return 'break'

    def new_custom_command(self, command, func):
        if not command in self.customcommands:
            self.customcommands[command] = func

    def get_first_element(self, command):
        return command.strip().split(' ')[0]

    def _on_enter(self, event):

        all_output = ScrolledText.get(self, '1.0', 'end-1c')
        self._command = all_output.split('\n')[-1].split('>')[1]
        self._all_commands.append(self._command)

        if self.custom:
            if self._command in self.customcommands:
                self.customcommands[self._command]()
                return 'break'

        if self.nocommand:
            self._show_dir()
            return 'break'

        if self.get_first_element(self._command) == 'cls' or self.get_first_element(self._command) == 'clear':
            self.clear_screen()
            return 'break'
        elif self.get_first_element(self._command) == '':
            self._show_dir()
            return 'break'
        elif self.get_first_element(self._command) == 'cd':
            # only our second arg will be the new path - any more args and we error
            args = self._command.strip().split()[1:]
            switch_dir = args[0]

            if len(args) > 1:
                self.show_output(f"cd: string not in pwd: {switch_dir}")
                return 'break'

            os.chdir(switch_dir)
            self.path = os.getcwd()
            self._show = self.path + '>'

            self._show_dir()
            return 'break'
        elif self.get_first_element(self._command) == 'color':
            args = self._command.strip().split()[1:]


            for i, arg in enumerate(args):
                if arg != 'current':
                    if '=' in arg:
                        self.colors[arg.split('=')[0]] = arg.split('=')[1]
                    else:
                        self.colors[self.__index(i, self.colors)[0]] = arg

            err = ""

            for i, c in enumerate(self.colors):
                if self.colors[c] == '':
                    continue

                if c == "bg":
                    try:
                        ScrolledText.config(self, bg=self.colors[c])
                    except TclError:
                        err += "bg: Invalid color name: " + self.colors[c] + "\n"
                elif c == "fg":
                    try:
                        ScrolledText.config(self, fg=self.colors[c])
                    except TclError:
                        err += "fg: Invalid color name: " + self.colors[c] + "\n"
                elif c == "insert":
                    try:
                        ScrolledText.config(self, insertbackground=self.colors[c])
                    except TclError:
                        err += "insert: Invalid color name: " + self.colors[c] + "\n"

            self.show_output(err)
            return 'break'

        self.run(self._command)
        return 'break' # make sure tkinter doesn't use default callback

    def run(self, cmd):
        self._command = cmd
        self._all_commands.append(self._command)

        output = ""

        try:
            output = subprocess.check_output(self._command, cwd=self.path, shell=True).decode()
        except:
            output = "Error: command failed to procede.\n"

        ScrolledText.insert(self, END, "\n" + output + "\n" + self._show) # show output
        ScrolledText.mark_set(self, 'insert', 'end-1c')
        ScrolledText.see(self, 'end-1c')
        self._all_output.append(output) # append output to all the outputs

    def show_output(self, output):
        ScrolledText.insert(self, END, "\n" + output + "\n" + self._show) # show output
        ScrolledText.mark_set(self, 'insert', 'end-1c')
        ScrolledText.see(self, 'end-1c')

    def clear_output(self):
        self._all_output = []

    def last_output(self):
        return self._all_output[-1]

    def clear_commands(self):
        self._all_commands = []

    def last_command(self):
        return self._all_commands[-1]

    def commands(self):
        return self._all_commands

    def output(self):
        return self._all_output

    def dark_mode(self, bg='grey7', fg='white', insertbackground='white'):
        self.colors['bg'] = bg # set bg
        self.colors['fg'] = fg # set fg
        self.colors['insertbackground'] = insertbackground
        ScrolledText.config(self, bg=bg, fg=fg, insertbackground=insertbackground) # configure colors
        is_dark = True

    def light_mode(self, bg='white', fg='black', insertbackground='black'):
        self.colors['bg'] = bg # set bg
        self.colors['fg'] = fg # set fg
        self.colors['insertbackground'] = insertbackground
        ScrolledText.config(self, bg=bg, fg=fg, insertbackground=insertbackground) # configure colors
        is_dark = False

    def toggle_mode():
        if is_dark:
            light_mode()
        else:
            dark_mode()

def default():
    root = Tk()
    root.config(bg='grey7')
    text = Terminal(root)
    text.custom = True
    text.pack()
    text.dark_mode()
    root.mainloop()

if __name__ == "__main__":
    root = Tk()
    root.config(bg='grey7')
    text = Terminal(root)
    text.custom = True
    text.pack()
    text.dark_mode()
    root.mainloop()
