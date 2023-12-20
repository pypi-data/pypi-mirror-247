NAME
    loado

DESCRIPTION
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
        BAR1: █,
        BAR2: ▒,
        BAR3: ▬,
        BAR4: ━,
        BAR5: =,
        BAR6: ○,
        BAR7: ●,

        SPIN1: ['|', '/', '-', '\\', '|', '/', '-', '\\', '|', '/', '-', '\\', '|', '/', '-', '\\', '|', '/', '-', '\\', '|', '/', '-', '\\'],
        SPIN2: ['◜', '◠', '◝', '◞', '◡', '◟', '◜', '◠', '◝', '◞', '◡', '◟', '◜', '◠', '◝', '◞', '◡', '◟', '◜', '◠', '◝', '◞', '◡', '◟', '◜', '◠', '◝', '◞', '◡', '◟', '◜', '◠', '◝', '◞', '◡', '◟'],
        SPIN3: ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏', '⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏', '⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏', '⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏', '⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏'],
        SPIN4: ['⣾', '⣽', '⣻', '⢿', '⡿', '⣟', '⣯', '⣷', '⣾', '⣽',
        '⣻', '⢿', '⡿', '⣟', '⣯', '⣷', '⣾', '⣽', '⣻', '⢿', '⡿', '⣟', '⣯',
        '⣷', '⣾', '⣽', '⣻', '⢿', '⡿', '⣟', '⣯', '⣷', '⣾', '⣽', '⣻', '⢿',
        '⡿', '⣟', '⣯', '⣷'],
        SPIN5: ['⠁', '⠂', '⠄', '⡀', '⢀', '⠠', '⠐', '⠈', '⠁', '⠂',
        '⠄', '⡀', '⢀', '⠠', '⠐', '⠈', '⠁', '⠂', '⠄', '⡀', '⢀', '⠠', '⠐',
        '⠈', '⠁', '⠂', '⠄', '⡀', '⢀', '⠠', '⠐', '⠈', '⠁', '⠂', '⠄', '⡀',
        '⢀', '⠠', '⠐', '⠈'],
        SPIN6: ['⣀', '⡀', '⠄', '⡈', '⠐', '⠈', '⠄', '⡀', '⣀', '⡀',
        '⠄', '⡈', '⠐', '⠈', '⠄', '⡀', '⣀', '⡀', '⠄', '⡈', '⠐', '⠈', '⠄',
        '⡀', '⣀', '⡀', '⠄', '⡈', '⠐', '⠈', '⠄', '⡀', '⣀', '⡀', '⠄', '⡈',
        '⠐', '⠈', '⠄', '⡀'],
        SPIN7: ['▔', '▕', '▖', '▗', '▘', '▙', '▚', '▛', '▜', '▝',
        '▞', '▟', '▔', '▕', '▖', '▗', '▘', '▙', '▚', '▛', '▜', '▝', '▞',
        '▟', '▔', '▕', '▖', '▗', '▘', '▙', '▚', '▛', '▜', '▝', '▞', '▟']

        WAVE1: ['▁', '▂', '▃', '▄', '▅', '▆', '▇', '█'],
        WAVE2: ['▏', '▎', '▍', '▌', '▋', '▊', '▉', '█'],
        WAVE3: ['▔', '▕', '▖', '▗', '▘', '▙', '▚', '▛', '▜', '▝',
        '▞', '▟'],
        WAVE4: ['⣀', '⡀', '⠄', '⡈', '⠐', '⠈', '⠄', '⡀'],
        WAVE5: ['⣠', '⣤', '⣶', '⣾', '⣿'],
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

