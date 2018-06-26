# Progress

A simple command line progress bar library for Python 3.

## Installation

Just use pip!

```bash
git clone git@github.com:ClaytonPassmore/progress.git
pip install ./progress
```

## Usage

Track progress while looping over a range.

```python
from progress import progress_range

for i in progress_range(10, -2, -2):
  process(i)
```

Track progress while looping over an iterable object.

```python
from glob import glob
from progress import progress_bar

filenames = glob('*')

for filename in progress_bar(filenames):
  process(filename)
```

Track progress for an undefined quantity.

```python
from progress import progress_counter

progress = progress_counter()

while(True):
  process()
  progress.tick()
```
