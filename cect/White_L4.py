# Temporary class to allow this to be used in comparison notebook.
# Should be tidied up.

from cect.WhiteDataReader import WhiteDataReader
from cect.ConnectomeReader import analyse_connections

import os


def get_instance():
    spreadsheet_location = os.path.dirname(os.path.abspath(__file__)) + "/data/"
    filename = "%saconnectome_white_1986_L4.csv" % spreadsheet_location

    return WhiteDataReader(filename)


my_instance = get_instance()

read_data = my_instance.read_data
read_muscle_data = my_instance.read_muscle_data

READER_DESCRIPTION = (
    """Data extracted from **%s** for neuronal connectivity"""
    % my_instance.filename.split("/")[-1]
)


def main1():
    cells, neuron_conns = read_data()
    neurons2muscles, muscles, muscle_conns = read_muscle_data()
    analyse_connections(cells, neuron_conns, neurons2muscles, muscles, muscle_conns)
    from cect.ConnectomeView import SMALL_VIEW
    from cect.ConnectomeReader import DEFAULT_COLORMAP

    fig = my_instance.to_plotly_matrix_fig(
                "Acetylcholine", SMALL_VIEW, color_continuous_scale=DEFAULT_COLORMAP
            )

    fig.show()

if __name__ == "__main__":
    main1()
