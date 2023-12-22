"""Tests for the example module."""
import os
from pathlib import Path

import numpy as np
import pytest
import rasterio

from geo_rasterizer import (
    rasterize_multilabel,
    rasterize,
    raster_to_geotif,
    dense_rasters_to_rgb,
    rasterize_batch,
)
import geopandas as gpd

TEST_DATA_PATH = Path(__file__).parents[1] / "test_data"

GDF_PATH = TEST_DATA_PATH / "test_df.gpkg"
REF_PATH = TEST_DATA_PATH / "test_geotif.tif"

REFERENCE_IMAGE = rasterio.open(REF_PATH)
GEODATAFRAME = gpd.read_file(GDF_PATH, bbox=REFERENCE_IMAGE.bounds)

BATCH_GDF_PATH = TEST_DATA_PATH / "batch_test.gpkg"
BATCH_REFERENCE_IMAGES_PATH = TEST_DATA_PATH / "batch"
BATCH_CONTROL_PATH = TEST_DATA_PATH / "batch_control"


def test_rasterize_multilabel_illegal_geopackage():
    with pytest.raises(Exception):
        rasterize_multilabel(
            gpkg=123,
            reference_image=REFERENCE_IMAGE,
            class_column="label",
            classes=["r1", "a", "g1", "g6", "k4"],
            include_background_class=True,
            dense=True,
        )


def test_rasterize_multilabel_illegal_reference_image():
    with pytest.raises(Exception):
        rasterize_multilabel(
            gpkg=GEODATAFRAME,
            reference_image=None,
            class_column="label",
            classes=["r1", "a", "g1", "g6", "k4"],
            include_background_class=True,
            dense=True,
        )


def test_rasterize_multilabel_read_input():
    raster = rasterize_multilabel(
        gpkg=GEODATAFRAME,
        reference_image=REFERENCE_IMAGE,
        class_column="label",
        classes=["r1", "a", "g1", "g6", "k4"],
        include_background_class=True,
        dense=True,
    )
    assert raster.shape == (1, 900, 1000)
    assert set(raster.flatten()) == {0, 1, 2, 3, 4, 5}


def test_rasterize_multilabel(caplog):
    raster = rasterize_multilabel(
        gpkg=GDF_PATH,
        reference_image=REF_PATH,
        class_column="label",
        classes=["r1", "a", "g1", "g6", "k4"],
        include_background_class=True,
        dense=True,
    )
    assert raster.shape == (1, 900, 1000)
    assert set(raster.flatten()) == {0, 1, 2, 3, 4, 5}

    raster_onehot = rasterize_multilabel(
        gpkg=GDF_PATH,
        reference_image=REF_PATH,
        class_column="label",
        classes=["r1", "a", "g1", "g6", "k4"],
        include_background_class=True,
        dense=False,
    )
    assert raster_onehot.shape == (6, 900, 1000)
    assert set(raster_onehot.flatten()) == {0, 1}

    raster_no_bg = rasterize_multilabel(
        gpkg=GDF_PATH,
        reference_image=REF_PATH,
        class_column="label",
        classes=["r1", "a", "g1", "g6", "k4"],
        include_background_class=False,
        dense=True,
    )
    assert raster_no_bg.shape == (1, 900, 1000)
    assert set(raster_no_bg.flatten()) == {-9999, 0, 1, 2, 3, 4}
    assert (raster_no_bg == -9999).sum() == 190
    assert (
        caplog.messages[0] == "include_background_class is set to False, but "
        "there were background pixels found. Background "
        "pixels were set to -9999. If this is not "
        "intended, set include_background_class=True"
    )


def test_rasterize_multilabel_missing_class(tmp_path):
    # remove one of the classes
    df = gpd.read_file(GDF_PATH)
    filtered_df_path = tmp_path / "filtered_df.gpkg"
    df[df["label"] != "g1"].to_file(filtered_df_path)
    raster = rasterize_multilabel(
        gpkg=filtered_df_path,
        reference_image=REF_PATH,
        class_column="label",
        classes=["r1", "a", "g1", "g6", "k4"],
        include_background_class=True,
        dense=True,
    )
    assert raster.shape == (1, 900, 1000)
    # check if class 3 is missing (it has been filtered out)
    assert set(raster.flatten()) == {0, 1, 2, 4, 5}


