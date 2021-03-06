"""Provide a sample test passing with pytest."""
import os
import tempfile
import shutil
import numpy as np
import pytest

from shareloc_utils.smlm_file import read_smlm_file, plot_histogram
from shareloc_utils.batch_download import download


def test_smlm_file():
    """Test that pytest works."""
    effel_tower_path = os.path.join(os.path.dirname(__file__), "eiffel_tower.smlm")
    manifest = read_smlm_file(effel_tower_path)
    tables = manifest["files"]
    histogram = plot_histogram(tables[0]["data"], value_range=(0, 255))
    assert histogram.shape == (1040, 470)
    assert np.isclose(histogram.mean(), 0.06435147299509002)
    assert np.isclose(histogram.min(), 0.0)
    assert np.isclose(histogram.max(), 65.0)


@pytest.mark.parametrize(
    "datasets,conversion",
    [
        (["884215"], True),
        (["https://sandbox.zenodo.org/record/884215"], True),
        (["884215"], False),
    ],
)
def test_download(datasets, conversion):
    print(datasets, conversion)
    dirpath = tempfile.mkdtemp()
    download(
        datasets,
        dirpath,
        file_patterns=["*.smlm"],
        conversion=conversion,
        delimiter=",",
        extension=".txt",
        sandbox=True,
    )
    assert os.path.exists(
        f"{dirpath}/eiffel_tower-df/_covers/screenshot-2_thumbnail.png"
    )
    if conversion:
        assert os.path.exists(f"{dirpath}/eiffel_tower-df/eiffel_tower-df/data.txt")
    assert os.path.exists(f"{dirpath}/eiffel_tower-df/README.md")
    shutil.rmtree(dirpath)
