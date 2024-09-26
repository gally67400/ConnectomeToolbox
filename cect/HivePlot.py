import matplotlib.pyplot as plt
import networkx as nx
from hiveplotlib import hive_plot_n_axes
from hiveplotlib.converters import networkx_to_nodes_edges
from hiveplotlib.node import split_nodes_on_variable
from hiveplotlib.viz import hive_plot_viz
from hiveplotlib.viz.plotly import hive_plot_viz as plotly_hive_plot_viz

import pprint
import sys

from cect.WormAtlasInfo import WA_COLORS

INTERNEURON_COLOR = WA_COLORS["Hermaphrodite"]["Nervous Tissue"]["interneuron"]
SENSORY_COLOR = WA_COLORS["Hermaphrodite"]["Nervous Tissue"]["sensory neuron"]
MOTORNEURON_COLOR = WA_COLORS["Hermaphrodite"]["Nervous Tissue"]["motor neuron"]

INTERNEURON = "Interneuron"
MOTORNEURON = "Motorneuron"
SENSORY = "Sensory"

if __name__ == "__main__":
    sz = 3

    from cect.TestDataReader import get_instance

    synclass = "Acetylcholine"
    """
    from cect.VarshneyDataReader import get_instance
    synclass = 'Generic_CS' """

    test_conn = get_instance()

    G = nx.stochastic_block_model(
        sizes=[sz, sz, sz],
        p=[[0.2, 0.2, 0.2], [0.2, 0.2, 0.2], [0.2, 0.2, 0.2]],
        directed=True,
        seed=0,
    )
    G = test_conn.to_networkx_graph(synclass)

    nodes, edges = networkx_to_nodes_edges(G)
    # for node in nodes:

    print(nodes)
    print(edges)

    print(pprint.pprint(nx.node_link_data(G)))

    blocks_dict = split_nodes_on_variable(nodes, variable_name="SIM_class")
    print(blocks_dict)

    splits = list(blocks_dict.values())
    print(splits)

    # pull out degree information from nodes
    degrees = dict(G.degree)

    # add degree information to Node instances
    for node in nodes:
        deg = degrees[node.unique_id]
        block = node.data["SIM_class"]
        node.add_data(data={"degree": deg})

        print(f" - Node {node.unique_id}, block {block} has degree {deg}; {node.data}")

    hp = hive_plot_n_axes(
        node_list=nodes,
        edges=edges,
        axes_assignments=splits,
        sorting_variables=["degree"] * 3,
        repeat_axes=[True, True, True],
        repeat_edge_kwargs={"color": "grey"},
    )

    for ax in hp.axes:
        if "1" in ax:
            hp.axes[ax].long_name = INTERNEURON
        if "2" in ax:
            hp.axes[ax].long_name = MOTORNEURON
        if "3" in ax:
            hp.axes[ax].long_name = SENSORY

    for ax_name in hp.axes:
        ax = hp.axes[ax_name]
        print(f" - Axis {ax.long_name}, {ax.start}->{ax.end}...")

    hp.add_edge_kwargs(
        axis_id_1="Group 1_repeat",
        axis_id_2="Group 2",
        a2_to_a1=False,
        color=INTERNEURON_COLOR,
    )

    hp.add_edge_kwargs(
        axis_id_1="Group 2",
        axis_id_2="Group 1_repeat",
        a2_to_a1=False,
        color=MOTORNEURON_COLOR,
    )
    hp.add_edge_kwargs(
        axis_id_1="Group 1",
        axis_id_2="Group 3_repeat",
        a2_to_a1=False,
        color=INTERNEURON_COLOR,
    )
    hp.add_edge_kwargs(
        axis_id_1="Group 3_repeat",
        axis_id_2="Group 1",
        a2_to_a1=False,
        color=SENSORY_COLOR,
    )
    hp.add_edge_kwargs(
        axis_id_1="Group 3",
        axis_id_2="Group 2_repeat",
        a2_to_a1=False,
        color=SENSORY_COLOR,
    )
    hp.add_edge_kwargs(
        axis_id_1="Group 2_repeat",
        axis_id_2="Group 3",
        a2_to_a1=False,
        color=MOTORNEURON_COLOR,
    )

    plotly = False
    plotly = True

    if plotly:
        fig = plotly_hive_plot_viz(
            hp,
        )
        # ax.set_title("Stochastic Block Model, Base Hive Plot Visualization", y=1.05, size=20)
        # fig.update_traces(mode="markers+lines", hovertemplate=None)
        fig.update_layout(hovermode="closest")

        fig.update(data=[{"hoverinfo": "skip"}])

        # print(dir(fig))
        count = 0
        for d in fig.data:
            if d["mode"] == "markers":
                nrn_num = len(d["x"])
                d["hovertemplate"] = "%{text}<extra></extra>"
                d.pop("hoverinfo", None)

                if count == 0 or count == 1:
                    d["marker"]["color"] = [INTERNEURON_COLOR] * nrn_num
                    type_ = "Interneuron"
                if count == 2 or count == 3:
                    d["marker"]["color"] = [MOTORNEURON_COLOR] * nrn_num
                    type_ = "Motorneuron"
                if count == 4 or count == 5:
                    d["marker"]["color"] = [SENSORY_COLOR] * nrn_num
                    type_ = "Sensory"

                d["text"] = ["%s (%s)" % (n, degrees[n]) for n in blocks_dict[type_]]

                print(d)
                count += 1

        import json

        def _format_json(json_str):
            return json.dumps(json.loads(json_str), sort_keys=True, indent=2)

        with open("hive.json", "w") as asset_file:
            asset_file.write(_format_json(fig.to_json()))

        import plotly.io as pio

        pio.renderers.default = "browser"
        if "-nogui" not in sys.argv:
            fig.show()

        print("Done")
    else:
        fig, ax = hive_plot_viz(hp)
        ax.set_title(
            "Stochastic Block Model, Base Hive Plot Visualization", y=1.05, size=20
        )
        plt.show()
