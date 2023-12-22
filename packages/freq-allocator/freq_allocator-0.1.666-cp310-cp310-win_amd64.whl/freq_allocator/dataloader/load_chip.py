from pathlib import Path
import json
import networkx as nx
import numpy as np
from scipy.interpolate import interp1d, interp2d, interpn
from ..model.formula import amp2freq_formula


def load_chip_data_from_file(
    H,
    W,
    qubit_data_filename=r"./chipdata/qubit_data.json",
    qubit_freq_filename=r"./chipdata/qubit_freq_real.json",
    xy_crosstalk_filename=r"./chipdata/xy_crosstalk_sim.json",
    varType='double',
):
    with open(
        qubit_data_filename,
        "r",
        encoding="utf-8",
    ) as file:
        content = file.read()
        chip_data_dic = json.loads(content)
        file.close()

    with open(
        xy_crosstalk_filename,
        "r",
        encoding="utf-8",
    ) as file:
        content = file.read()
        xy_crosstalk_sim_dic = json.loads(content)
        file.close()

    with open(
        qubit_freq_filename,
        "r",
        encoding="utf-8",
    ) as file:
        content = file.read()
        freq_dic = json.loads(content)
        file.close()

    chip = nx.grid_2d_graph(H, W)

    unused_nodes = []
    anharm_list = []
    for qubit in chip.nodes():
        qubit_name = f'q{qubit[0] * W + qubit[1] + 1}'
        chip.nodes[qubit]['name'] = qubit_name
        if not (qubit_name in chip_data_dic and qubit_name in freq_dic):
            unused_nodes.append(qubit)
            continue
        chip.nodes[qubit]['frequency'] = freq_dic[qubit_name]

        if varType == 'double':
            allowFreq = chip_data_dic[qubit_name]['allow_freq']
            chip.nodes[qubit]['allow freq'] = []
            startAf = 0
            for af in range(len(allowFreq)):
                if (
                    af == len(allowFreq) - 1
                    or np.abs(allowFreq[af] - allowFreq[af + 1]) > 1
                ):
                    chip.nodes[qubit]['allow freq'].append(
                        (allowFreq[af], allowFreq[startAf])
                    )
                    startAf = af + 1
            chip.nodes[qubit]['allow freq'] = chip.nodes[qubit]['allow freq'][::-1]
            chip.nodes[qubit]['isolated_error'] = interp1d(
                allowFreq, chip_data_dic[qubit_name]['isolated_error'], kind='linear'
            )

        else:
            chip.nodes[qubit]['allow freq'] = chip_data_dic[qubit_name]['allow_freq']
            chip.nodes[qubit]['isolated_error'] = chip_data_dic[qubit_name][
                'isolated_error'
            ]

        ac_spectrum = chip_data_dic[qubit_name]['ac_spectrum']
        del ac_spectrum[3]
        if len(chip.nodes[qubit]['allow freq']) > 2:
            if len(ac_spectrum) == 4:
                chip.nodes[qubit]['ac_spectrum'] = ac_spectrum
                chip.nodes[qubit]['freq_max'] = ac_spectrum[0]
                chip.nodes[qubit]['freq_min'] = amp2freq_formula(np.pi/2, *ac_spectrum, tans2phi=True)
            else:
                chip.nodes[qubit]['freq_max'] = ac_spectrum[-1]

                del ac_spectrum[6:]
                chip.nodes[qubit]['freq_min'] = amp2freq_formula(np.pi / 2, *ac_spectrum, tans2phi=True)
                chip.nodes[qubit]['ac_spectrum'] = ac_spectrum
        else:
            chip.nodes[qubit]['freq_max'] = max(chip.nodes[qubit]['allow freq'])
            chip.nodes[qubit]['freq_min'] = min(chip.nodes[qubit]['allow freq'])
            if len(ac_spectrum) == 4:
                chip.nodes[qubit]['ac_spectrum'] = ac_spectrum
            else:
                del ac_spectrum[6:]
                chip.nodes[qubit]['ac_spectrum'] = ac_spectrum
        print(qubit_name, chip.nodes[qubit]['freq_max'], chip.nodes[qubit]['freq_min'],chip_data_dic[qubit_name]['anharm'],
              ac_spectrum)

        chip.nodes[qubit]['T1 spectra'] = interp1d(
            chip_data_dic[qubit_name]['t1_spectrum']['freq'],
            chip_data_dic[qubit_name]['t1_spectrum']['t1'],
        )
        chip.nodes[qubit]['anharm'] = round(chip_data_dic[qubit_name]['anharm'])
        chip.nodes[qubit]['sing tq'] = 20
        chip.nodes[qubit]['xy_crosstalk_coef'] = chip_data_dic[qubit_name][
            'xy_crosstalk_coef'
        ]
        anharm_list.append(round(chip_data_dic[qubit_name]['anharm']))
    chip.remove_nodes_from(unused_nodes)
    anharm_list = sorted(list(set(anharm_list)), reverse=True)

    error_arr = [
        xy_crosstalk_sim_dic['error_arr'][
            xy_crosstalk_sim_dic['alpha_list'].index(anharm)
        ]
        for anharm in anharm_list
    ]
    xy_crosstalk_sim_dic['alpha_list'] = anharm_list
    xy_crosstalk_sim_dic['error_arr'] = error_arr

    for qubit in chip.nodes:
        error_arr1 = xy_crosstalk_sim_dic['error_arr'][
            anharm_list.index(chip.nodes[qubit]['anharm'])
        ]
        f = interp2d(
            xy_crosstalk_sim_dic['detune_list'],
            xy_crosstalk_sim_dic['mu_list'],
            error_arr1,
            kind='cubic',
        )
        chip.nodes[qubit]['xy_crosstalk_f'] = f

    return chip