```
CLASSES
    EnterExit(builtins.object)
        bar
        spin
        timed
        wave

        class bar(EnterExit)
         |  bar(length, char='█', text='')
         |  
         |  Method resolution order:
         |      bar
         |      EnterExit
         |      builtins.object
         |  
         |  Methods defined here:
         |  
         |  __init__(self, length, char='█', text='')
         |      Initialize self.  See help(type(self)) for accurate s
    ignature.
         |  
         |  crash(self, message)
         |  
         |  print_bar(self)
         |  
         |  run(self, sleep=0.1, method=None, *method_args, **method_
    kwargs)
         |  
         |  sleep(self, seconds=0.1)
         |  
         |  stop(self)
         |  
         |  update(self, progress)
         |  
         |  update_bar(self)
         |  
          |  ----------------------------------------------------------------------
          |  Static methods defined here:
          |  
          |  multi(*loading_bars, sleep=0.1)
          |  
          |  ----------------------------------------------------------------------
          |  Methods inherited from EnterExit:
          |  
          |  __enter__(self)
          |  
          |  __exit__(self, exc_type, exc_value, traceback)
          |  
          |  ----------------------------------------------------------------------
          |  Data descriptors inherited from EnterExit:
          |  
          |  __dict__
          |      dictionary for instance variables (if defined)
          |  
          |  __weakref__
          |      list of weak references to the object (if defined)

                                                            class spin(EnterExit)
                                                             |  spin(total, chars=['|', '/', '-', '\\', '|', '/', '-', '\
                                                        \', '|', '/', '-', '\\', '|', '/', '-', '\\', '|', '/', '-', '\\'
                                                        , '|', '/', '-', '\\'], text='')
                                                             |  
                                                             |  Method resolution order:
                                                             |      spin
                                                             |      EnterExit
                                                             |      builtins.object
                                                             |  
                                                             |  Methods defined here:
                                                             |  
                                                             |  __init__(self, total, chars=['|', '/', '-', '\\', '|', '/
                                                        ', '-', '\\', '|', '/', '-', '\\', '|', '/', '-', '\\', '|', '/',
                                                         '-', '\\', '|', '/', '-', '\\'], text='')
                                                             |      Initialize self.  See help(type(self)) for accurate s
                                                        ignature.
                                                             |  
                                                             |  crash(self, message)
                                                             |  
                                                             |  print_spin(self)
                                                             |  
                                                             |  run(self, sleep=0.1, method=None, *method_args, **method_
                                                        kwargs)
                                                             |  
                                                             |  sleep(self, seconds=0.1)
                                                             |  
                                                             |  stop(self)
                                                             |  
                                                             |  update(self, progress)
                                                             |  
                                                             |  update_spin(self)
    |  
         |  ---------------------------------------------------------
    -------------
         |  Static methods defined here:
         |  
         |  multi(*spinning_objects, sleep=0.1)
         |  
         |  ---------------------------------------------------------
    -------------
         |  Methods inherited from EnterExit:
         |  
         |  __enter__(self)
         |  
         |  __exit__(self, exc_type, exc_value, traceback)
         |  
         |  ---------------------------------------------------------
    -------------
         |  Data descriptors inherited from EnterExit:
         |  
         |  __dict__
         |      dictionary for instance variables (if defined)
         |  
         |  __weakref__
         |      list of weak references to the object (if defined)

            class timed(EnterExit)
             |  timed(length, text='')
             |  
             |  Method resolution order:
             |      timed
             |      EnterExit
             |      builtins.object
             |  
             |  Methods defined here:
             |  
             |  __init__(self, length, text='')
             |      Initialize self.  See help(type(self)) for accurate s
        ignature.
             |  
             |  crash(self, message)
             |  
             |  print_timer(self)
             |  
             |  run(self, sleep=0.1)
             |  
             |  sleep(self, seconds=0.1)
             |  
             |  stop(self)
             |  
             |  update(self)
             |  
                  |  ---------------------------------------------------------
             -------------
                  |  Static methods defined here:
                  |  
                  |  multi(*timed_objects, sleep=0.1)
                  |  
                  |  ---------------------------------------------------------
             -------------
                  |  Methods inherited from EnterExit:
                  |  
                  |  __enter__(self)
                  |  
                  |  __exit__(self, exc_type, exc_value, traceback)
                  |  
                  |  ---------------------------------------------------------
             -------------
                  |  Data descriptors inherited from EnterExit:
                  |  
                  |  __dict__
                  |      dictionary for instance variables (if defined)
                  |  
                  |  __weakref__
                  |      list of weak references to the object (if defined)

            class wave(EnterExit)
             |  wave(length, chars=['▁', '▂', '▃', '▄', '▅', '▆', '▇', '█
        '], text='')
             |  
             |  Method resolution order:
             |      wave
             |      EnterExit
             |      builtins.object
             |  
             |  Methods defined here:
             |  
             |  __init__(self, length, chars=['▁', '▂', '▃', '▄', '▅', '▆
        ', '▇', '█'], text='')
             |      Initialize self.  See help(type(self)) for accurate s
        ignature.
             |  
             |  crash(self, message)
             |  
             |  print_wave(self)
             |  
             |  run(self, sleep=0.1)
             |  
             |  sleep(self, seconds=0.1)
             |  
             |  stop(self)
             |  
             |  update(self, progress)
            |  
                 |  ---------------------------------------------------------
            -------------
                 |  Static methods defined here:
                 |  
                 |  multi(*wave_objects, sleep=0.1)
                 |  
                 |  ---------------------------------------------------------
            -------------
                 |  Methods inherited from EnterExit:
                 |  
                 |  __enter__(self)
                 |  
                 |  __exit__(self, exc_type, exc_value, traceback)
                 |  
                 |  ---------------------------------------------------------
            -------------
                 |  Data descriptors inherited from EnterExit:
                 |  
                 |  __dict__
                 |      dictionary for instance variables (if defined)
                 |  
                 |  __weakref__
                 |      list of weak references to the object (if defined)

DATA
    __all__ = ['bar', 'spin', 'wave', 'timed']
    __copyright__ = 'Copyright (c) 2023 loado'
    __license__ = 'MIT'

VERSION
    5.8.0

AUTHOR
    loado
```
