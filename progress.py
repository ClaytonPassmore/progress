import math
import shutil
import sys


class ProgressRange(object):
    def __init__(self, *args, out=sys.stdout, digits=0, mark='#', message=None, finished_message=None):
        self.range = range(*args)
        self.iter = iter(self.range)
        self.progress = -1
        self.total = len(self.range)
        self.width = shutil.get_terminal_size().columns
        self.out = out
        self.digits = digits
        self.mark = mark
        self.message = message
        self.finished_message = finished_message

    def __iter__(self):
        return self

    def __next__(self):
        # Need to check terminal size incase it changed.
        self.width = shutil.get_terminal_size().columns

        self.progress += 1
        progress_string = '{} {}'.format(self.percentage_string(), self.bar())

        if self.message is not None:
            progress_string = '{} {}'.format(self.message, progress_string)

        self.out.write('\r' + progress_string)

        try:
            return next(self.iter)
        except:
            self.out.write(self.finished_message_string())
            raise

    def finished_message_string(self):
        if self.finished_message is None:
            return '\n'

        finished_string = '\r{{:{}}}\n'.format(self.width)
        return finished_string.format(self.finished_message)


    def bar_string_width(self):
        bar_width = self.width - (self.percentage_string_width() + 1)
        bar_width -= 2  # For ends

        if self.message is not None:
            bar_width -= (len(self.message) + 1)

        if bar_width < 0:
            bar_width = 0

        return bar_width

    def bar(self):
        bar_width = self.bar_string_width()
        number_of_marks = math.floor(self.percentage() * bar_width)

        bar = '[{{:<{}}}]'.format(bar_width)
        return bar.format(self.mark * number_of_marks)

    def percentage(self):
        if self.total <= 0:
            return 1.00

        return self.progress / float(self.total)

    def percentage_string(self):
        percentage = 100 * self.percentage()

        # Technically could be rounding up here when I should be rounding down.
        if self.digits > 0:
            percentage = round(percentage, self.digits)
        else:
            percentage = int(math.floor(percentage))

        # Subtract 1 for the % sign.
        string_width = self.percentage_string_width() - 1

        # Format right for the given width and precision.
        percentage_string = '{{:>{}.{}f}}%'.format(string_width, self.digits)
        return percentage_string.format(percentage)

    def percentage_string_width(self):
        # 3 characters plus % sign.
        percentage_width = 4

        if self.digits > 0:
            # Decimal point plus digits
            percentage_width += (1 + self.digits)

        return percentage_width

