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

        # Sets initial state.
        self.reset()

    def computed_width(self):
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

    def render(self):
        # Create a dictionary of renderable components with empty strings as the
        # default for each component until it gets rendered.
        rendered_components = dict((comp, '') for comp in self.renderable_components())

        non_component_widths = len(self.progress_format.format(**rendered_components))
        remaining_width = self.computed_width() - non_component_widths

        # Figure out which components we need to render.
        components_to_render = [x[1] for x in string.Formatter().parse(self.progress_format)]
        render_order = filter(lambda comp: comp in components_to_render, self.render_order)

        # Call formatters in order of priority.
        for component in render_order:
            render_func = getattr(self, 'render_{}'.format(component))
            rendered_components[component] = render_func(remaining_width)
            remaining_width -= len(rendered_components[component])

        return self.progress_format.format(**rendered_components)

    def render_count(self, width):
        return self.count_format.format(self.count)
