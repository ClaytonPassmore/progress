from sys import stdout, stderr
from unittest import TestCase
from unittest.mock import patch, MagicMock
from random import randint

from progress import progress

class MockGetTerminalSize(object):
    columns = randint(0, 100)
    rows = randint(0, 100)

class TestProgressArguments(TestCase):
    @patch('sys.stdout.write')
    def test_defaults(self, mock_stdout):
        subject = progress()
        self.assertEqual(subject.count_format, '{:>5}')
        self.assertEqual(subject.render_order, subject.renderable_components())
        self.assertEqual(subject.progress_format, 'Processed: {count}')
        self.assertEqual(subject.stream, stdout)
        self.assertEqual(subject.width, None)

        # Computed from args.
        self.assertEqual(subject.computed_render_order, ['count'])

    @patch('sys.stderr.write')
    def test_overrides(self, mock_stderr):
        subject = progress(
            count_format='yolo {}',
            render_order=['bar'],
            progress_format='foo',
            stream=stderr,
            width=50
        )
        self.assertEqual(subject.count_format, 'yolo {}')
        self.assertEqual(subject.render_order, ['bar'])
        self.assertEqual(subject.progress_format, 'foo')
        self.assertEqual(subject.stream, stderr)
        self.assertEqual(subject.width, 50)

        # Computed from args.
        self.assertEqual(subject.computed_render_order, [])

@patch('sys.stdout.write')
class TestProgress(TestCase):
    @patch('shutil.get_terminal_size', return_value=MockGetTerminalSize())
    def test_computed_width_unspecified_width(self, mock_get_terminal_size, mock_stdout):
        subject = progress()
        self.assertEqual(subject.compute_width(), mock_get_terminal_size().columns)

    def test_computed_width_specified_width(self, mock_stdout):
        width = randint(0, 100)
        subject = progress(width=width)
        self.assertEqual(subject.compute_width(), width)

    def test_tick(self, mock_stdout):
        subject = progress()
        subject.write = MagicMock()

        self.assertEqual(subject.count, 0)
        subject.tick()
        self.assertEqual(subject.count, 1)
        subject.write.assert_called_once_with()

    def test_reset(self, mock_stdout):
        subject = progress()
        subject.count = 5
        subject.write = MagicMock()

        self.assertEqual(subject.count, 5)
        subject.reset()
        self.assertEqual(subject.count, 0)
        subject.write.assert_called_once_with()

    def test_write(self, mock_stdout):
        subject = progress()
        subject.write()
        mock_stdout.assert_called_with('\r' + subject.render())

    def test_renderable_components(self, mock_stdout):
        subject = progress()
        self.assertEqual(subject.renderable_components(), ['count'])

    def test_render_count(self, mock_stdout):
        subject = progress()
        width = randint(0, 100)
        subject.count = randint(0, 100)

        expected_render = subject.count_format.format(subject.count)
        self.assertEqual(subject.render_count(width), expected_render)

        subject.count_format = '{:>10}'
        expected_render = subject.count_format.format(subject.count)
        self.assertEqual(subject.render_count(width), expected_render)

    def test_compute_render_order(self, mock_stdout):
        render_order = ['count', 'foo', 'bar']
        subject = progress(render_order=render_order)

        subject.progress_format = '{bar} {foo} {count}'
        self.assertEqual(subject.compute_render_order(), render_order)

        subject.progress_format = ''
        self.assertEqual(subject.compute_render_order(), [])

        subject.progress_format = '{bar} {bazz} {foo}'
        self.assertEqual(subject.compute_render_order(), ['foo', 'bar'])

    def test_blank_components(self, mock_stdout):
        subject = progress()
        subject.renderable_components = MagicMock(return_value=['foo', 'bar', 'buzz'])

        self.assertEqual(subject.blank_components(), {
            'foo': '',
            'bar': '',
            'buzz': ''
        })

    def test_render(self, mock_stdout):
        subject = progress()
        subject.computed_render_order = ['foo', 'bar', 'bazz']
        subject.renderable_components = MagicMock(return_value=['foo', 'bar', 'bazz'])
        subject.progress_format = '{bazz} {foo} {bar}'
        subject.compute_width = MagicMock(return_value=100)
        subject.render_foo = MagicMock(return_value='foo')
        subject.render_bar = MagicMock(return_value='bar')
        subject.render_bazz = MagicMock(return_value='bazz')

        self.assertEqual(subject.render(), 'bazz foo bar')
        subject.render_foo.assert_called_once_with(100 - 2)
        subject.render_bar.assert_called_once_with(100 - 2 - 3)
        subject.render_bazz.assert_called_once_with(100 - 2 - 3 - 3)