def gen_pos(chip):
    # wStep = 1
    # hStep = 1
    pos = dict()
    for qubit in chip:
        # pos[qubit] = [qubit[0] * wStep, qubit[1] * hStep]
        pos[qubit] = [qubit[1], -qubit[0]]
    return pos


def twoQ_gen_pos(chip, xtalkG):
    bitPos = gen_pos(chip)
    for bit in bitPos:
        bitPos[bit][0] *= 2
        bitPos[bit][1] *= 2
    pos = dict()
    for coupler in xtalkG:
        pos[coupler] = [
            (bitPos[coupler[0]][0] + bitPos[coupler[1]][0]) / 2,
            (bitPos[coupler[0]][1] + bitPos[coupler[1]][1]) / 2,
        ]
    return pos


def max_Algsubgraph(chip):
    dualChip = nx.Graph()
    dualChip.add_nodes_from(list(chip.edges))
    for coupler1 in dualChip.nodes:
        for coupler2 in dualChip.nodes:
            if coupler1 == coupler2 or set(coupler1).isdisjoint(set(coupler2)):
                continue
            else:
                dualChip.add_edge(coupler1, coupler2)
    maxParallelCZs = [[], [], [], []]
    for edge in chip.edges:
        if sum(edge[0]) < sum(edge[1]):
            start = edge[0]
            end = edge[1]
        else:
            start = edge[1]
            end = edge[0]
        if start[0] == end[0]:
            if sum(start) % 2:
                maxParallelCZs[0].append(edge)
            else:
                maxParallelCZs[2].append(edge)
        else:
            if sum(start) % 2:
                maxParallelCZs[1].append(edge)
            else:
                maxParallelCZs[3].append(edge)
    return maxParallelCZs


def xtalk_G(chip):
    xtalkG = nx.Graph()
    for coupler1 in chip.edges:
        if not (coupler1 in xtalkG.nodes):
            xtalkG.add_node(coupler1)
        if not (xtalkG.nodes[coupler1].get('two tq')):
            xtalkG.nodes[coupler1]['two tq'] = 40
        for coupler2 in chip.edges:
            if coupler1 == coupler2 or (coupler1, coupler2) in xtalkG.edges:
                continue
            distance = []
            for i in coupler1:
                for j in coupler2:
                    if nx.has_path(chip, i, j):
                        distance.append(nx.shortest_path_length(chip, i, j))
                    else:
                        distance.append(100000)
            if 1 in distance and not (0 in distance):
                xtalkG.add_edge(coupler1, coupler2)
    return xtalkG
