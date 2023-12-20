import time
import shutil
import random

BAR1 = '█'
BAR2 = '▒'
BAR3 = '▬'
BAR4 = '━'
BAR5 = '='
BAR6 = '○'
BAR7 = '●'

SPIN1 = ['|', '/', '-', '\\']*6
SPIN2 = ['◜', '◠', '◝', '◞', '◡', '◟']*6
SPIN3 = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']*5
SPIN4 = ['⣾', '⣽', '⣻', '⢿', '⡿', '⣟', '⣯', '⣷']*5
SPIN5 = ['⠁', '⠂', '⠄', '⡀', '⢀', '⠠', '⠐', '⠈']*5
SPIN6 = ['⣀', '⡀', '⠄', '⡈', '⠐', '⠈', '⠄', '⡀']*5
SPIN7 = ['▔', '▕', '▖', '▗', '▘', '▙', '▚', '▛', '▜', '▝', '▞', '▟']*3

WAVE1 = ['▁', '▂', '▃', '▄', '▅', '▆', '▇', '█']
WAVE2 = ['▏', '▎', '▍', '▌', '▋', '▊', '▉', '█']
WAVE3 = ['▔', '▕', '▖', '▗', '▘', '▙', '▚', '▛', '▜', '▝', '▞', '▟']
WAVE4 = ['⣀', '⡀', '⠄', '⡈', '⠐', '⠈', '⠄', '⡀']
WAVE5 = ['⣠', '⣤', '⣶', '⣾', '⣿']

GREY = '\033[38;5;236m'
GREEN = "\033[0;32m"
BLUE = "\033[0;34m"
RED = "\033[0;31m"
RESET = '\033[0m'

class EnterExit:
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.stop()

class bar(EnterExit):
    def __init__(self, length, char=BAR1, text=''):
        self.length = length
        self.iters = range(self.length + 1)
        self.text = text
        self.char = char
        self.progress = 0
        self.start_time = time.time()
        self.elapsed_time = 0
        self.bar = ''
        self.error = False
        self.error_message = ''
        self.finished = False
        self.column_size = shutil.get_terminal_size().columns - 30
        self.bar_length = self.column_size - len(self.text) - 1
        self.bar_length = self.bar_length if self.bar_length > 0 else 1

        self.bar_error_color = RED
        self.bar_background_color = GREY
        self.bar_loading_color = BLUE
        self.bar_completed_color = GREEN
        self.bar_reset_color = RESET

    def update(self, progress):
        try:
            if not self.finished:
                self.progress = progress
                percent_to_fill = self.progress / self.length
                percent_to_fill_background = 1 - percent_to_fill
                self.bar = f'{self.bar_loading_color}{self.char}{self.bar_reset_color}' * int(
                    percent_to_fill * self.bar_length)
                self.bar += f'{self.bar_background_color}{self.char}{self.bar_reset_color}' * int(
                    percent_to_fill_background * self.bar_length)
                if self.progress >= self.length:
                    self.bar = f'{self.bar_completed_color}{self.char}{self.bar_reset_color}' * self.bar_length
                    self.finished = True

                self.elapsed_time = time.time() - self.start_time
                self.update_bar()
                self.print_bar()
        except:
            self.error = True
            self.error_message = 'Error'
            self.update_bar()
            self.print_bar()
            self.finished = True

    def update_bar(self):
        percent_to_fill = self.progress / self.length
        percent_to_fill_background = 1 - percent_to_fill
        if self.error:
            self.bar = f'{self.bar_error_color}{self.char}{self.bar_reset_color}' * int(percent_to_fill * self.bar_length)
            self.bar += f'{self.bar_background_color}{self.char}{self.bar_reset_color}' * int(
                percent_to_fill_background * self.bar_length)
        elif self.finished:
            self.bar = f'{self.bar_completed_color}{self.char}{self.bar_reset_color}' * self.bar_length
        else:
            self.bar = f'{self.bar_loading_color}{self.char}{self.bar_reset_color}' * int(percent_to_fill * self.bar_length)
            self.bar += f'{self.bar_background_color}{self.char}{self.bar_reset_color}' * int(
                percent_to_fill_background * self.bar_length)

    def print_bar(self):
        self.elapsed_time = time.time() - self.start_time
        format_time = time.strftime('%H:%M:%S', time.gmtime(self.elapsed_time))
        percent_complete = self.progress / self.length
        percent_complete_str = f'{percent_complete * 100:.2f}'
        text = f'{self.text} {self.bar} {self.bar_reset_color} {percent_complete_str[:-3]}% [{format_time}]'
        print(f'\r{text}', end=' ', flush=True)

        if self.error:
            self.finished = True

    def stop(self):
        self.finished = True
        print()

    def crash(self, message):
        self.error = True
        self.text = message
        self.update_bar()
        self.print_bar()
        self.finished = True

    def sleep(self, seconds=0.1):
        time.sleep(seconds)
        return self

    def run(self, sleep=0.1, method=None, *method_args, **method_kwargs):
        for iteration in self.iters:
            self.update(iteration)
            if self.error or self.finished:
                break
            self.sleep(sleep)
        return self

    @staticmethod
    def multi(*loading_bars, sleep=0.1):
        for loading_bar in loading_bars:
            loading_bar.run(sleep).stop()
        return loading_bars

