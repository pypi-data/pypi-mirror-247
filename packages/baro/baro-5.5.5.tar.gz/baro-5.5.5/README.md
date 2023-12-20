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