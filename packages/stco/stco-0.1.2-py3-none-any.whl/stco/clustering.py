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

"""clustering.py: Implementation of A-DBSCAN on periods ("snapshots") of a time series for use in subsequent overlay analyses."""

from math import pi, sqrt
from typing import Union

from esda.adbscan import ADBSCAN, get_cluster_boundary
from geopandas import GeoDataFrame
from pandas import DataFrame, concat, to_datetime
from tqdm import tqdm


class SnapshotADBSCAN:
    def __init__(
        self,
        data: Union[DataFrame, GeoDataFrame],
        period: str,
        eps: float,
        min_sample_pct: float,
        time_field: str = "time",
        x_field: str = "X",
        y_field: str = "Y",
        **kwargs,
    ) -> None:
        """
        Instantiates SnapshotADBSCAN object to run snapshot-based A-DBSCAN.

        Args:
            data (Union[DataFrame, GeoDataFrame]): Input point features.
            period (str): Pandas/NumPy Period alias.
            eps (float): Eps parameter for ADBSCAN, in the unit of the input dataset's coordinate system.
            min_sample_pct (float): Percentage of the total points within each period to use as the minimum samples parameter in ADBSCAN.
            time_field (str, optional): Name of time field in data. Defaults to "time".
            x_field (str, optional): Name of X coordinate field in data - not needed for GeoDataFrame inputs. Defaults to "X".
            y_field (str, optional): Name of Y coordinate field in data - not needed for GeoDataFrame inputs. Defaults to "Y".
        """
        if type(data) is GeoDataFrame:
            data = self._create_xy_series(data)
        self.data = self._check_data_types(data, time_field, x_field, y_field)
        self.period = self._check_period(period)
        self.eps = eps
        self.min_sample_pct = min_sample_pct
        self.time_field = time_field
        self.x_field = x_field
        self.y_field = y_field

        # Handling other kwargs
        self._adbscan_algorithm = kwargs.get("algorithm", "auto")
        self._adbscan_n_jobs = kwargs.get("n_jobs", 1)
        self._adbscan_pct_exact = kwargs.get("pct_exact", 0.1)
        self._adbscan_reps = kwargs.get("reps", 100)
        self._adbscan_keep_solus = kwargs.get("keep_solus", False)
        self._adbscan_pct_thr = kwargs.get("pct_thr", 0.9)

    @staticmethod
    def _check_period(period_value: str) -> str:
        """
        Method to check the validity of the period value passed in.

        Args:
            period_value (str): Period value to create "snapshots" with.

        Raises:
            ValueError: Raised when invalid period value is passed in.

        Returns:
            str: Period value, if valid.
        """
        valid_periods = [
            "Y",  # Annual
            "Q",  # Quarterly
            "M",  # Monthly
            "W",  # Weekly
            "D",  # Daily
            "H",  # Hourly
            "T",  # Minutely
        ]

        if period_value not in valid_periods:
            raise ValueError(
                f"Period must be one of following strings: {valid_periods}"
            )

        else:
            return period_value

    @staticmethod
    def _check_data_types(
        data: Union[DataFrame, GeoDataFrame],
        time_field: str,
        x_field: str,
        y_field: str,
    ) -> Union[DataFrame, GeoDataFrame]:
        """
        Method to check data types and attempt to fix any issues.

        Args:
            data (Union[DataFrame, GeoDataFrame]): Input point features.
            time_field (str): Name of time field in data.
            x_field (str): Name of X coordinate field in data.
            y_field (str): Name of Y coordinate field in data.

        Raises:
            TypeError: Raised when type of time field passed in in invalid.
            TypeError: Raised when type of X coordinate field passed in in invalid.
            TypeError: Raised when type of Y coordinate field passed in in invalid.

        Returns:
            Union[DataFrame, GeoDataFrame]: Output data, potentially updated with new types.
        """
        # Check Time
        if data[time_field].dtype.name != "datetime64[ns]":
            try:
                data[time_field] = to_datetime(data[time_field])
            except TypeError:
                print(
                    f"Series for Time field, {time_field}, must be of type 'datetime64[ns]'"
                )

        # Check X
        if data[x_field].dtype.name != "float64":
            try:
                data[x_field] = data[x_field].astype("float64")
            except TypeError:
                print(f"Series for X field, {x_field}, must be of type 'float64'")

        # Check Y
        if data[y_field].dtype.name != "float64":
            try:
                data[y_field] = data[y_field].astype("float64")
            except TypeError:
                print(f"Series for Y field, {y_field}, must be of type 'float64'")

        # Return updated version of data -- in case of casting
        return data

    @staticmethod
    def _create_xy_series(data: GeoDataFrame) -> GeoDataFrame:
        """
        Method to convert GeoDataFrame Point coordinates to X and Y series in GeoDataFrame.

        Args:
            data (GeoDataFrame): Input point features.

        Returns:
            GeoDataFrame: Output point features.
        """
        if "X" not in data.columns:
            data["X"] = data.geometry.x
        if "Y" not in data.columns:
            data["Y"] = data.geometry.y

        return data

    def _create_period(self) -> None:
        """
        Creates a new Series in the DataFrame containing the period of the record.
        """
        self.data["PERIOD"] = (
            self.data[self.time_field].dt.to_period(self.period).astype(str)
        )

    def fit_all(self) -> GeoDataFrame:
        """
        Method to fit model to data from all periods/snapshots of time, create cluster boundaries, and concatenate footprints results into single GeoDataFrame.

        Returns:
            GeoDataFrame: Output cluster footprints.
        """
        # Import Numba for Boundary Construction
        import numba

        # Create Periods
        self._create_period()

        # Create List of Empty Output GDFs
        footprint_df_list = []

        # Loop through Timesteps
        for step in tqdm(self.data.PERIOD.unique()):
            # Filter data
            filtered_data = self.data.loc[(self.data["PERIOD"] == step)].copy()

            # Fit Model
            abdscan = ADBSCAN(
                self.eps,
                filtered_data.shape[0] * self.min_sample_pct,
                self._adbscan_algorithm,
                self._adbscan_n_jobs,
                self._adbscan_pct_exact,
                self._adbscan_reps,
                self._adbscan_keep_solus,
                self._adbscan_pct_thr,
            )

            abdscan.fit(filtered_data)

            # Get Footprints
            footprints = get_cluster_boundary(abdscan.votes["lbls"], filtered_data)

            # Create Dictionary of Timestep Label & Footprints
            data = {"PERIOD": step, "geometry": footprints}

            # Convert to GDF & Append
            footprint_df_list.append(GeoDataFrame(data))

        # Concatenate GDFs
        return concat(footprint_df_list)