class spin(EnterExit):
    def __init__(self, total, chars=SPIN1, text=''):
        self.text = text
        self.chars = chars
        self.iters = range(total)
        self.progress = 0
        self.start_time = time.time()
        self.elapsed_time = 0
        self.error = False
        self.error_message = ''
        self.finished = False

        self.spin_color = BLUE
        self.error_color = RED
        self.complete_color = GREEN

    def update(self, progress):
        try:
            if not self.finished:
                self.progress = progress
                self.elapsed_time = time.time() - self.start_time
                self.update_spin()
                self.print_spin()
        except:
            self.error = True
            self.error_message = 'ERROR'
            self.print_spin()
            self.finished = True

    def update_spin(self):
        pass

    def print_spin(self):
        spin_char = self.chars[self.progress % len(self.chars)]
        format_time = time.strftime('[%H:%M:%S]', time.gmtime(self.elapsed_time))
        color = self.spin_color

        if self.error:
            spin_char = self.error_message
            color = self.error_color
        elif self.finished:
            spin_char = 'COMPLETE'
            color = self.complete_color

        text = f'{self.text} {color}{spin_char}{RESET} {format_time}'
        print(f'\r{text}', end=' ', flush=True)

        if self.error:
            self.finished = True

    def stop(self):
        self.finished = True
        print()

    def crash(self, message):
        self.error = True
        self.error_message = message
        self.print_spin()
        self.finished = True

    def sleep(self, seconds=0.1):
        time.sleep(seconds)
        return self

    def run(self, sleep=0.1, method=None, *method_args, **method_kwargs):
        for iteration in self.iters:
            self.update(iteration)
            if self.error or self.finished:
                break
            self.sleep(sleep)
        if not self.finished:
            self.finished = True
            self.print_spin()
        return self

    @staticmethod
    def multi(*spinning_objects, sleep=0.1):
        for spinning_object in spinning_objects:
            spinning_object.run(sleep).stop()
        return spinning_objects

class wave(EnterExit):
    def __init__(self, length, chars=WAVE1, text=''):
        self.text = text
        self.iters = range(length)
        self.progress = 0
        self.start_time = time.time()
        self.elapsed_time = 0
        self.error = False
        self.error_message = ''
        self.finished = False

        self.wave_pattern = chars
        self.wave_color = BLUE  # Blue color
        self.error_color = RED  # Red color
        self.complete_color = GREEN  # Green color
        self.reset_color = RESET  # Reset color

    def update(self, progress):
        try:
            if not self.finished:
                self.progress = progress
                self.elapsed_time = time.time() - self.start_time
                self.print_wave()
        except:
            self.error = True
            self.error_message = 'ERROR'
            self.print_wave()
            self.finished = True

    def print_wave(self):
        wave_char = []
        for i in range(4):
            wave_char.append(random.choice(self.wave_pattern))
        wave_char = ''.join(wave_char)
        format_time = time.strftime('[%H:%M:%S]', time.gmtime(self.elapsed_time))
        color = self.wave_color

        if self.error:
            wave_char = self.error_message
            color = self.error_color
        elif self.finished:
            wave_char = 'COMPLETE'
            color = self.complete_color

        text = f'{self.text} {color}{wave_char}{self.reset_color} {format_time}'
        print(f'\r{text}', end=' ', flush=True)

        if self.error:
            self.finished = True

    def stop(self):
        self.finished = True
        print()

    def crash(self, message):
        self.error = True
        self.error_message = message
        self.print_wave()
        self.finished = True

    def sleep(self, seconds=0.1):
        time.sleep(seconds)
        return self

    def run(self, sleep=0.1):
        for iteration in self.iters:
            self.update(iteration)
            if self.error or self.finished:
                break
            self.sleep(sleep)
        if not self.finished:
            self.finished = True
            self.print_wave()
        return self

    @staticmethod
    def multi(*wave_objects, sleep=0.1,):
        for wave_object in wave_objects:
            wave_object.run(sleep).stop()
        return wave_objects

