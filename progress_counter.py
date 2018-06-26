import math

from progress import Progress


class ProgressCounter(Progress):
    def __init__(self, **kwargs):
        self.bar_format = kwargs.get('bar_format', '[{}]')
        self.mark = kwargs.get('mark', '#')
        self.mark_proportion = kwargs.get('mark_proportion', 30)

        # Default override
        kwargs['progress_format'] = kwargs.get('progress_format', 'Processed: {count} {bar}')
        super().__init__(**kwargs)

    def renderable_components(self):
        return super().renderable_components() + ['bar']

    def render_bar(self, width):
        non_component_width = len(self.bar_format.format(''))
        bar_width = width - non_component_width

        if width <= 0:
            return ''

        number_of_marks = int(math.floor(bar_width * float(self.mark_proportion) / 100.0))
        marks = self.mark * number_of_marks

        whitespace = bar_width - number_of_marks
        left_whitespace = ' ' * (self.count % (whitespace))

        mark_format = '{{:<{}}}'.format(bar_width)
        mark_space = mark_format.format(left_whitespace + marks)

        return self.bar_format.format(mark_space)
