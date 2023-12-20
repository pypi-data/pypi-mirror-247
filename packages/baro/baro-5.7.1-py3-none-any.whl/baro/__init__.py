'''
Easy and simple loading bar for python.

```
CLASSES:
    baro.thin(total, color_start=fore.GREEN, color_end=fore.BLUE)
    baro.line(total, color_start=fore.GREEN, color_end=fore.BLUE)
    baro.bar(total, color_start=fore.GREEN, color_end=fore.BLUE)
    baro.spin(total, color_start=fore.GREEN, color_end=fore.BLUE)
    baro.spin2(total, color_start=fore.GREEN, color_end=fore.BLUE)
    baro.customspin(total, chars, color_start=fore.GREEN, color_end=fore.BLUE)
    baro.timed(total, desc='', color_start=fore.GREEN, color_end=fore.BLUE)

FORE, STYLE, BACK:
    fore.BLACK, fore.RED, fore.GREEN, fore.YELLOW, fore.BLUE, fore.MAGENTA, fore.CYAN, fore.WHITE, fore.RESET

    style.BOLD, style.DIM, style.NORMAL, style.RESET_ALL

    back.BLACK, back.RED, back.GREEN, back.YELLOW, back.BLUE, back.MAGENTA, back.CYAN, back.WHITE, back.RESET
```

# How to use baro!
```python
import baro

baro.thin(100).start().close()

bar = baro.line(100)
bar.start()
bar.close()

bar2 = baro.bar(100)
with bar2 as bar_2:
    for iterable in bar2:
        # do something
        bar_2.update(iterable)
        bar_2.sleep(0.1)

bar3 = baro.spin(100).start().close()

bar4 = baro.spin2(100).start().close()

bar5 = baro.custom(100, ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i']).start().close()

bar6 = baro.timed(100, 'This is a timed bar').start().close()
```
'''

import time
import shutil

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

def color(color=None, style=None, back=None):
    return_string = ''
    if color: return_string += color
    if style: return_string += style
    if back: return_string += back
    return return_string

def reset():
    return color(color=fore.RESET, style=style.RESET_ALL, back=back.RESET)    

