# ShareLoc Utilities

Utility tools in Python for shareLoc.xyz

## Features
 - Batch downloading datasets from the https://shareloc.xyz website
 - Parser for *.smlm files


## Installation
```
pip install -U shareloc-utils
```

If you want to use the shareloc potree viewer:

```
pip install -U shareloc-utils[potree]
```

## Usage for batch downloading

The easiest way to download a single dataset is to go to https://shareloc.xyz and click the download icon (downward arrow) on the dataset card.

You will then get a generated command which you can use for downloading the dataset.

If you want to know how the generated commands works, here we will give a few examples.

Basically, you can pass dataset URLs directly to the command line like this:
```
python -m shareloc_utils.batch_download --datasets=https://sandbox.zenodo.org/record/891810 --output_dir=./output
```

If you want to download multiple datasets, use commas to separate their URLs or Zenodo IDs. For example:
```
python -m shareloc_utils.batch_download --datasets=891810,887832 --sandbox --output_dir=./output
```
Note that if you are using the sandbox server and you use Zenodo IDs, you will need an additional `--sandbox` parameter. 

If you want to convert the downloaded dataset to text file format (e.g. CSV), you can add ` --conversion` after the command. If you want to generate a potree octree for visualization, use `--extension=".potree"` (a potree folder) or `--extension=".potree.zip"` (a zipped potree file). 

To print all other options, type: 
```
python -m shareloc_utils.batch_download --help
```

### Bookmarking multiple datasets for download 

The shareLoc.xyz website supports bookmarks, which allow you to mark multiple datasets and download them all at the same time (similar to a shopping cart).

To use this feature, you move your mouse on top of the dataset card you are interested in, then click the bookmark icon to mark it. Repeat the process and mark all the datasets you want to download. Then click the bookmark icon in the navigation bar and click "Download All".

## Use the SMLM file parser

In Python, you use the `read_smlm_file` function to parse the *.smlm file downloaded from ShareLoc(https://shareloc.xyz).

In the following example, we first parse the tables in the smlm file, then generate a histogram image:
```python
from PIL import Image
from shareloc_utils.smlm_file import read_smlm_file, plot_histogram

# parse the .smlm file
manifest = read_smlm_file("./localization_table.smlm")
# one file can contain multiple localization tables
tables = manifest["files"]

# generate a histogram image for the first table
histogram = plot_histogram(tables[0]["data"], value_range=(0, 255))

# save the histogram image as 16-bit png file
im = Image.fromarray(histogram.astype("uint16"))
im.save("output.png")
```

## Development

- Install and set up development environment.

  ```sh
  pip install -r requirements_dev.txt
  ```

  This will install all requirements.
It will also install this package in development mode, so that code changes are applied immediately without reinstall necessary.

- Here's a list of development tools we use.
  - [black](https://pypi.org/project/black/)
  - [flake8](https://pypi.org/project/flake8/)
  - [mypy](https://pypi.org/project/mypy/)
  - [pydocstyle](https://pypi.org/project/pydocstyle/)
  - [pylint](https://pypi.org/project/pylint/)
  - [pytest](https://pypi.org/project/pytest/)
  - [tox](https://pypi.org/project/tox/)
- It's recommended to use the corresponding code formatter and linters also in your code editor to get instant feedback. A popular editor that can do this is [`vscode`](https://code.visualstudio.com/).
- Run all tests, check formatting and linting.

  ```sh
  tox
  ```

- Run a single tox environment.

  ```sh
  tox -e lint
  ```

- Reinstall all tox environments.

  ```sh
  tox -r
  ```

- Run pytest and all tests.

  ```sh
  pytest
  ```

- Run pytest and calculate coverage for the package.

  ```sh
  pytest --cov-report term-missing --cov=shareloc_utils
  ```

- Continuous integration is by default supported via [GitHub actions](https://help.github.com/en/actions). GitHub actions is free for public repositories and comes with 2000 free Ubuntu build minutes per month for private repositories.
