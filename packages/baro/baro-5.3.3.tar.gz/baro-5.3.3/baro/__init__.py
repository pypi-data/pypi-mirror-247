'''
Easy and simple loading bar for python.

TYPES:
    baro.SPIN,
    baro.BAR

# How to use:
```python
from baro import baro

bar = baro(total=100, 'Setting up..', type=baro.SPIN)

# Option 1
bar.start().close()

# Option 2
for iter in bar:
    # Do something
    bar.update(iter)

bar.close()

# Option 3
with baro(total=100, 'Setting up..', type=baro.SPIN) as bar:
    # Do something
    for iter in bar:
        # Do something
        bar.update(iter)
```

CLASSES:
    baro.baro,
    baro.fore (Contains fore colors for coloring text),
    baro.style (Contains style i.e. BOLD for styling text),
    baro.back (Contains the colors for the background of the text)

METHODS:
    baro.color(
        color: fore (Default none), 
        style: style (Default none),
        back: back (Default none)
    )
    baro.reset() Returns the defualt color, style, and back.
'''

import sys
import time

BAR = '█'
BAR_UNFILLED = '░'
SPIN_CHARS = ['|', '/', '-', '\\']

class baro:
    def __init__(self, total, desc='', type='bar'):
        self.iter = range(total)
        self.desc = desc if desc else ''
        self.start_time = time.time()
        self.last_print_time = 0
        self.last_print_n = 0
        self.total = total
        self.red = '\033[31m'
        self.blue = '\033[34m'
        self.green = '\033[32m'
        self.yellow = '\033[33m'
        self.reset = '\033[0m'
        if type != 'bar':
            type = 'spin'

        self.type = type

    def bar_update(self, n=1):
        self.last_print_n += n
        now = time.time()
        if now - self.last_print_time >= 0.1:
            self.last_print_time = now
            elapsed = now - self.start_time

            bar_width = int(100 * elapsed / self.total)

            filled_length = int(bar_width * self.last_print_n / self.total)
            bar_unfilled = int(bar_width * (self.total - self.last_print_n) / self.total)
            bar_unfilled = '░' * bar_unfilled
            bar = '█' * filled_length + bar_unfilled
            color = self.blue
            if self.last_print_n >= self.total:
                color = self.green

            progress_msg = f'\r%s |{color}%s{self.reset}| {self.yellow}%d{self.reset}/{self.red}%d{self.reset} %s' % (
                self.desc, bar, self.last_print_n, self.total, self.format_elapsed(elapsed)
            )

            sys.stdout.write(progress_msg)
            sys.stdout.flush()

    def spin_update(self, n=1):
        self.last_print_n += n
        now = time.time()
        if now - self.last_print_time >= 0.1:
            self.last_print_time = now
            elapsed = now - self.start_time

            spin_char = SPIN_CHARS[self.last_print_n % len(SPIN_CHARS)]

            # check if done
            color = self.blue
            msg = spin_char
            if self.last_print_n >= self.total:
                msg = f'COMPLETE'
                color = self.green

            progress_msg = f'\r{self.desc} {color}{msg}{self.reset} {self.yellow}%d{self.reset}/{self.red}%d{self.reset} %s' % (
                self.last_print_n, self.total, self.format_elapsed(elapsed)
            )

            sys.stdout.write(progress_msg)
            sys.stdout.flush()

    def step(self, n=1):
        if self.type == 'bar':
            self.bar_update(n)

        elif self.type == 'spin':
            self.spin_update(n)

        else:
            self.bar_update(n)

        return self

    def close(self):
        sys.stdout.write('\n')
        self.last_print_time = 0
        self.last_print_n = 0

    def sleep(self, n=1):
        time.sleep(n)
        return self

    def format_elapsed(self, elapsed):
        hours = int(elapsed // 3600)
        minutes = int((elapsed % 3600) // 60)
        seconds = int(elapsed % 60)
        return f'{hours:02d}:{minutes:02d}:{seconds:02d}'

    def start(self, sleep=0.1):
        for i in self.iter:
            self.step()
            time.sleep(sleep)
        return self

    def set_type(self, type):
        if type != 'bar': self.type = 'spin'
        else: self.type = 'bar'
        return self.type

    def set_desc(self, desc):
        self.desc = desc
        return self.desc

    def set_total(self, total):
        self.total = total
        return self.total

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()

    def __iter__(self):
        return iter(self.iter)

    def __next__(self):
        return next(self.iter)

    def __repr__(self):
        return f'load(total: {self.total}, desc: {self.desc!r})'

    def __str__(self):
        return f'load(total: {self.total}, desc: {self.desc!r})'

class fore:
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    RESET = '\033[0m'

class style:
    BOLD = '\033[1m'
    DIM = '\033[2m'
    NORMAL = '\033[22m'
    RESET_ALL = '\033[0m'

class back:
    BLACK = '\033[40m'
    RED = '\033[41m'
    GREEN = '\033[42m'
    YELLOW = '\033[43m'
    BLUE = '\033[44m'
    MAGENTA = '\033[45m'
    CYAN = '\033[46m'
    WHITE = '\033[47m'
    RESET = '\033[49m'

SPIN = 'spin'
BAR = 'bar'

def color(color=None, style=None, back=None):
    return_string = ''
    if color: return_string += color
    if style: return_string += style
    if back: return_string += back
    return return_string

def reset():
    return color(color=color.RESET, style=style.RESET_ALL, back=back.RESET)

__version__ = '5.3.3'
__author__ = 'toolkitr'
__license__ = 'MIT'
__copyright__ = 'Copyright (c) 2023 toolkitr'
__all__ = (
    'baro',
    'fore',
    'style',
    'back',
    'color',
    'reset',
)