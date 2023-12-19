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

"""overlay.py: Overlay analyses for use on clusters of footprints from periods ("snapshots") of time to assess the temporal stability of clusters."""

import math

from geopandas import GeoDataFrame, sjoin
from pandas import merge
from shapely.ops import polygonize


def weighted_overlay(footprints: GeoDataFrame) -> GeoDataFrame:
    """
    Overlay approach that takes time into account and weights more recent clusters at a higher level than less recent clusters.

    Computed as the period index divided by the sum of all period indexes.

    Args:
        footprints (GeoDataFrame): Input polygon fetaures from TemporalADBSCAN.

    Returns:
        GeoDataFrame: Output polygons features.
    """
    # Reset Index
    footprints.reset_index(inplace=True)

    # Find Unique Periods & Sort
    unique_periods = [str(i) for i in footprints.PERIOD.unique()]
    unique_periods.sort()

    # Create Dictionary of Periods & Indexes
    period_indexes = {}

    for index, value in enumerate(unique_periods):
        period_indexes[value] = index + 1

    # Calculate Sum of Indexes
    index_sum = sum(list(period_indexes.values()))

    # Compute Weights in DF
    footprints["weight"] = 0.0

    for index, row in footprints.iterrows():
        footprints.at[index, "weight"] = period_indexes[row["PERIOD"]] / index_sum

    # Find Bounds of Footprints & Convert to New GDF
    bounds = footprints.geometry.exterior.unary_union
    polygons = GeoDataFrame(geometry=list(polygonize(bounds)), crs=footprints.crs)
    polygons["OID"] = range(len(polygons))

    # Get Centroids
    polygons_centroid = polygons.copy()
    polygons_centroid["geometry"] = polygons.centroid

    # Spatial Join & Counting
    counts = sjoin(polygons_centroid, footprints)
    counts = counts.groupby(["OID"])["weight"].sum().rename("WEIGHT").reset_index()

    # Return GeoDataFrame with Counts
    return merge(polygons, counts)


def simple_overlay(footprints: GeoDataFrame) -> GeoDataFrame:
    """
    Overlay approach that finds overlapping polygons and calculates the feature count for each intersecting area.

    Args:
        footprints (GeoDataFrame): Input polygon fetaures from TemporalADBSCAN.

    Returns:
        GeoDataFrame: Output polygons features.
    """
    # Find Bounds of Footprints & Convert to New GDF
    bounds = footprints.geometry.exterior.unary_union
    polygons = GeoDataFrame(geometry=list(polygonize(bounds)), crs=footprints.crs)
    polygons["OID"] = range(len(polygons))

    # Get Centroids
    polygons_centroid = polygons.copy()
    polygons_centroid["geometry"] = polygons.centroid

    # Spatial Join & Counting
    counts = sjoin(polygons_centroid, footprints)
    counts = (
        counts.groupby(["OID"])["index_right"].count().rename("COUNT").reset_index()
    )

    # Return GeoDataFrame with Counts
    return merge(polygons, counts)


def _calculate_cluster_time_indexes(footprints: GeoDataFrame) -> GeoDataFrame:
    """
    Function to create list of time series indexes where cluster was defined as cluster and store back into GDF.

    Args:
        footprints (GeoDataFrame): Input polygon features.

    Returns:
        GeoDataFrame: Output polygon features with time index lists.
    """
    # Reset Index
    footprints = footprints.reset_index(drop=True)

    # Find Unique Periods & Sort
    unique_periods = [str(i) for i in footprints["PERIOD"].unique()]
    unique_periods.sort()

    # Create Dictionary of Periods & Indexes
    period_indexes = {}

    for index, value in enumerate(unique_periods):
        period_indexes[value] = index + 1

    # Compute Weights in DF
    footprints["index"] = 0.0

    for index, row in footprints.iterrows():
        footprints.at[index, "index"] = period_indexes[row["PERIOD"]]

    # Find Bounds of Footprints & Convert to New GDF
    bounds = footprints.geometry.exterior.unary_union
    polygons = GeoDataFrame(geometry=list(polygonize(bounds)), crs=footprints.crs)
    polygons["OID"] = range(len(polygons))

    # Get Centroids
    polygons_centroid = polygons.copy()
    polygons_centroid["geometry"] = polygons.centroid

    # Spatial Join
    counts = sjoin(polygons_centroid, footprints)

    # Find Indexes for Each Cluster & Store in Dict
    cluster_index_dict = {}

    for oid in counts.OID.unique():
        oid_indexes = list(counts.loc[counts["OID"] == oid]["index"])

        oid_indexes = [int(i) for i in oid_indexes]

        oid_indexes.sort()

        cluster_index_dict[oid] = oid_indexes

    # Create New Column with Empty List for Each Row
    polygons["index_list"] = [[] for _ in range(len(polygons))]

    # Update Column to List of Indexes where included as Cluster
    for index, row in polygons.iterrows():
        try:
            polygons.at[index, "index_list"] = cluster_index_dict[row["OID"]]
        except KeyError:
            print(f"KeyError: {row['OID']} not found")
            polygons.at[index, "index_list"] = []

    # Return
    return polygons, list(period_indexes.values())


def stcec(footprints: GeoDataFrame, significance_percent: float = 0.9) -> GeoDataFrame:
    """
    Function to classify index list of a given cluster area into an STCEC classification.

    Args:
        footprints (GeoDataFrame): Input polygon features.
        significance_percent (float, optional): Percentage used to determine temporal significance of long lasting clusters. Defaults to 0.9.

    Returns:
        GeoDataFrame: Output polygon features with STCEC classes.
    """
    # Create List of Indexes
    footprints_new, indexes = _calculate_cluster_time_indexes(footprints)

    # Index Stats
    indexes.sort()

    total_indexes = len(indexes)
    significance_length = math.ceil(total_indexes * significance_percent)

    most_recent_index = indexes[-1:][0]
    second_most_recent_index = indexes[-2:-1][0]

    # Classification
    footprints_new["STCEC"] = ""

    for index, row in footprints_new.iterrows():
        # Get List of Indexes for each row
        index_list = row["index_list"]

        index_list.sort()

        # Checks for Determining STCEC Class
        if len(index_list) >= significance_length:
            if most_recent_index in index_list:
                value = "PERSISTENT"
            else:
                value = "HISTORICAL"
        else:
            if len(index_list) == 1:
                if most_recent_index in index_list:
                    value = "NEW"
                else:
                    value = "SPORADIC"
            else:
                if (
                    most_recent_index in index_list
                    and second_most_recent_index in index_list
                ):
                    value = "INTENSIFYING"
                else:
                    for i in range(len(index_list)):
                        try:
                            consecutive = index_list[i] + 1 == index_list[i + 1]
                            if consecutive:
                                value = "DIMINISHING"
                                break
                        except IndexError:
                            value = "OCCASIONAL"

        # Set STCEC Value
        footprints_new.at[index, "STCEC"] = value

    # Return new GDF
    return footprints_new
