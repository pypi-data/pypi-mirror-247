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

"""test_clustering.py: Testing for stco/clustering.py - should be run from ./tests using `python -m unittest -v test_clustering.py`"""

import sys
import unittest
from pathlib import Path

from geopandas import GeoDataFrame, points_from_xy
from numpy.random import seed
from pandas import DataFrame, concat, to_datetime
from shapely import Polygon
from sklearn.datasets import make_blobs

sys.path.append(str(Path(__file__).parent.parent.parent))

from stco.clustering import SnapshotADBSCAN  # noqa: E402


def _create_dataset():
    # Set of Blobs for Time Step 1
    X_1, _ = make_blobs(
        n_samples=100, centers=[[1, 1]], cluster_std=0.4, random_state=0
    )
    df_1 = DataFrame(
        {"X": [i[0] for i in X_1], "Y": [i[1] for i in X_1], "time": "01/01/2021"}
    )
    df_1["time"] = to_datetime(df_1["time"])
    gdf_1 = GeoDataFrame(df_1, geometry=points_from_xy(df_1["X"], df_1["Y"]))

    # Set of Blobs for Time Step 2
    X_2, _ = make_blobs(
        n_samples=100, centers=[[0.5, 0.75]], cluster_std=0.4, random_state=1
    )
    df_2 = DataFrame(
        {"X": [i[0] for i in X_2], "Y": [i[1] for i in X_2], "time": "01/01/2022"}
    )
    df_2["time"] = to_datetime(df_2["time"])
    gdf_2 = GeoDataFrame(df_2, geometry=points_from_xy(df_2["X"], df_2["Y"]))

    # Set of Blobs for Time Step 3
    X_3, _ = make_blobs(
        n_samples=100, centers=[[0.75, 1.5]], cluster_std=0.4, random_state=2
    )
    df_3 = DataFrame(
        {"X": [i[0] for i in X_3], "Y": [i[1] for i in X_3], "time": "01/01/2023"}
    )
    df_3["time"] = to_datetime(df_3["time"])
    gdf_3 = GeoDataFrame(df_3, geometry=points_from_xy(df_3["X"], df_3["Y"]))

    # Concat
    gdf = concat([gdf_1, gdf_2, gdf_3])

    return gdf


class TestSnapshotADBSCAN(unittest.TestCase):
    def setUp(self):
        # Data Set Up
        self.gdf = _create_dataset()
        seed(10)
        self.sabds = SnapshotADBSCAN(
            self.gdf, "Y", 0.5, 0.05, pct_exact=0.5, reps=50, keep_solus=True
        )

        # Solutions
        self.wkt_solu = "POLYGON ((0.7425526388668438 0.1106387391102293, 0.6448857009479549 0.2076814127104292, 0.5999138610441741 0.3820915612889553, 0.5805788139731629 0.4319928251284099, 0.4736370357953915 0.8153661580741164, 0.3544408609768194 0.9149038879144125, 0.3479206612135821 1.1851129022103097, 0.4918060006057066 1.3877586832632045, 0.3174919237499949 1.7803101580927159, 0.5307506379543361 1.777448474259717, 0.655509725978119 1.7640259812396135, 0.800787019723078 1.7718128215267943, 1.0042000082883282 1.7143481975623343, 1.3914951936422957 1.8963572796805832, 1.5953008775182398 1.7583556704122332, 1.769176810592154 1.5922059165737696, 1.8652943797122759 1.534611179774557, 1.953257909945577 1.3777917947961655, 1.7056209383870655 1.1600628833468893, 1.5976316292630424 0.9179366944936797, 1.747023196059987 0.6090888480494356, 1.907901849595043 0.418253730160494, 1.7532602788225018 0.4608963755430214, 1.4557602738173203 0.5060696718585389, 1.250092580410875 0.3591769377573009, 1.186264975892184 0.3855025254891105, 0.8584024354986064 0.4500194826327925, 0.7425526388668438 0.1106387391102293))"
        self.len_solu = 3

    def test_fit_all(self):
        # Run Fit
        footprints = self.sabds.fit_all()

        # Assert
        self.assertEqual(footprints.iloc[0]["geometry"].wkt, self.wkt_solu)
        self.assertEqual(len(footprints), self.len_solu)
