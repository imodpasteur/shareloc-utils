"""Provide a sample test passing with pytest."""
import os
import tempfile
import shutil
import numpy as np

from shareloc_utils.smlm_file import read_smlm_file, plot_histogram
from shareloc_utils.batch_download import download

def test_smlm_file():
    """Test that pytest works."""
    effel_tower_path = os.path.join(os.path.dirname(__file__), 'eiffel_tower.smlm')
    manifest = read_smlm_file(effel_tower_path)
    tables = manifest["files"]
    histogram = plot_histogram(tables[0]["data"], value_range=(0, 255))
    assert histogram.shape == (1040, 470)
    assert np.isclose(histogram.mean(), 0.06435147299509002)
    assert np.isclose(histogram.min(), 0.0)
    assert np.isclose(histogram.max(), 65.0)

def test_download():
    dirpath = tempfile.mkdtemp()
    download(
        ["https://sandbox.zenodo.org/record/884215"],
        dirpath,
        file_patterns=["*.smlm"],
        conversion=True,
        delimiter=",",
        extension=".txt",
    )
    assert os.path.exists("./output/eiffel_tower-df/_covers/screenshot-2_thumbnail.png")
    assert os.path.exists("./output/eiffel_tower-df/eiffel_tower-df/data.txt")
    assert os.path.exists("./output/eiffel_tower-df/README.md")
    shutil.rmtree(dirpath)