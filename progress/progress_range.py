from .progress_bar import ProgressBar


class ProgressRange(ProgressBar):
    def __init__(self, *args, **kwargs):
        iterator = range(*args)
        super().__init__(iterator, **kwargs)