class timed(EnterExit):
    def __init__(self, length, text=''):
        self.text = text
        self.length = length
        self.start_time = time.time()
        self.elapsed_time = 0
        self.error = False
        self.error_message = ''
        self.finished = False

        self.timed_color = BLUE  # Blue color
        self.error_color = RED  # Red color
        self.complete_color = GREEN  # Green color
        self.reset_color = RESET  # Reset color

    def update(self):
        try:
            if not self.finished:
                self.elapsed_time = time.time() - self.start_time
                self.print_timer()
        except:
            self.error = True
            self.error_message = 'ERROR'
            self.print_timer()
            self.finished = True

    def print_timer(self):
        format_elapsed_time = time.strftime('%H:%M:%S', time.gmtime(self.elapsed_time))
        format_total_time = time.strftime('%H:%M:%S', time.gmtime(self.length))
        percentage = int((self.elapsed_time / self.length) * 100)
        color = self.timed_color
        ending = ''
        if self.error:
            format_elapsed_time = self.error_message
            color = self.error_color
            ending = f'[{color}ERROR{self.reset_color}]'
        elif self.finished:
            format_elapsed_time = format_total_time
            color = self.complete_color
            ending = f'[{color}COMPLETE{self.reset_color}]'

        text = f'{self.text} [{color}{format_elapsed_time}s/{format_total_time}s{self.reset_color}] {percentage}% {ending}'
        print(f'\r{text}', end=' ', flush=True)

        if self.error:
            self.finished = True

    def stop(self):
        self.finished = True
        print()

    def crash(self, message):
        self.error = True
        self.error_message = message
        self.print_timer()
        self.finished = True

    def sleep(self, seconds=0.1):
        time.sleep(seconds)
        return self

    def run(self, sleep=0.1):
        while self.elapsed_time < self.length:
            self.update()
            if self.error or self.finished:
                break
            self.sleep(sleep)
        if not self.finished:
            self.finished = True
            self.print_timer()
        return self

    @staticmethod
    def multi(*timed_objects, sleep=0.1,):
        for timed_object in timed_objects:
            timed_object.run(sleep).stop()
        return timed_objects

__doc__ = f"""
Easy, modern, and beginner friendly loading animations.
```ruby
COLORS:
    RED
    GREEN
    BLUE
    RESET
```

```javascript
TYPES:
    BAR1: {BAR1},
    BAR2: {BAR2},
    BAR3: {BAR3},
    BAR4: {BAR4},
    BAR5: {BAR5},
    BAR6: {BAR6},
    BAR7: {BAR7},

    SPIN1: {SPIN1},
    SPIN2: {SPIN2},
    SPIN3: {SPIN3},
    SPIN4: {SPIN4},
    SPIN5: {SPIN5},
    SPIN6: {SPIN6},
    SPIN7: {SPIN7},

    WAVE1: {WAVE1},
    WAVE2: {WAVE2},
    WAVE3: {WAVE3},
    WAVE4: {WAVE4},
    WAVE5: {WAVE5},
```
# Basic example
```python
import loado as ld

# Bar
ld.bar(10, BAR1, 'A bar').run().stop()

# Spin
spinner = ld.spin(10, SPIN1, 'A spin')
spinner.run()
spinner.stop()

# Wave
with ld.wave(10, WAVE1, 'A wave') as wave:
    wave.run()
    wave.stop()
    print('Finished wave!')

# Timed
with ld.timed(10, 'A timed') as timed:
    timed.run()
    timed.stop()
    print('Finished timed!')
```
You can use the variable way or the with statement way.
"""

__version__ = '5.8.1'
__author__ = 'loado'
__license__ = 'MIT'
__copyright__ = 'Copyright (c) 2023 loado'
__all__ = [
    'bar',
    'spin',
    'wave',
    'timed',
]