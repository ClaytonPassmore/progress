import shutil
import string
import sys


class Progress(object):
    def __init__(self, **kwargs):
        self.count_format = kwargs.get('count_format', '{:>5}')
        self.render_order = kwargs.get('render_order', self.renderable_components())
        self.progress_format = kwargs.get('progress_format', 'Processed: {count}')
        self.stream = kwargs.get('stream', sys.stdout)
        self.width = kwargs.get('width', None)

        # Pre-compute instead of doing it on each render.
        self.computed_render_order = self.compute_render_order()

        # Sets initial state.
        self.reset()

    def compute_render_order(self):
        # Figure out which components we need to render.
        components_to_render = [x[1] for x in string.Formatter().parse(self.progress_format)]
        return list(filter(lambda comp: comp in components_to_render, self.render_order))

    def compute_width(self):
        return self.width or shutil.get_terminal_size().columns

    def tick(self):
        self.count += 1
        self.write()

    def reset(self):
        self.count = 0
        self.write()

    def write(self):
        self.stream.write('\r' + self.render())

    def renderable_components(self):
        return ['count']

    def blank_components(self):
        # Create a dictionary of renderable components with empty strings as the
        # default for each component until it gets rendered.
        return dict((comp, '') for comp in self.renderable_components())

    def render(self):
        rendered_components = self.blank_components()

        non_component_widths = len(self.progress_format.format(**rendered_components))
        remaining_width = self.compute_width() - non_component_widths

        # Call formatters in order of priority.
        for component in self.computed_render_order:
            render_func = getattr(self, 'render_{}'.format(component))
            rendered_components[component] = render_func(remaining_width)
            remaining_width -= len(rendered_components[component])

        return self.progress_format.format(**rendered_components)

    def render_count(self, width):
        return self.count_format.format(self.count)
