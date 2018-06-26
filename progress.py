import math
import shutil
import sys


class Progress(object):
    def __init__(self, *args, **kwargs):
        self.bar_mark = kwargs.get('bar_mark', '#')
        self.bar_format = kwargs.get('bar_format', '[{}]')
        self.message = kwargs.get('message', None)
        self.percentage_format = kwargs.get('percentage_format', '{:>5.1f}%')
        self.render_order = kwargs.get('render_order', ['percentage', 'bar'])
        self.progress_format = kwargs.get('progress_format', '{percentage} {bar}')
        self.stream = kwargs.get('stream', sys.stdout)
        self.width = kwargs.get('width', None)
        self.total = kwargs.get('total', None)

        self.progress = -1

    def computed_width(self):
        return self.width or shutil.get_terminal_size().columns

    def tick(self):
        self.progress += 1
        return self.render()

    def render(self):
        rendered_components = {
            'percentage': '',
            'description': '',
            'bar': ''
        }

        non_component_widths = len(self.progress_format.format(**rendered_components))
        remaining_width = self.computed_width() - non_component_widths

        # Call formatters in order of priority.
        for component in self.render_order:
            render_func = getattr(self, 'render_{}'.format(component))
            rendered_components[component] = render_func(remaining_width)
            remaining_width -= len(rendered_components[component])

        return self.progress_format.format(**rendered_components)

    def percentage(self):
        if self.total is None:
            raise Exception('Total is undefined')

        percentage = 1.00
        if self.total > 0:
            percentage = self.progress / float(self.total)

        return percentage

    def render_percentage(self, width):
        percentage = self.percentage() * 100
        return self.percentage_format.format(percentage)

    def render_bar(self, width):
        non_component_width = len(self.bar_format.format(''))
        mark_width = width - non_component_width

        mark_width_format = '{{:<{}}}'.format(mark_width)
        bar_format_with_width = self.bar_format.format(mark_width_format)

        number_of_marks = math.floor(self.percentage() * mark_width)
        return bar_format_with_width.format(self.bar_mark * number_of_marks)
