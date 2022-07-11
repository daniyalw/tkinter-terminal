# terminal
This is a terminal widget in Tkinter and Python.

Note: running applications such as gcc or such, which have infinite loops, will hang this, since no new thread/process is created when executing user input. 

## Installation
Download the folder and in command-line, travel to the 'terminal' directory. Use `pip install .`.

## How to use
A simple script
```
from tkinter import *
from terminal import *

root = Tk()
terminal = Terminal(root)
terminal.pack()
root.mainloop()
```

A terminal will be shown.

## Specifications
### Dark mode
To use dark mode:
```
terminal.dark_mode()
```
Use the `dark_mode` method.

### Run a command programmatically
To run a command, use the `run` method:
```
terminal.run('echo hello')
```

### Clear the console
To clear the console programmatically, use the `clear_screen` method:
```
terminal.clear_screen()
```
To clear it within the console, use the `cls` command.

### Get all used commands
To get used commands, use the `commands` method:
```
used_commands = terminal.commands()
```

### Get all output
To get all output, use the `output` method:
```
all_output = terminal.output()
```

### Clear all output
To clear the output list, use the `clear_output` method:
```
terminal.clear_output()
```

### Clear all used commands
To clear the used commands list, use the `clear_commands` method:
```
terminal.clear_commands()
```

### Disable commands
To disable all commands except for what commands you manually set:
```
terminal.disable_commands()
```

### Set a command
To set a command that the user can run:
```
terminal.new_custom_command("my-cool-command", myfunction)
```