def test_rasterize(tmp_path):
    raster_g1_filter = rasterize(
        gdf=GEODATAFRAME,
        reference_image=REFERENCE_IMAGE,
        filters={"label": ["g1"]},
    )
    assert raster_g1_filter.shape == (900, 1000)

    raster_no_filter = rasterize(
        gdf=GEODATAFRAME,
        reference_image=REFERENCE_IMAGE,
    )
    assert raster_no_filter.shape == (900, 1000)

    assert (raster_g1_filter == raster_no_filter).sum() == 323989
    assert (raster_g1_filter != raster_no_filter).sum() == 576011


def test_rasters_to_geotif(tmp_path):
    output_path = tmp_path / "output.tif"
    raster = np.zeros((1, 900, 1000))
    raster[:, :, 250:500] = 1
    raster[:, :, 500:750] = 2
    raster[:, :, 750:] = 3

    raster_to_geotif(
        raster=raster,
        reference=REF_PATH,
        output=output_path,
    )

    with rasterio.open(output_path) as output_img, rasterio.open(REF_PATH) as ref_img:
        assert list(output_img.bounds) == list(ref_img.bounds)
        assert (output_img.read() == raster).all()


def test_one_hot_rasters_to_rgb():
    with open(TEST_DATA_PATH / "multilabel_raster.npy", "rb") as f:
        raster = np.load(f)

    with pytest.raises(ValueError) as e:
        dense_rasters_to_rgb(
            raster=raster,
            num_classes=4,
            alpha=True,
            cmap="tab10",
        )
    e.value
    assert e.match(
        "num_classes cannot be lower than the max index in the raster\n"
        "num_classes is 4, but the maximum index in raster is 5"
    )

    rgba_raster = dense_rasters_to_rgb(
        raster=raster,
        num_classes=5,
        alpha=True,
        cmap="tab10",
    )

    assert len(rgba_raster.shape) == 3
    assert rgba_raster.shape[0] == 4
    assert rgba_raster.dtype == "uint8"
    assert rgba_raster.max() <= 255
    assert rgba_raster.min() >= 0

    rgb_raster = dense_rasters_to_rgb(
        raster=raster,
        num_classes=5,
        alpha=False,
        cmap="tab10",
    )

    assert len(rgb_raster.shape) == 3
    assert rgb_raster.shape[0] == 3
    assert rgb_raster.dtype == "uint8"
    assert rgb_raster.max() <= 255
    assert rgb_raster.min() >= 0


def test_rastersize_batch(tmp_path):
    input_file_names = os.listdir(BATCH_REFERENCE_IMAGES_PATH)
    control_file_names = os.listdir(BATCH_CONTROL_PATH)
    prefix = "rasterized"

    rasterize_batch(
        gpkg=BATCH_GDF_PATH,
        reference_images_folder=BATCH_REFERENCE_IMAGES_PATH,
        class_column="FI_CODE",
        classes=["r1", "r2", "a", "g1", "g6", "k4", "b1"],
        include_background_class=True,
        dense=True,
        output_folder=tmp_path,
        prefix=prefix,
    )

    assert len(os.listdir(tmp_path)) == len(input_file_names)

    for file_name in input_file_names:
        assert any(
            file_name in control_file_name for control_file_name in control_file_names
        )

        control_file_names = os.listdir(BATCH_CONTROL_PATH)
        with rasterio.open(
            tmp_path / str(prefix + "_" + file_name)
        ) as output_img, rasterio.open(
            BATCH_CONTROL_PATH / str(prefix + "_" + file_name)
        ) as control_img:
            assert list(output_img.bounds) == list(control_img.bounds)
            assert (output_img.read() == control_img.read()).all()


def test_rastersize_batch_no_input_folder(tmp_path):
    prefix = "rasterized"

    with pytest.raises(Exception):
        rasterize_batch(
            gpkg=BATCH_GDF_PATH,
            reference_images_folder="/fake/folder",
            class_column="FI_CODE",
            classes=["r1", "r2", "a", "g1", "g6", "k4", "b1"],
            include_background_class=True,
            dense=True,
            output_folder=tmp_path,
            prefix=prefix,
        )


def test_rastersize_no_output_folder(tmp_path):
    prefix = "rasterized"
    output_folder_path = tmp_path / "output"

    assert not os.path.exists(output_folder_path)

    rasterize_batch(
        gpkg=BATCH_GDF_PATH,
        reference_images_folder=BATCH_REFERENCE_IMAGES_PATH,
        class_column="FI_CODE",
        classes=["r1", "r2", "a", "g1", "g6", "k4", "b1"],
        include_background_class=True,
        dense=True,
        output_folder=tmp_path / "output",
        prefix=prefix,
    )

    assert os.path.isdir(output_folder_path)
