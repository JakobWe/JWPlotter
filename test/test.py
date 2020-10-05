import unittest
import plotter.PlotImplementations as PlotImplementations


class TestStringMethods(unittest.TestCase):

    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_PlotImplementation(self):
        class_under_test = PlotImplementations.AppendPlot("title")


if __name__ == '__main__':
    unittest.main()
