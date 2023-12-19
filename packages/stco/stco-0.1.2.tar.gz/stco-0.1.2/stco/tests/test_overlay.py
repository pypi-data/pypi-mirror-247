#!/usr/bin/env python
# -*- coding: utf-8 -*-

# MIT License
#
# Copyright (c) 2023 Luke Zaruba
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""test_overlay.py: Testing for stco/overlay.py - should be run from ./tests using `python -m unittest -v test_overlay.py`"""

import sys
import unittest
from pathlib import Path

from geopandas import GeoDataFrame
from shapely import Polygon

sys.path.append(str(Path(__file__).parent.parent.parent))

from stco.overlay import simple_overlay, stcec, weighted_overlay  # noqa: E402


class TestSimpleOverlay(unittest.TestCase):
    def setUp(self):
        # Data
        polygon_1 = Polygon(
            ((0.0, 0.0), (0.0, 1.0), (1.0, 1.0), (1.0, 0.0), (0.0, 0.0))
        )
        polygon_2 = Polygon(
            ((0.5, 0.0), (0.5, 1.0), (1.5, 1.0), (1.5, 0.0), (0.5, 0.0))
        )
        polygon_3 = Polygon(
            ((0.5, 0.5), (0.5, 1.5), (1.5, 1.5), (1.5, 0.5), (0.5, 0.5))
        )

        data = {
            "PERIOD": ["2021", "2022", "2023"],
            "geometry": [polygon_1, polygon_2, polygon_3],
        }

        self.gdf = GeoDataFrame(data)
        self.wkt_solu = "POLYGON ((0 0, 0 1, 0.5 1, 0.5 0.5, 0.5 0, 0 0))"
        self.count_solu = 1

    def test_simple_overlay(self):
        # Run Simple Overlay
        simple_overlay_output = simple_overlay(self.gdf)

        # Assert
        self.assertEqual(simple_overlay_output.iloc[0]["geometry"].wkt, self.wkt_solu)
        self.assertEqual(simple_overlay_output.iloc[0]["COUNT"], self.count_solu)


class TestSTCEC(unittest.TestCase):
    def setUp(self):
        # Data
        polygon_1 = Polygon(
            ((0.0, 0.0), (0.0, 1.0), (1.0, 1.0), (1.0, 0.0), (0.0, 0.0))
        )
        polygon_2 = Polygon(
            ((0.5, 0.0), (0.5, 1.0), (1.5, 1.0), (1.5, 0.0), (0.5, 0.0))
        )
        polygon_3 = Polygon(
            ((0.5, 0.5), (0.5, 1.5), (1.5, 1.5), (1.5, 0.5), (0.5, 0.5))
        )

        data = {
            "PERIOD": ["2021", "2022", "2023"],
            "geometry": [polygon_1, polygon_2, polygon_3],
        }

        self.gdf = GeoDataFrame(data)
        self.wkt_solu = "POLYGON ((0 0, 0 1, 0.5 1, 0.5 0.5, 0.5 0, 0 0))"
        self.stcec_solu = "SPORADIC"

    def test_stcec(self):
        # Run STCEC
        stcec_output = stcec(self.gdf)

        # Assert
        self.assertEqual(stcec_output.iloc[0]["geometry"].wkt, self.wkt_solu)
        self.assertEqual(stcec_output.iloc[0]["STCEC"], self.stcec_solu)


class TestWeightedOverlay(unittest.TestCase):
    def setUp(self):
        # Data
        polygon_1 = Polygon(
            ((0.0, 0.0), (0.0, 1.0), (1.0, 1.0), (1.0, 0.0), (0.0, 0.0))
        )
        polygon_2 = Polygon(
            ((0.5, 0.0), (0.5, 1.0), (1.5, 1.0), (1.5, 0.0), (0.5, 0.0))
        )
        polygon_3 = Polygon(
            ((0.5, 0.5), (0.5, 1.5), (1.5, 1.5), (1.5, 0.5), (0.5, 0.5))
        )

        data = {
            "PERIOD": ["2021", "2022", "2023"],
            "geometry": [polygon_1, polygon_2, polygon_3],
        }

        self.gdf = GeoDataFrame(data)
        self.wkt_solu = "POLYGON ((0 0, 0 1, 0.5 1, 0.5 0.5, 0.5 0, 0 0))"
        self.weight_solu = 0.167

    def test_simple_overlay(self):
        # Run Weighted Overlay
        weighted_overlay_output = weighted_overlay(self.gdf)

        # Assert
        self.assertEqual(weighted_overlay_output.iloc[0]["geometry"].wkt, self.wkt_solu)
        self.assertEqual(
            round(weighted_overlay_output.iloc[0]["WEIGHT"], 3), self.weight_solu
        )


suite = unittest.TestSuite()
for i in [TestSimpleOverlay, TestSTCEC, TestWeightedOverlay]:
    a = unittest.TestLoader().loadTestsFromTestCase(i)
    suite.addTest(a)

if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    runner.run(suite)
