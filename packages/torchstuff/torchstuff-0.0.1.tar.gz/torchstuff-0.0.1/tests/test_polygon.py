import unittest

import torch

from torchstuff.polygon import Polygon


class TestPolygon(unittest.TestCase):
    def setUp(self):
        self.vertices = torch.tensor([[0., 0.], [0., 1.], [1., 1.], [1., 0.], [0., 0.]], dtype=torch.float32)
        self.polygon = Polygon(self.vertices)

    def test_area(self):
        self.assertEqual(self.polygon.area, 1.0)

    def test_length(self):
        self.assertEqual(self.polygon.length, 4.0)


if __name__ == '__main__':
    unittest.main()