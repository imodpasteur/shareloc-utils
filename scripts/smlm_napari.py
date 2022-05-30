import napari
import pathlib
import numpy as np
from vispy.color import Colormap
from shareloc_utils.smlm_file import read_smlm_file, plot_histogram
from shareloc_utils.batch_download import download

def plot_smlm_in_napari(output_dir,
                        datasets = 5514120, #Znodo DOI number
                        extension = ".smlm"):
    datasets=str(datasets)
    list_path=list(pathlib.Path(output_dir+datasets).glob('*/*/*.smlm'))
    # down load
    if not list_path:
        download(
        datasets=[datasets],
        output_dir=output_dir+datasets,
        extension=extension,
        conversion=False,
        sandbox=False)

    redhot_cmap=Colormap([[0, 0, 0], [1, 0, 0],[1, 1, 0], [1, 1, 1]])
    cmap = [redhot_cmap, 'cyan', 'green', 'magenta']
    
    for sample_index in range(len(list_path)):
        viewer = napari.Viewer()
        print("plotting: ",list_path[sample_index])
        imag_path = list_path[sample_index]
        manifest = read_smlm_file(imag_path)
        tables = manifest["files"]
        histogram = []
        name = []
        colormap = []
        for ch in range(len(tables)):
        #histogram.append(plot_histogram(tables[ch]["data"], value_range=(0, 255)))
        #print(np.shape(histogram))
        #histogram = np.concatenate((histogram, plot_histogram(tables[ch]["data"], value_range=(0, 255))[:,:,np.newaxis]), axis=-1)
            histogram = plot_histogram(tables[ch]["data"], value_range=(0, 255))
            name.append(tables[ch]["name"])
            colormap.append(cmap[ch])
            viewer.add_image(
                histogram,
                blending="additive",
                colormap=cmap[ch],
                contrast_limits=[0, 10],
                name=tables[ch]["name"])

def main():
    import argparse

    parser = argparse.ArgumentParser(description="Visualize locally SMLM data via napari")
    parser.add_argument(
        "--datasets",
        default=[],
        help="A Zenodo ID XXXX",
    )
    parser.add_argument("--output_dir", default=None, help="output directory path")
    parser.add_argument(
        "--sandbox",
        action="store_true",
        help="Use the sandbox site, used only when Zenodo IDs are provided for the datasets",
    )
    parser.add_argument(
        "--conversion",
        action="store_true",
        help="enable conversion to text file (e.g. csv)",
    )
    parser.add_argument(
        "--extension", default=".smlm", help="file extension for text file conversion"
    )

    args = parser.parse_args()

    plot_smlm_in_napari(output_dir = args.output_dir,
                        datasets = args.datasets, #Znodo DOI number
                        extension = args.extension)
    napari.run()


if __name__ == "__main__":
    main()