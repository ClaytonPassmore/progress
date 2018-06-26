import math

from iterable_progress_counter import IterableProgressCounter


class ProgressBar(IterableProgressCounter):
    def __init__(self, iterator, **kwargs):
        self.percentage_format = kwargs.get('percentage_format', '{:>5.1f}%')

        # Default override.
        kwargs['progress_format'] = kwargs.get('progress_format', '{percentage} {bar}')
        super().__init__(iterator, **kwargs)

    def renderable_components(self):
        return ['percentage'] + super().renderable_components()

    def percentage(self):
        percentage = 1.00
        if self.total > 0:
            percentage = self.count / float(self.total)

        return percentage

    def render_percentage(self, width):
        percentage = self.percentage() * 100
        return self.percentage_format.format(percentage)

    def render_bar(self, width):
        non_component_width = len(self.bar_format.format(''))
        bar_width = width - non_component_width

        mark_width_format = '{{:<{}}}'.format(bar_width)
        bar_format_with_width = self.bar_format.format(mark_width_format)

        number_of_marks = math.floor(self.percentage() * bar_width)
        return bar_format_with_width.format(self.mark * number_of_marks)
