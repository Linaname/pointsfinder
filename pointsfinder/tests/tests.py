import pointsfinder
from pointsfinder import app
from unittest import TestCase


class PointsfinderTest(TestCase):
    def setUp(self):
        data = ('-2.5 1 Tag1\n'
                '0 0 Tag2\n'
                '-4 -2 Tag3\n'
                '2 -3.5 Tag4\n'
                '4.5 4.5 Tag5\n'
                '0 1 Tag6\n'
                )
        self.finder = pointsfinder.PointSet(data)

    def test_find_neighbors_tags(self):
        self.assertCountEqual(self.finder.find_neighbors_tags(-2, -1, 2.3), ['Tag1', 'Tag2', 'Tag3'])
        self.assertCountEqual(self.finder.find_neighbors_tags(2.5, 5, 2), [])
        self.assertCountEqual(self.finder.find_neighbors_tags(2.5, 5, 4), ['Tag5'])

    def test_io_loop(self):
        input_values = ['-2 -1 2.3', 'WRONG', '2.5 5 2', 'exit']
        expected_output = ['Tag1, Tag2, Tag3', 'Input is incorrect', '']
        output = []
        app.input = lambda *args: input_values.pop(0)
        app.print = lambda arg: output.append(arg)
        self.finder.run_io_loop()
        self.assertListEqual(output, expected_output)