class thin:
    def __init__(self, total, sub=None, color_start=fore.GREEN, color_end=fore.BLACK):
        self.bar = '━'
        self.total = total
        self.sub = sub if sub else 40
        self.width = shutil.get_terminal_size().columns - self.sub
        self.color_start = color_start
        self.color_end = color_end
        self.start_time = time.time()
        self.elapsed_time = 0
        self.end_time = None

    def sleep(self, sleep=0.1):
        time.sleep(sleep)
        return self

    def update(self, progress):
        filled_width = int(self.width * progress / self.total)
        remaining_width = self.width - filled_width
        color_progress = self.color_start + self.bar * filled_width + self.color_end + self.bar * remaining_width + reset()
        percentage = progress / self.total * 100
        self.elapsed_time = self.format_elapsed(time.time() - self.start_time)
        print(f'\r{color_progress} {percentage:.1f}% [{self.elapsed_time}]', end='')
        if progress+1 >= self.total:
            color_progress = fore.BLUE + self.bar * filled_width + fore.BLUE + self.bar * remaining_width + reset()
            self.end_time = self.elapsed_time
            print(f'\r{color_progress} 100% [{self.elapsed_time}]', end='')

        return self

    def format_elapsed(self, elapsed):
        hours = int(elapsed // 3600)
        minutes = int((elapsed % 3600) // 60)
        seconds = int(elapsed % 60)
        return f'{hours:02d}:{minutes:02d}:{seconds:02d}'

    def start(self, sleep=0.1):
        for i in range(self.total):
            self.update(i)
            time.sleep(sleep)
        return self

    def close(self):
        self.end_time = self.format_elapsed(time.time() - self.start_time)
        print()
        return self

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return self.close()

    def __iter__(self):
        return iter(range(self.total))

    def __next__(self):
        return next(range(self.total))

    def __repr__(self):
        return f'baro(total: {self.total})'

    def __str__(self):
        return f'baro(total: {self.total})'

class line:
    def __init__(self, total, sub=None, color_start=fore.GREEN, color_end=fore.BLACK):
        self.bar = '▬'
        self.total = total
        self.sub = sub if sub else 40
        self.width = shutil.get_terminal_size().columns - self.sub
        self.color_start = color_start
        self.color_end = color_end
        self.start_time = time.time()
        self.elapsed_time = 0
        self.end_time = None

    def sleep(self, sleep=0.1):
        time.sleep(sleep)
        return self

    def update(self, progress):
        filled_width = int(self.width * progress / self.total)
        remaining_width = self.width - filled_width
        color_progress = self.color_start + self.bar * filled_width + self.color_end + self.bar * remaining_width + reset()
        percentage = progress / self.total * 100
        self.elapsed_time = self.format_elapsed(time.time() - self.start_time)
        print(f'\r{color_progress} {percentage:.1f}% [{self.elapsed_time}]', end='')
        if progress+1 >= self.total:
            color_progress = fore.BLUE + self.bar * filled_width + fore.BLUE + self.bar * remaining_width + reset()
            self.end_time = self.elapsed_time
            print(f'\r{color_progress} 100% [{self.elapsed_time}]', end='')

        return self

    def format_elapsed(self, elapsed):
        hours = int(elapsed // 3600)
        minutes = int((elapsed % 3600) // 60)
        seconds = int(elapsed % 60)
        return f'{hours:02d}:{minutes:02d}:{seconds:02d}'

    def start(self, sleep=0.1):
        for i in range(self.total):
            self.update(i)
            time.sleep(sleep)
        return self

    def close(self):
        self.end_time = self.format_elapsed(time.time() - self.start_time)
        print()
        return self

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return self.close()

    def __iter__(self):
        return iter(range(self.total))

    def __next__(self):
        return next(range(self.total))

    def __repr__(self):
        return f'baro(total: {self.total})'

    def __str__(self):
        return f'baro(total: {self.total})'

class bar:
    def __init__(self, total, sub=None, color_start=fore.GREEN, color_end=fore.BLACK):
        self.bar = '█'
        self.total = total
        self.sub = sub if sub else 40
        self.width = shutil.get_terminal_size().columns - self.sub
        self.color_start = color_start
        self.color_end = color_end
        self.start_time = time.time()
        self.elapsed_time = 0
        self.end_time = None

    def sleep(self, sleep=0.1):
        time.sleep(sleep)
        return self

    def update(self, progress):
        filled_width = int(self.width * progress / self.total)
        remaining_width = self.width - filled_width
        color_progress = self.color_start + self.bar * filled_width + self.color_end + self.bar * remaining_width + reset()
        percentage = progress / self.total * 100
        self.elapsed_time = self.format_elapsed(time.time() - self.start_time)
        print(f'\r{color_progress} {percentage:.1f}% [{self.elapsed_time}]', end='')
        if progress+1 >= self.total:
            color_progress = fore.BLUE + self.bar * filled_width + fore.BLUE + self.bar * remaining_width + reset()
            self.end_time = self.elapsed_time
            print(f'\r{color_progress} 100% [{self.elapsed_time}]', end='')

        return self

    def format_elapsed(self, elapsed):
        hours = int(elapsed // 3600)
        minutes = int((elapsed % 3600) // 60)
        seconds = int(elapsed % 60)
        return f'{hours:02d}:{minutes:02d}:{seconds:02d}'

    def start(self, sleep=0.1):
        for i in range(self.total):
            self.update(i)
            time.sleep(sleep)
        return self

    def close(self):
        self.end_time = self.format_elapsed(time.time() - self.start_time)
        print()
        return self

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return self.close()

    def __iter__(self):
        return iter(range(self.total))

    def __next__(self):
        return next(range(self.total))

    def __repr__(self):
        return f'baro(total: {self.total})'

    def __str__(self):
        return f'baro(total: {self.total})'

class spin:
    def __init__(self, total, color_start=fore.GREEN, color_end=fore.BLUE):
        self.chars = ['|', '/', '-', '\\']*5 * round(total/50)
        self.total = total
        self.color_start = color_start
        self.color_end = color_end
        self.start_time = time.time()
        self.elapsed_time = 0
        self.end_time = None
        self.total_steps = len(self.chars)
        self.current_step = 0

    def sleep(self, sleep=0.1):
        time.sleep(sleep)
        return self

    def format_elapsed(self, elapsed):
        hours = int(elapsed // 3600)
        minutes = int((elapsed % 3600) // 60)
        seconds = int(elapsed % 60)
        return f'{hours:02d}:{minutes:02d}:{seconds:02d}'

    def start(self, sleep=0.1):
        for i in range(self.total):
            self.update(i)
            time.sleep(sleep)
        return self

    def close(self):
        self.end_time = self.format_elapsed(time.time() - self.start_time)
        print()
        return self

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return self.close()

    def __iter__(self):
        return iter(range(self.total))

    def __next__(self):
        return next(range(self.total))

    def __repr__(self):
        return f'baro(total: {self.total})'

    def __str__(self):
        return f'baro(total: {self.total})'

    def update(self, progress):
        progress = progress / self.total
        progress_steps = int(progress * 100)
        self.current_step = int((progress * self.total_steps) % self.total_steps)
        self.elapsed_time = self.format_elapsed(time.time() - self.start_time)
        print(f'\r{self.color_start}{self.chars[self.current_step]}{reset()} {self.color_end}{reset()} {progress_steps}% [{self.elapsed_time}]', end='')
        if self.current_step+1 >= self.total_steps:
            self.end_time = self.elapsed_time
            print(f'\r{self.color_start}COMPLETE{reset()} {self.color_end}{reset()} 100% [{self.elapsed_time}]', end='')

class spin2:
    def __init__(self, total, color_start=fore.GREEN, color_end=fore.BLUE):
        self.chars = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']*5 * round(total/50)
        self.total = total
        self.color_start = color_start
        self.color_end = color_end
        self.start_time = time.time()
        self.elapsed_time = 0
        self.end_time = None
        self.total_steps = len(self.chars)
        self.current_step = 0

    def sleep(self, sleep=0.1):
        time.sleep(sleep)
        return self

    def format_elapsed(self, elapsed):
        hours = int(elapsed // 3600)
        minutes = int((elapsed % 3600) // 60)
        seconds = int(elapsed % 60)
        return f'{hours:02d}:{minutes:02d}:{seconds:02d}'

    def start(self, sleep=0.1):
        for i in range(self.total):
            self.update(i)
            time.sleep(sleep)
        return self

    def close(self):
        self.end_time = self.format_elapsed(time.time() - self.start_time)
        print()
        return self

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return self.close()

    def __iter__(self):
        return iter(range(self.total))

    def __next__(self):
        return next(range(self.total))

    def __repr__(self):
        return f'baro(total: {self.total})'

    def __str__(self):
        return f'baro(total: {self.total})'

    def update(self, progress):
        progress = progress / self.total
        progress_steps = int(progress * 100)
        self.current_step = int((progress * self.total_steps) % self.total_steps)
        self.elapsed_time = self.format_elapsed(time.time() - self.start_time)
        print(f'\r{self.color_start}{self.chars[self.current_step]}{reset()} {self.color_end}{reset()} {progress_steps}% [{self.elapsed_time}]', end='')
        if self.current_step+1 >= self.total_steps:
            self.end_time = self.elapsed_time
            print(f'\r{self.color_start}COMPLETE{reset()} {self.color_end}{reset()} 100% [{self.elapsed_time}]', end='')

class custom:
    def __init__(self, total, chars: list, color_start=fore.GREEN, color_end=fore.BLUE):
        self.chars = chars * round(total/50)
        self.total = total
        self.color_start = color_start
        self.color_end = color_end
        self.start_time = time.time()
        self.elapsed_time = 0
        self.end_time = None
        self.total_steps = len(self.chars)
        self.current_step = 0

    def sleep(self, sleep=0.1):
        time.sleep(sleep)
        return self

    def format_elapsed(self, elapsed):
        hours = int(elapsed // 3600)
        minutes = int((elapsed % 3600) // 60)
        seconds = int(elapsed % 60)
        return f'{hours:02d}:{minutes:02d}:{seconds:02d}'

    def start(self, sleep=0.1):
        for i in range(self.total):
            self.update(i)
            time.sleep(sleep)
        return self

    def close(self):
        self.end_time = self.format_elapsed(time.time() - self.start_time)
        print()
        return self

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return self.close()

    def __iter__(self):
        return iter(range(self.total))

    def __next__(self):
        return next(range(self.total))

    def __repr__(self):
        return f'baro(total: {self.total})'

    def __str__(self):
        return f'baro(total: {self.total})'

    def update(self, progress):
        progress = progress / self.total
        progress_steps = int(progress * 100)
        self.current_step = int((progress * self.total_steps) % self.total_steps)
        self.elapsed_time = self.format_elapsed(time.time() - self.start_time)
        print(f'\r{self.color_start}{self.chars[self.current_step]}{reset()} {self.color_end}{reset()} {progress_steps}% [{self.elapsed_time}]', end='')
        if self.current_step+1 >= self.total_steps:
            self.end_time = self.elapsed_time
            print(f'\r{self.color_start}COMPLETE{reset()} {self.color_end}{reset()} 100% [{self.elapsed_time}]', end='')

class timed:
    def __init__(self, total, desc='', color_start=fore.GREEN, color_end=fore.BLUE):
        self.time = total
        self.desc = desc
        self.color_start = color_start
        self.color_end = color_end
        self.start_time = time.time()
        self.elapsed_time = 0
        self.end_time = None

    def sleep(self, sleep=0.1):
        time.sleep(sleep)
        return self

    def format_elapsed(self, elapsed):
        hours = int(elapsed // 3600)
        minutes = int((elapsed % 3600) // 60)
        seconds = int(elapsed % 60)
        return f'{hours:02d}:{minutes:02d}:{seconds:02d}'

    def start(self):
        while True:
            self.elapsed_time = time.time() - self.start_time
            if self.elapsed_time >= self.time:
                self.elapsed_time = self.format_elapsed(self.elapsed_time)
                print(f'\r{self.color_start}[{self.elapsed_time}/{self.format_elapsed(self.time)}] {self.color_end}[COMPLETE]{reset()} {self.desc}', end='')
                break
            else:
                self.elapsed_time = self.format_elapsed(self.elapsed_time)
                print(f'\r{self.color_start}[{self.elapsed_time}/{self.format_elapsed(self.time)}] {self.color_end}{reset()} {self.desc}', end='')
                time.sleep(0.1)
        return self
        
    def close(self):
        self.end_time = self.format_elapsed(time.time())
        print()
        return self

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return self.close()

    def __iter__(self):
        return iter(range(self.time))

    def __next__(self):
        return next(range(self.time))

    def __repr__(self):
        return f'baro(time: {self.time}, desc: {self.desc})'

    def __str__(self):
        return f'baro(time: {self.time}, desc: {self.desc})'

__version__ = '5.7.1'
__author__ = 'toolkitr'
__license__ = 'MIT'
__copyright__ = 'Copyright (c) 2023 toolkitr'
__all__ = (
    'thin',
    'line',
    'bar',
    'spin',
    'spin2',
    'custom',
    'timed'
)