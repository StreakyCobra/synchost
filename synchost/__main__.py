# -*- coding: utf-8 -*-

import importlib
import os
import sys

from collections import defaultdict
from synchost.config import plugins_path

sys.path.insert(0, plugins_path)

# Some parameters
maxlen = 0
colors = dict()
colors['red'] = "\x1b[91m"
colors['green'] = "\x1b[92m"
colors['yellow'] = "\x1b[93m"
colors['blue'] = "\x1b[94m"
colors['magenta'] = "\x1b[95m"
colors['cyan'] = "\x1b[96m"
colors['white'] = "\x1b[97m"
colors['OFF'] = "\x1b[0m"
restart_line = "\033[2K\r"


def colored(text, color):
    return colors[color] + text + colors['OFF']


def load_module(module_name):
    # Load the module dynamically
    mod = importlib.import_module(module_name)
    # Return the module
    return mod


def print_title(val, sub=False):
    sym = '-' if sub else "="
    sys.stdout.write(colored(val, 'cyan'))
    sys.stdout.write('\n')
    sys.stdout.write(colored(sym * len(val), 'magenta'))
    sys.stdout.write('\n')


def print_line(name, rc, text=None, nl=True):
    if rc == 0:
        color = 'green'
        if text is None:
            text = "OK"
    elif rc == -1:
        color = 'yellow'
        if text is None:
            text = "NA"
    elif rc == -2:
        color = 'white'
        if text is None:
            text = "NA"
    else:
        color = 'red'
        if text is None:
            text = "KO"

    sys.stdout.write(colored(("%%-%ds" % maxlen) % name,
                             'blue'))
    sys.stdout.write(colored(' → ', 'magenta'))
    sys.stdout.write(colored(text, color))
    sys.stdout.write('\n' if nl else '')
    sys.stdout.flush()


def apply(modname, funcname, printname=None):
    # Create title from function name if not specified
    if printname is None:
        printname = modname

    print_line(printname, -2, "Processing…", nl=False)

    # Get desired function
    try:
        func = getattr(load_module(modname), funcname)
        result = func()
    except BaseException:
        print_line(printname, -1, "No \"%s()\" function" % funcname)
        return

    sys.stdout.write(restart_line)
    if isinstance(result, int):
        print_line(printname, result)
    elif result is not None:
        print_line(printname, result[0], result[1])
    else:
        print_line(printname, 1, "Function \"%s()\" failed" % funcname)


def plugins():
    filenames = os.listdir(plugins_path)
    filenames = filter(lambda x: os.path.isfile(os.path.join(plugins_path, x)),
                       filenames)
    filenames = map(lambda x: os.path.splitext(x), filenames)
    filenames = filter(lambda x: x[1] == '.py', filenames)
    plugins = list(map(lambda x: x[0], filenames))

    global maxlen
    maxlen = max(map(len, plugins))

    result = defaultdict(list)
    for plugin in plugins:
        # Get desired function
        try:
            func = getattr(load_module(plugin), 'category')
            result[func].append(plugin)
        except BaseException:
            result['Unknown'].append(plugin)

    return result


def run():
    cmd = 'status'
    if len(sys.argv) >= 2:
        cmd = sys.argv[1]

    print_title(cmd.upper())

    plugs = plugins()

    for cat in sorted(plugs.keys()):
        sys.stdout.write('\n')
        print_title(cat, sub=True)
        for plugin in sorted(plugs[cat]):
            apply(plugin, cmd)


# When used as a script
if __name__ == "__main__":
    run()
