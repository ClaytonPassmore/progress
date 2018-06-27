import math

from .progress_counter import ProgressCounter


class IterableProgressCounter(ProgressCounter):
    def __init__(self, iterable, **kwargs):
        self.iterable = iter(iterable)
        self.total = self.computed_total(iterable)

        self.message = kwargs.get('message', None)
        self.total_format = kwargs.get('total_format', '{}')

        # Default override.
        kwargs['progress_format'] = kwargs.get('progress_format', 'Processed: {count}/{total} {bar}')
        super().__init__(**kwargs)

    def __iter__(self):
        return self

    def __next__(self):
        try:
            next_value = next(self.iterable)
            self.tick()
            return next_value
        except StopIteration:
            self.render_completed(self.computed_width())
            raise

    def computed_total(self, iterable):
        try:
            return len(iterable)
        except TypeError:
            return math.inf

    def render_completed(self, width):
        if self.message is None:
            self.stream.write('\n')
            return

        message_format = '{{:<{}}}'.format(width)
        formatted_message = message_format.format(self.message)
        self.stream.write('\r{}\n'.format(formatted_message))

    def render_total(self, width):
        renderable_total = 'Unknown' if self.total == math.inf else self.total
        return self.total_format.format(renderable_total)

    def renderable_components(self):
        return ['total'] + super().renderable_components()
