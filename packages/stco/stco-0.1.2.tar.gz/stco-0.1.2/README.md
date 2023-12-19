![PyPI - Version](https://img.shields.io/pypi/v/stco)
![CI - Test](https://github.com/lukezaruba/stco/actions/workflows/01-lint-format-test.yml/badge.svg)
![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)
![GitHub last commit](https://img.shields.io/github/last-commit/lukezaruba/stco)
![GitHub issues](https://img.shields.io/github/issues/lukezaruba/stco)
![PyPI - License](https://img.shields.io/pypi/l/stco)

# stco

A Python package for assessing the temporal stability of spatial clustering methods via spatial overlay analysis.

## Introduction

Typically, to look at hotspots of point patterns we might aggregate the points to polygons and use a method like LISA or Getis-Ord Gi\* to find cold and hot spots. With clustering methods like A-DBSCAN, or any other clustering method that removes noise, we can produce cluster footprints to show "hotspots." There are existing ways to examine the spatial stability of clusters (e.g., A-DBSCAN), but what about looking at temporal stability of clusters and how they change over time? Methods like ST-DBSCAN incorporate the temporal dimension directly into the clustering algorithm, which slighly differs from what we are trying to accomplish here, since we want to look at change over time rather then clustering over both space and time. This leads to the question of, is there a way to study the temporal stability of clusters and explore emerging hotspots, in a way similar to that of Esri's Space Time Cube, without having to aggregate the data? The answer is yes, through `stco`.

`stco` seeks to provide a very simple way to analyze spatial clusters over time with the help of overlay analysis, one of the fundamental operations of GIScience. Rather than runnning clustering directly on the spatiotemporal data, we run spatial clustering on periods of time (by subsetting the data and taking "snapshots") of the spatiotemporal data to produce clusters for each time step. After this, a simple or weighted overlay can be used to examine how clusters change over time. In addition, through the STCEC method, cluster overlays can be classified according to the characteristics of the temporal pattern of cluster recognition in a given area.

## Installation

To install `stco` from PyPI, use the following command.

```bash
pip install stco
```

`stco` has been tested in Python 3.9, 3.10, and 3.11, and support for 3.12 is expected to work and will be tested in the near future. `stco` depends on the following packages:

- `esda`
- `geopandas`
- `numba`
- `numpy`
- `pandas`
- `shapely`
- `tqdm`

There are also additional dependencies for development. A comprehensive list of the recommended dependencies and the version used in development can be found in the `requirements.txt` file.

## Examples & Documentation

For examples, refer to the `examples` folder within the repository, which contains several notebooks.

For documentation, refer to the `examples` folder as well as the source code in the `stco` folder. In order to view documentation through the Python REPL or a notebook, you can use the following code on any given function, class, or method.

```python
from stco.clustering import SnapshotADBSCAN
from stco.overlay import simple_overlay, stcec, weighted_overlay

help(SnapshotADBSCAN)
help(simple_overlay)
help(weighted_overlay)
help(stcec)
```
