from sko.PSO import PSO
import os, json
import pickle
import geatpy as ea
import numpy as np
from copy import deepcopy
import random
from matplotlib import pyplot as plt
import matplotlib
from freq_allocator.dataloader.load_chip import gen_pos, max_Algsubgraph, xtalk_G
import networkx as nx
from freq_allocator.model.two_qubit_model import (
    twoQ_err_model,
    twoq_T1_err,
    twoq_T2_err,
    twoq_xtalk_err,
    twoq_pulse_distort_err,
    inner_leakage,
)
import time


def two_alloc(chip, a):
    font = {'family': 'Times New Roman', 'weight': 'bold', 'size': 25}

    current_date = time.strftime("%Y-%m-%d")
    current_time = time.strftime("%H:%M:%S", time.localtime()).replace(':', '.')
    path = f'.\\results\\{current_date}\\{current_time}'

    # 做一个判断，按idle freq确定qh，ql后，如果完全不可能做门，就删掉这条边
    edges_to_remove = []
    for qcq in chip.edges():
        if chip.nodes[qcq[0]]['frequency'] > chip.nodes[qcq[1]]['frequency']:
            qh, ql = qcq[0], qcq[1]
        else:
            qh, ql = qcq[1], qcq[0]
        if chip.nodes[qh]['freq_min'] + chip.nodes[qh]['anharm'] > chip.nodes[ql]['freq_max']:
            edges_to_remove.append(qcq)
    chip.remove_edges_from(edges_to_remove)

    originXtalkG = xtalk_G(chip)
    maxParallelCZs = max_Algsubgraph(chip)
    xtalkG = xtalk_G(chip)

    for level in range(len(maxParallelCZs)):
        couplerActivate = [[coupler, 'gray'] for coupler in chip.edges]
        for i in couplerActivate:
            if i[0] in maxParallelCZs[level]:
                i[1] = 'green'
        pos = gen_pos(chip)
        plt.figure(figsize=(8, 8))
        nx.draw_networkx_edges(
            chip,
            pos,
            edgelist=chip.edges,
            edge_color=list(dict(couplerActivate).values()),
            edge_cmap=plt.cm.plasma,
            width=8,
        )
        path_name = os.path.join(path, f'twoq chip {level}.pdf')
        os.makedirs(os.path.dirname(path_name), exist_ok=True)
        nx.draw_networkx_nodes(chip, pos, nodelist=chip.nodes, cmap=plt.cm.plasma)
        plt.axis('off')
        plt.savefig(path_name, dpi=300)
        plt.close()

    for level in range(len(maxParallelCZs)):
        print('level', level)
        if len(maxParallelCZs[level]) == 0:
            continue
        epoch = 0
        xTalkSubG = deepcopy(xtalkG)
        xTalkSubG.remove_nodes_from(
            set(xtalkG.nodes).difference(set(maxParallelCZs[level]))
        )

        centerConflictQCQ = list(xTalkSubG.nodes)[0]
        newreOptimizeQCQs = []
        avgErrEpoch = []
        jumpToEmpty = False
        hisReOptimizeQCQs = []
        hisXtalkG = []
        repeat_optimize_history = {'center_node': 1,
                                   'chip_history': [],
                                   'error_history': []
                                   }

        fixQcq = []


        # 先把固定节点附近的边分配好，后面不去动它了
        for qcq in xTalkSubG.nodes:
            if len(chip.nodes[qcq[0]]['allow freq']) == 2 or \
                    len(chip.nodes[qcq[1]]['allow freq']) == 2:
                if len(chip.nodes[qcq[0]]['allow freq']) == 2:
                    qfix = qcq[0]
                    qnfix = qcq[1]
                else:
                    qfix = qcq[1]
                    qnfix = qcq[0]

                fixQcq.append(qcq)

                if chip.nodes[qfix]['frequency'] > chip.nodes[qnfix]['frequency'] and \
                        chip.nodes[qfix]['frequency'] + chip.nodes[qfix]['anharm'] > chip.nodes[qnfix]['freq_min']:
                    xTalkSubG.nodes[qcq]['frequency'] = chip.nodes[qfix]['frequency'] + chip.nodes[qfix]['anharm']
                else:
                    xTalkSubG.nodes[qcq]['frequency'] = chip.nodes[qfix]['frequency']

        while len(
            [
                xTalkSubG.nodes[qcq]['all err']
                for qcq in xTalkSubG.nodes
                if xTalkSubG.nodes[qcq].get('all err', False)
            ]
        ) < len(xTalkSubG.nodes) or (
            len(
                [
                    xTalkSubG.nodes[qcq]['all err']
                    for qcq in xTalkSubG.nodes
                    if xTalkSubG.nodes[qcq].get('all err', False)
                ]
            )
            == len(xTalkSubG.nodes)
            and not (jumpToEmpty)
        ):
            reOptimizeQCQs = [centerConflictQCQ]
            for qcq in xTalkSubG.nodes():
                if (
                    centerConflictQCQ in newreOptimizeQCQs
                    and not (qcq in reOptimizeQCQs)
                    and qcq in newreOptimizeQCQs
                ):
                    reOptimizeQCQs.append(qcq)
                elif (
                    not (xTalkSubG.nodes[centerConflictQCQ].get('frequency', False))
                    and not (qcq in reOptimizeQCQs)
                    and not (xTalkSubG.nodes[qcq].get('frequency', False))
                    and nx.has_path(xTalkSubG, qcq, centerConflictQCQ)
                    and nx.shortest_path_length(xTalkSubG, qcq, centerConflictQCQ) == 1
                ):
                    reOptimizeQCQs.append(qcq)
            print('optimize gates: ', reOptimizeQCQs)

            
            bounds = []
            for qcq in reOptimizeQCQs:

                if chip.nodes[qcq[0]]['frequency'] > chip.nodes[qcq[1]]['frequency']:
                    qh, ql = qcq[0], qcq[1]
                else:
                    qh, ql = qcq[1], qcq[0]

                if chip.nodes[qh]['freq_max'] + chip.nodes[qh]['anharm'] < chip.nodes[ql]['freq_min']:
                    qh, ql = ql, qh

                lb = (max(chip.nodes[ql]['freq_min'], chip.nodes[qh]['freq_min'] + chip.nodes[qh]['anharm']))
                ub = (min(chip.nodes[ql]['freq_max'], chip.nodes[qh]['freq_max'] + chip.nodes[qh]['anharm']))
                # if lb >= ub:
                #     lb, ub = ub, lb

                bound = (lb, ub)
                assert bound[0] < bound[1]
                bounds.append(bound)

            for qcq in fixQcq:
                if qcq in reOptimizeQCQs:
                    reOptimizeQCQs.remove(qcq)
            reOptimizeQCQs = tuple(reOptimizeQCQs)

            @ea.Problem.single
            def err_model_fun(frequencys):
                return twoQ_err_model(frequencys, chip, xTalkSubG, reOptimizeQCQs, a)

            problem = ea.Problem(
                name='two q err model',
                M=1,  # 初始化M（目标维数）
                maxormins=[1],  # 初始化maxormins（目标最小最大化标记列表，1：最小化该目标；-1：最大化该目标）
                Dim=len(reOptimizeQCQs),  # 决策变量维数
                varTypes=[1] * len(reOptimizeQCQs),  # 决策变量的类型列表，0：实数；1：整数
                lb=[b[0] for b in bounds],  # 决策变量下界
                ub=[b[1] for b in bounds],  # 决策变量上界
                evalVars=err_model_fun,
            )

            algorithm = ea.soea_DE_best_1_bin_templet(
                problem,
                ea.Population(Encoding='RI', NIND=300),
                MAXGEN=50,
                logTras=1,
                # trappedValue=1e-10,
                # maxTrappedCount=20
            )
            algorithm.mutOper.F = 0.95
            algorithm.recOper.XOVR = 0.7

            # algorithm.run()
            path_name = os.path.join(path, f'pattern = {level+1}\\epoch={epoch + 1} soea_DE result')
            os.makedirs(os.path.dirname(path_name), exist_ok=True)

            freq_bset = None
            res = ea.optimize(
                algorithm,
                prophet=freq_bset,
                # prophet=np.array(self.experiment_options.FIR0),
                verbose=True,
                drawing=0,
                outputMsg=True,
                drawLog=False,
                saveFlag=True,
                dirName=path_name,
            )
            freq_bset = res['Vars'][0]

            for qcq in reOptimizeQCQs:
                xTalkSubG.nodes[qcq]['frequency'] = freq_bset[reOptimizeQCQs.index(qcq)]

            newreOptimizeQCQs, conflictGatePairs, conflictSpectator, error_evarage, xTalkSubG = twoQ_checkcoli(
                chip, xTalkSubG, a
            )
            # hisXtalkG.append(xTalkSubG)
            # hisReOptimizeQCQs.append(set(newreOptimizeQCQs))
            # ocqc = [len(h) for h in hisReOptimizeQCQs]

            repeat_optimize_history['error_history'].append(error_evarage)
            repeat_optimize_history['chip_history'].append(deepcopy(xTalkSubG))

            if len(repeat_optimize_history['error_history']) > 3 or len(newreOptimizeQCQs) == 0:
                idx = repeat_optimize_history['error_history'].index(min(repeat_optimize_history['error_history']))
                xTalkSubG = repeat_optimize_history['chip_history'][idx]

                repeat_optimize_history['error_history'] = []
                repeat_optimize_history['chip_history'] = []

                jumpToEmpty = True
            else:
                print('no jump')
                jumpToEmpty = False

            avgErrEpoch.append(error_evarage)

            print('avg err estimate', avgErrEpoch)
            if len(
                [
                    xTalkSubG.nodes[qcq]['all err']
                    for qcq in xTalkSubG.nodes
                    if xTalkSubG.nodes[qcq].get('all err', False)
                ]
            ) == len(xTalkSubG.nodes):
                for qcq in chip.edges:
                    if qcq in xTalkSubG.nodes:
                        xtalkG.nodes[qcq]['frequency'] = xTalkSubG.nodes[qcq][
                            'frequency'
                        ]
                        xtalkG.nodes[qcq]['spectator err'] = xTalkSubG.nodes[qcq][
                            'spectator err'
                        ]
                        xtalkG.nodes[qcq]['parallel err'] = xTalkSubG.nodes[qcq][
                            'parallel err'
                        ]
                        xtalkG.nodes[qcq]['innerLeakage err'] = xTalkSubG.nodes[qcq][
                            'innerLeakage err'
                        ]
                        xtalkG.nodes[qcq]['T err'] = xTalkSubG.nodes[qcq]['T err']
                        xtalkG.nodes[qcq]['distort err'] = xTalkSubG.nodes[qcq][
                            'distort err'
                        ]
                        xtalkG.nodes[qcq]['all err'] = xTalkSubG.nodes[qcq]['all err']
                        conflictGatePairFinal = conflictGatePairs
                        conflictSpectatorFinal = conflictSpectator

            # 保存每次迭代之后的xTalkSubG，主要是其中的error
            path_name = os.path.join(path, f'pattern = {level+1}\\epoch = {epoch + 1},chip_process.pickle')
            os.makedirs(os.path.dirname(path_name), exist_ok=True)
            with open(path_name, "ab") as f:
                pickle.dump(xTalkSubG, f)

            pos = gen_pos(chip)
            labelDict = {}
            for qubit in chip:
                labelDict[qubit] = chip.nodes[qubit]['name']

            errList = []
            for i in chip.edges:
                if i in xTalkSubG.nodes:
                    errList.append(xTalkSubG.nodes[i].get('all err', 1e-3))
                else:
                    errList.append(1e-3)
            edge_colors = np.log10(errList)

            errLow = min(errList)
            errHigh = max(errList)
            fig, ax = plt.subplots(figsize=(8, 12))
            nx.draw_networkx_labels(
                chip, pos, labelDict, font_size=12, font_color="black"
            )
            nx.draw_networkx_edges(
                chip,
                pos,
                edgelist=chip.edges,
                edge_color=edge_colors,
                edge_cmap=plt.cm.coolwarm,
                width=12,
            )
            nx.draw_networkx_nodes(chip, pos, ax=ax, nodelist=chip.nodes, node_size=2000, node_color='white')

            cb = plt.colorbar(
                matplotlib.cm.ScalarMappable(
                    norm=matplotlib.colors.LogNorm(vmin=errLow, vmax=errHigh),
                    cmap='coolwarm',
                ),
                ax=ax
            )
            ax.set_title(f'pattern = {level+1} epoch = {epoch + 1}', fontdict=font)
            cb.set_label(r'error', fontdict=font)
            cb.ax.tick_params(labelsize=15)
            plt.axis('off')
            plt.tight_layout()

            path_name = os.path.join(path, f'pattern = {level+1}\\epoch = {epoch + 1} chip_error_log.png')
            os.makedirs(os.path.dirname(path_name), exist_ok=True)
            plt.savefig(path_name, dpi=300)
            plt.close()

            reOptimizeQCQsDict = dict()
            for qcq in newreOptimizeQCQs:
                if not(nx.has_path(originXtalkG, qcq, centerConflictQCQ)):
                    reOptimizeQCQsDict[qcq] = 10000
                else:
                    reOptimizeQCQsDict[qcq] = nx.shortest_path_length(originXtalkG, qcq, centerConflictQCQ)

            emptyQCQDict = dict()
            for qcq in xTalkSubG:
                if not(xTalkSubG.nodes[qcq].get('frequency', False)):
                    if not(nx.has_path(originXtalkG, qcq, centerConflictQCQ)):
                        emptyQCQDict[qcq] = 10000
                    else:
                        emptyQCQDict[qcq] = nx.shortest_path_length(originXtalkG, qcq, centerConflictQCQ)

            if len(reOptimizeQCQsDict) > 0 and not (jumpToEmpty):
                print('reoptimize qcq distance', reOptimizeQCQsDict)
                centerConflictQCQ = random.choices(
                    list(reOptimizeQCQsDict.keys()),
                    weights=[
                        1 / max(0.5, distance)
                        for distance in reOptimizeQCQsDict.values()
                    ],
                    k=1,
                )[0]
            elif len(emptyQCQDict) > 0:
                print('empty qcq distance', emptyQCQDict)
                centerConflictQCQ = list(
                    sorted(emptyQCQDict.items(), key=lambda x: x[1])
                )[0][0]
            epoch += 1

        fig, ax = plt.subplots()
        print('ave', avgErrEpoch)
        ax.plot(avgErrEpoch, label='err epoch')
        ax.set_xlabel('epoch')
        ax.legend()

        path_name = os.path.join(path, f'pattern = {level + 1}\\CZ err.png')
        os.makedirs(os.path.dirname(path_name), exist_ok=True)
        plt.savefig(path_name, dpi=300)
        plt.close()

        for qcq in xTalkSubG.nodes:
            chip.edges[qcq]['frequency'] = xTalkSubG.nodes[qcq]['frequency']
            chip.edges[qcq]['error_all'] = xTalkSubG.nodes[qcq]['all err']

        # pos = gen_pos(chip)
        # labelDict = dict([(i, i) for i in chip.nodes])

        # freqList = []
        # for qcq in chip.edges:
        #     if qcq in xTalkSubG.nodes:
        #         freqList.append(round(xtalkG.nodes[qcq]['frequency']))
        #     else:
        #         freqList.append(3000)
        # freqLow = min(freqList)
        # freqHigh = max(freqList)
        #
        # plt.figure(figsize=(8, 8))
        # nx.draw_networkx_labels(chip, pos, labelDict, font_size=14, font_color="black")
        # nx.draw_networkx_edges(
        #     chip,
        #     pos,
        #     edgelist=chip.edges,
        #     edge_color=freqList,
        #     edge_cmap=plt.cm.plasma,
        #     width=8,
        # )
        # nx.draw_networkx_nodes(chip, pos, nodelist=chip.nodes, cmap=plt.cm.plasma)
        # plt.axis('off')
        # plt.colorbar(
        #     matplotlib.cm.ScalarMappable(
        #         norm=matplotlib.colors.Normalize(vmin=freqLow, vmax=freqHigh),
        #         cmap=plt.cm.plasma,
        #     )
        # )
        # plt.savefig('results\\' + str(level) + 'best' + 'cz freq.pdf', dpi=300)
        # plt.close()
        #
        # pos = gen_pos(chip)
        # labelDict = dict([(i, i) for i in chip.nodes])
        #
        # errList = []
        # for qcq in chip.edges:
        #     if qcq in xTalkSubG.nodes:
        #         errList.append(xtalkG.nodes[qcq]['spectator err'])
        #     else:
        #         errList.append(1e-5)
        # errList = np.log10(errList)
        # errLow = min(errList)
        # errHigh = max(errList)
        #
        # plt.figure(figsize=(8, 8))
        # nx.draw_networkx_labels(chip, pos, labelDict, font_size=14, font_color="black")
        # nx.draw_networkx_edges(
        #     chip,
        #     pos,
        #     edgelist=chip.edges,
        #     edge_color=errList,
        #     edge_cmap=plt.cm.plasma,
        #     width=8,
        # )
        # nx.draw_networkx_nodes(chip, pos, nodelist=chip.nodes, cmap=plt.cm.plasma)
        # plt.axis('off')
        # plt.colorbar(
        #     matplotlib.cm.ScalarMappable(
        #         norm=matplotlib.colors.Normalize(vmin=errLow, vmax=errHigh),
        #         cmap=plt.cm.plasma,
        #     )
        # )
        # plt.savefig('results\\' + str(level) + 'best' + 'cz spectator err.pdf', dpi=300)
        # plt.close()
        #
        # pos = gen_pos(chip)
        # labelDict = dict([(i, i) for i in chip.nodes])
        #
        # errList = []
        # for qcq in chip.edges:
        #     if qcq in xTalkSubG.nodes:
        #         errList.append(xtalkG.nodes[qcq]['parallel err'])
        #     else:
        #         errList.append(1e-5)
        # errList = np.log10(errList)
        # errLow = min(errList)
        # errHigh = max(errList)
        #
        # plt.figure(figsize=(8, 8))
        # nx.draw_networkx_labels(chip, pos, labelDict, font_size=14, font_color="black")
        # nx.draw_networkx_edges(
        #     chip,
        #     pos,
        #     edgelist=chip.edges,
        #     edge_color=errList,
        #     edge_cmap=plt.cm.plasma,
        #     width=8,
        # )
        # nx.draw_networkx_nodes(chip, pos, nodelist=chip.nodes, cmap=plt.cm.plasma)
        # plt.axis('off')
        # plt.colorbar(
        #     matplotlib.cm.ScalarMappable(
        #         norm=matplotlib.colors.Normalize(vmin=errLow, vmax=errHigh),
        #         cmap=plt.cm.plasma,
        #     )
        # )
        # plt.savefig('results\\' + str(level) + 'best' + 'cz parallel err.pdf', dpi=300)
        # plt.close()
        #
        # pos = gen_pos(chip)
        # labelDict = dict([(i, i) for i in chip.nodes])
        #
        # errList = []
        # for qcq in chip.edges:
        #     if qcq in xTalkSubG.nodes:
        #         errList.append(xtalkG.nodes[qcq]['innerLeakage err'])
        #     else:
        #         errList.append(1e-5)
        # errList = np.log10(errList)
        # errLow = min(errList)
        # errHigh = max(errList)
        #
        # plt.figure(figsize=(8, 8))
        # nx.draw_networkx_labels(chip, pos, labelDict, font_size=14, font_color="black")
        # nx.draw_networkx_edges(chip, pos, edgelist=chip.edges, edge_color=errList, edge_cmap=plt.cm.plasma, width=8)
        # nx.draw_networkx_nodes(chip, pos, nodelist=chip.nodes, cmap=plt.cm.plasma)
        # plt.axis('off')
        # plt.colorbar(matplotlib.cm.ScalarMappable(norm=matplotlib.colors.Normalize(vmin=errLow, vmax=errHigh), cmap=plt.cm.plasma))
        # plt.savefig('results\\' + str(level) + 'best' + 'cz innerLeakage err.pdf', dpi=300)
        # plt.close()
        #
        # pos = gen_pos(chip)
        # labelDict = dict([(i, i) for i in chip.nodes])
        #
        # errList = []
        # for qcq in chip.edges:
        #     if qcq in xTalkSubG.nodes:
        #         errList.append(xtalkG.nodes[qcq]['T err'])
        #     else:
        #         errList.append(1e-5)
        # errList = np.log10(errList)
        # errLow = min(errList)
        # errHigh = max(errList)
        #
        # plt.figure(figsize=(8, 8))
        # nx.draw_networkx_labels(chip, pos, labelDict, font_size=14, font_color="black")
        # nx.draw_networkx_edges(
        #     chip,
        #     pos,
        #     edgelist=chip.edges,
        #     edge_color=errList,
        #     edge_cmap=plt.cm.plasma,
        #     width=8,
        # )
        # nx.draw_networkx_nodes(chip, pos, nodelist=chip.nodes, cmap=plt.cm.plasma)
        # plt.axis('off')
        # plt.colorbar(
        #     matplotlib.cm.ScalarMappable(
        #         norm=matplotlib.colors.Normalize(vmin=errLow, vmax=errHigh),
        #         cmap=plt.cm.plasma,
        #     )
        # )
        # plt.savefig('results\\' + str(level) + 'best' + 'cz t1 t2 err.pdf', dpi=300)
        # plt.close()
        #
        # pos = gen_pos(chip)
        # labelDict = dict([(i, i) for i in chip.nodes])
        #
        # errList = []
        # for qcq in chip.edges:
        #     if qcq in xTalkSubG.nodes:
        #         errList.append(xtalkG.nodes[qcq]['distort err'])
        #     else:
        #         errList.append(1e-5)
        # errList = np.log10(errList)
        # errLow = min(errList)
        # errHigh = max(errList)
        #
        # plt.figure(figsize=(8, 8))
        # nx.draw_networkx_labels(chip, pos, labelDict, font_size=14, font_color="black")
        # nx.draw_networkx_edges(
        #     chip,
        #     pos,
        #     edgelist=chip.edges,
        #     edge_color=errList,
        #     edge_cmap=plt.cm.plasma,
        #     width=8,
        # )
        # nx.draw_networkx_nodes(chip, pos, nodelist=chip.nodes, cmap=plt.cm.plasma)
        # plt.axis('off')
        # plt.colorbar(
        #     matplotlib.cm.ScalarMappable(
        #         norm=matplotlib.colors.Normalize(vmin=errLow, vmax=errHigh),
        #         cmap=plt.cm.plasma,
        #     )
        # )
        # plt.savefig('results\\' + str(level) + 'best' + 'cz dist err.pdf', dpi=300)
        # plt.close()
        #
        # pos = gen_pos(chip)
        # labelDict = dict([(i, i) for i in chip.nodes])
        #
        # errList = []
        # for qcq in chip.edges:
        #     if qcq in xTalkSubG.nodes:
        #         errList.append(xtalkG.nodes[qcq]['all err'])
        #     else:
        #         errList.append(1e-5)
        # errList = np.log10(errList)
        # errLow = min(errList)
        # errHigh = max(errList)
        #
        # plt.figure(figsize=(8, 8))
        # nx.draw_networkx_labels(chip, pos, labelDict, font_size=14, font_color="black")
        # nx.draw_networkx_edges(
        #     chip,
        #     pos,
        #     edgelist=chip.edges,
        #     edge_color=errList,
        #     edge_cmap=plt.cm.plasma,
        #     width=8,
        # )
        # nx.draw_networkx_nodes(chip, pos, nodelist=chip.nodes, cmap=plt.cm.plasma)
        #
        # plt.axis('off')
        # plt.tight_layout()
        # plt.colorbar(
        #     matplotlib.cm.ScalarMappable(
        #         norm=matplotlib.colors.Normalize(vmin=errLow, vmax=errHigh),
        #         cmap=plt.cm.plasma,
        #     )
        # )
        # plt.savefig('results\\' + str(level) + 'best' + 'cz all err.pdf', dpi=300)
        # plt.close()

    # labelList = list(xtalkG.nodes)
    # errList = [xtalkG.nodes[qcq]['spectator err'] for qcq in labelList]
    # plt.scatter([range(len(labelList))], errList, color='blue', alpha=0.5, s=100)
    # plt.axhline(y=1e-2, color='red', linestyle='--')
    # plt.semilogy()
    # plt.savefig('results\\' + 'cz spectator err scatter.pdf', dpi=300)
    # plt.close()
    #
    # labelList = list(xtalkG.nodes)
    # errList = [xtalkG.nodes[qcq]['parallel err'] for qcq in labelList]
    # plt.scatter([range(len(labelList))], errList, color='blue', alpha=0.5, s=100)
    # plt.axhline(y=1e-2, color='red', linestyle='--')
    # plt.semilogy()
    # plt.savefig('results\\' + 'cz parallel err scatter.pdf', dpi=300)
    # plt.close()
    #
    # labelList = list(xtalkG.nodes)
    # errList = [xtalkG.nodes[qcq]['innerLeakage err'] for qcq in labelList]
    # plt.scatter([range(len(labelList))], errList, color='blue', alpha=0.5, s=100)
    # plt.axhline(y=1e-2, color='red', linestyle='--')
    # plt.semilogy()
    # plt.savefig('results\\' + 'cz innerLeakage err scatter.pdf', dpi=300)
    # plt.close()
    #
    # labelList = list(xtalkG.nodes)
    # errList = [xtalkG.nodes[qcq]['T err'] for qcq in labelList]
    # plt.scatter([range(len(labelList))], errList, color='blue', alpha=0.5, s=100)
    # plt.axhline(y=1e-2, color='red', linestyle='--')
    # plt.semilogy()
    # plt.savefig('results\\' + 'cz decoherence err scatter.pdf', dpi=300)
    # plt.close()
    #
    # labelList = list(xtalkG.nodes)
    # errList = [xtalkG.nodes[qcq]['distort err'] for qcq in labelList]
    # plt.scatter([range(len(labelList))], errList, color='blue', alpha=0.5, s=100)
    # plt.axhline(y=1e-2, color='red', linestyle='--')
    # plt.semilogy()
    # plt.savefig('results\\' + 'cz dist err scatter.pdf', dpi=300)
    # plt.close()
    #
    # labelList = list(xtalkG.nodes)
    # errList = [xtalkG.nodes[qcq]['all err'] for qcq in labelList]
    # plt.scatter([range(len(labelList))], errList, color='blue', alpha=0.5, s=100)
    # plt.axhline(y=1e-2, color='red', linestyle='--')
    # plt.semilogy()
    # plt.savefig('results\\' + 'cz all err scatter.pdf', dpi=300)
    # plt.close()
    #
    # errJson = dict()
    # for qcq in xtalkG.nodes:
    #     qcqName = chip.nodes[qcq[0]]['name'] + chip.nodes[qcq[1]]['name']
    #     errJson[qcqName] = {' frequency ':
    #             round(xtalkG.nodes[qcq]['frequency'], 3),
    #             ' spectator error ' :
    #             round(xtalkG.nodes[qcq]['spectator err'], 7),
    #             ' parallel error ' :
    #             round(xtalkG.nodes[qcq]['parallel err'], 7),
    #             ' T error ' :
    #             round(xtalkG.nodes[qcq]['T err'], 7),
    #             ' distort error ' :
    #             round(xtalkG.nodes[qcq]['distort err'], 7),
    #             ' all error ' :
    #             round(xtalkG.nodes[qcq]['all err'], 7)}
    #
    # with open('results\\cz err.json', 'w') as fp:
    #     json.dump(errJson, fp)
    #
    # with open('results\\conflict spectator dict.txt', 'w') as fp:
    #     for qcq in conflictSpectatorFinal:
    #         fp.write(str(qcq) + ': ')
    #         for neighbor in conflictSpectatorFinal[qcq]:
    #             fp.write(str(neighbor) + ' ')
    #         fp.write('\n')
    #
    # with open('results\\conflict gate pair.txt', 'w') as fp:
    #     for pair in conflictGatePairFinal:
    #         fp.write(str(pair) + '\n')
    path_name = os.path.join(path, f'chip_final.pickle')
    os.makedirs(os.path.dirname(path_name), exist_ok=True)
    with open(path_name, "ab") as f:
        pickle.dump(chip, f)

    return xtalkG


