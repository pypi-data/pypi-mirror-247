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
    bar.step(1)

bar.close()

# Option 3
with baro(total=100, 'Setting up..', type=baro.SPIN) as bar:
    # Do something
    for iter in bar:
        # Do something
        bar.step(1)
```

```javascript
CLASSES:
    baro.baro,
    baro.fore (Contains fore colors for coloring text),
    baro.style (Contains style ie. BOLD for styling text),
    baro.back (Contains the colors for the background of the text)

METHODS:
    baro.color(
        color: fore (Default none), 
        style: style (Default none),
        back: back (Default none)
    )
    baro.reset() Returns the defualt color, style, and back.
```