def twoQ_checkcoli(chip, xtalkG, a):
    reOptimizeQCQs = []
    conflictSpectator = dict()
    conflictGatePairs = []
    error_chip = 0
    qcq_num = 0
    for qcq in xtalkG.nodes:
        if xtalkG.nodes[qcq].get('frequency', False):
            if chip.nodes[qcq[0]]['frequency'] > chip.nodes[qcq[1]]['frequency']:
                qh, ql = qcq[0], qcq[1]
            else:
                qh, ql = qcq[1], qcq[0]
            if chip.nodes[qh]['freq_max'] + chip.nodes[qh]['anharm'] < chip.nodes[ql]['freq_min']:
                qh, ql = ql, qh

            fWork = xtalkG.nodes[qcq]['frequency']
            pulseql = fWork
            pulseqh = fWork - chip.nodes[qh]['anharm']

            T1Err1 = twoq_T1_err(
                pulseql,
                a[0],
                xtalkG.nodes[qcq]['two tq'],
                chip.nodes[ql]['T1 spectra']
            )
            T1Err2 = twoq_T1_err(
                pulseqh,
                a[0],
                xtalkG.nodes[qcq]['two tq'],
                chip.nodes[qh]['T1 spectra'],
            )
            T2Err1 = twoq_T2_err(
                pulseql,
                a[1],
                xtalkG.nodes[qcq]['two tq'],
                ac_spectrum_paras=chip.nodes[ql]['ac_spectrum'],
            )
            T2Err2 = twoq_T2_err(
                pulseqh,
                a[1],
                xtalkG.nodes[qcq]['two tq'],
                ac_spectrum_paras=chip.nodes[qh]['ac_spectrum'],
            )
            twoqDistErr = twoq_pulse_distort_err(
                [pulseqh, chip.nodes[qh]['frequency']],
                [pulseql, chip.nodes[ql]['frequency']],
                a[2],
                ac_spectrum_paras1=chip.nodes[qh]['ac_spectrum'],
                ac_spectrum_paras2=chip.nodes[ql]['ac_spectrum'],
            )
            innerLeakageErr = inner_leakage(
                    [pulseqh, chip.nodes[qh]['frequency']],
                    [pulseql, chip.nodes[ql]['frequency']],
                    a[3:5])
            
            twoqSpectatorErr = 1e-5
            for q in qcq:
                if q == ql:
                    pulse = pulseql
                else:
                    pulse = pulseqh

                for neighbor in chip[q]:
                    if neighbor in qcq:
                        continue
                    twoqSpectatorErrOnce = twoq_xtalk_err(
                            pulse,
                            chip.nodes[neighbor]['frequency'],
                            a[5:],
                            chip.nodes[q]['anharm'],
                            chip.nodes[neighbor]['anharm']
                        )
                        
                    if twoqSpectatorErrOnce > 4e-3:
                        if conflictSpectator.get(qcq, False):
                            conflictSpectator[qcq].append(neighbor)
                        else:
                            conflictSpectator[qcq] = [neighbor]
                        if qcq not in reOptimizeQCQs:
                            reOptimizeQCQs.append(qcq)
                    twoqSpectatorErr += twoqSpectatorErrOnce

            parallelErr = 1e-5
            for neighbor in xtalkG[qcq]:
                if xtalkG.nodes[neighbor].get('frequency', False):
                    for q0 in qcq:
                        for q1 in neighbor:
                            if (q0, q1) in chip.edges:
                                if q0 == ql:
                                    pulse = pulseql
                                else:
                                    pulse = pulseqh

                                if (
                                    chip.nodes[neighbor[0]]['frequency']
                                    < chip.nodes[neighbor[1]]['frequency']
                                ):
                                    q1l = neighbor[0]
                                else:
                                    q1l = neighbor[1]
                                if q1 == q1l:
                                    nPulse = xtalkG.nodes[neighbor]['frequency']
                                else:
                                    nPulse = (
                                        xtalkG.nodes[neighbor]['frequency']
                                        - chip.nodes[q1]['anharm']
                                    )

                                parallelErrOnce = twoq_xtalk_err(
                                        pulse,
                                        nPulse,
                                        a[5:],
                                        chip.nodes[q0]['anharm'],
                                        chip.nodes[q1]['anharm']
                                    )

                                if parallelErrOnce > 4e-3 and not (
                                    (qcq, neighbor) in conflictGatePairs
                                    or (neighbor, qcq) in conflictGatePairs
                                ):
                                    conflictGatePairs.append((qcq, neighbor))

                                    if qcq not in reOptimizeQCQs:
                                        reOptimizeQCQs.append(qcq)
                                parallelErr += parallelErrOnce

            allErr = (
                twoqSpectatorErr
                + parallelErr
                + T1Err1
                + T1Err2
                + T2Err1
                + T2Err2
                + twoqDistErr
            )
            error_chip += allErr
            qcq_num += 1
            xtalkG.nodes[qcq]['spectator err'] = twoqSpectatorErr
            xtalkG.nodes[qcq]['parallel err'] = parallelErr
            xtalkG.nodes[qcq]['innerLeakage err'] = innerLeakageErr
            xtalkG.nodes[qcq]['T err'] = T1Err1 + T1Err2 + T2Err1 + T2Err2
            xtalkG.nodes[qcq]['distort err'] = twoqDistErr
            xtalkG.nodes[qcq]['all err'] = allErr
            if allErr > 1.5e-2 and not (qcq in reOptimizeQCQs):
                reOptimizeQCQs.append(qcq)
                print(qcq, xtalkG.nodes[qcq]['all err'], 'qcq err')
    print('check, large err', reOptimizeQCQs)
    error_evarage = error_chip / qcq_num
    return reOptimizeQCQs, conflictGatePairs, conflictSpectator, error_evarage, xtalkG
