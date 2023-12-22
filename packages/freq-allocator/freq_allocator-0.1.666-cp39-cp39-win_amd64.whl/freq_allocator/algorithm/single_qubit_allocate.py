from copy import deepcopy
import os
import pickle
import time
import warnings
import geatpy as ea
from matplotlib import pyplot as plt
import matplotlib
import numpy as np
from freq_allocator.dataloader import gen_pos
import networkx as nx
from freq_allocator.model.single_qubit_model import single_err_model, singq_xtalk_err, singq_residual_err #, twoq_dist_bound
from freq_allocator.model.formula import freq_var_map
from sko.PSO import PSO
import random

def checkcoli(chip, a, varType):
    reOptimizeNodes = []
    conflictXyDict = dict()
    conflictResPairs = []
    # distParis = []
    for qubit in chip.nodes():
        if chip.nodes[qubit].get('frequency', False):
            if varType == 'double':
                isolateErr = chip.nodes[qubit]['isolated_error'](chip.nodes[qubit]['frequency'])
            else:
                isolateErr = chip.nodes[qubit]['isolated_error'][chip.nodes[qubit]['allow freq'].index(chip.nodes[qubit]['frequency'])]
            xyErr = 0
            residualErr = 0
            distBoundErr = 0
            for neighbor in chip.nodes():
                if chip.nodes[neighbor].get('frequency', False) and not(neighbor == qubit):
                    if chip.nodes[neighbor]['name'] in chip.nodes[qubit]['xy_crosstalk_coef']:
                        xyErrEachPair = singq_xtalk_err(a[2], chip.nodes[neighbor]['frequency'] - chip.nodes[qubit]['frequency'], 
                                                chip.nodes[qubit]['xy_crosstalk_coef'][chip.nodes[neighbor]['name']], 
                                                chip.nodes[qubit]['xy_crosstalk_f'])
                        xyErr += xyErrEachPair
                        if xyErrEachPair > 4e-3:
                            if conflictXyDict.get(qubit, False):
                                conflictXyDict[qubit].append(neighbor)
                            else:
                                conflictXyDict[qubit] = [neighbor]

                    if (qubit, neighbor) in chip.edges():
                        nResidualErr = singq_residual_err(a[0], a[1],                         
                                                chip.nodes[neighbor]['frequency'],
                                                chip.nodes[qubit]['frequency'],
                                                chip.nodes[neighbor]['anharm'],
                                                chip.nodes[qubit]['anharm'])
                        residualErr += nResidualErr
                        if nResidualErr > 2.5e-3 and not((qubit, neighbor) in conflictResPairs or (neighbor, qubit) in conflictResPairs):
                            conflictResPairs.append((qubit, neighbor))
                        
                        # distBoundErrEach = twoq_dist_bound(chip.nodes[qubit]['freq_max'], 
                        #                             chip.nodes[neighbor]['freq_max'],
                        #                             chip.nodes[qubit]['frequency'],
                        #                             chip.nodes[neighbor]['frequency'],
                        #                             a[-1])
                        # distBoundErr += distBoundErrEach
                        # if distBoundErrEach > 1e-3 and not((qubit, neighbor) in distParis or (neighbor, qubit) in distParis):
                        #     distParis.append((qubit, neighbor))

                        for nNeighbor in chip[neighbor]:
                            if nNeighbor == qubit:
                                continue
                            elif chip.nodes[nNeighbor].get('frequency', False):
                                nnResidualErr = singq_residual_err(a[2], a[3], 
                                                    chip.nodes[nNeighbor]['frequency'],
                                                    chip.nodes[qubit]['frequency'],
                                                    chip.nodes[nNeighbor]['anharm'],
                                                    chip.nodes[qubit]['anharm'])
                                residualErr += nnResidualErr
                            if nResidualErr > 2.5e-3 and not((qubit, nNeighbor) in conflictResPairs or (nNeighbor, qubit) in conflictResPairs):
                                conflictResPairs.append((qubit, nNeighbor))

            allErr = isolateErr + xyErr + residualErr# + distBoundErr
            if allErr > 1e-2 and not(qubit in reOptimizeNodes):
                reOptimizeNodes.append(qubit)
                print(qubit, allErr, 'single qubit err')
            chip.nodes[qubit]['xy err'] = xyErr
            chip.nodes[qubit]['residual err'] = residualErr
            # chip.nodes[qubit]['distort bound err'] = distBoundErr
            chip.nodes[qubit]['isolate err'] = isolateErr
            chip.nodes[qubit]['all err'] = allErr
    print('check, large err', reOptimizeNodes)
    return reOptimizeNodes, conflictXyDict, conflictResPairs#, distBoundErr

def sing_alloc(chip : nx.Graph, a, s: int = 1, varType='double'):
    epoch = 0
    centerConflictNode = (0, 0)
    avgErrEpoch = []
    newreOptimizeNodes = []
    hisReOptimizeNodes = []
    hisChip = []
    jumpToEmpty = False

    fixQ = []
    for qubit in chip.nodes:
        if len(chip.nodes[qubit]['allow freq']) == 2:
            fixQ.append(qubit)
            chip.nodes[qubit]['frequency'] = chip.nodes[qubit]['allow freq'][0]

    while len([chip.nodes[qubit]['all err'] for qubit in chip.nodes if chip.nodes[qubit].get('all err', False)]) < len(chip.nodes) or \
        (not(jumpToEmpty) and len([chip.nodes[qubit]['all err'] for qubit in chip.nodes if chip.nodes[qubit].get('all err', False)]) == len(chip.nodes)):
        
        reOptimizeNodes = [centerConflictNode]
        for qubit in chip.nodes():
            if centerConflictNode in newreOptimizeNodes and not(qubit in reOptimizeNodes) and \
                qubit in newreOptimizeNodes and \
                not(qubit in fixQ):
                reOptimizeNodes.append(qubit)
            elif not(chip.nodes[centerConflictNode].get('frequency', False)) and not(qubit in reOptimizeNodes) and \
                not(chip.nodes[qubit].get('frequency', False)) and \
                np.abs(qubit[0] - centerConflictNode[0]) + np.abs(qubit[1] - centerConflictNode[1]) <= s and \
                not(qubit in fixQ):
                reOptimizeNodes.append(qubit)
        print('optimize qubits: ', reOptimizeNodes)

        if varType == 'double':
            result_list = []
            fun_list = []
            for _ in range(10):
                lb = [0] * len(reOptimizeNodes)
                ub = [1] * len(reOptimizeNodes)

                func = lambda x : single_err_model(x, chip, reOptimizeNodes, a, varType)

                pso = PSO(func=func, dim=len(reOptimizeNodes), pop=60, max_iter=200, lb=lb, ub=ub)
                pso.run()
                result_list.append(freq_var_map(pso.gbest_x[reOptimizeNodes.index(qubit)], chip.nodes[qubit]['allow freq']))
                fun_list.append(pso.gbest_y[0])
            best_freq = result_list[fun_list.index(min(fun_list))]
            for qubit in reOptimizeNodes:
                chip.nodes[qubit]['frequency'] = best_freq[reOptimizeNodes.index(qubit)]

        else:
            result_list = []
            for _ in range(3):
                lb = [0] * len(reOptimizeNodes)
                ub = [len(chip.nodes[qubit]['allow freq']) - 1 for qubit in reOptimizeNodes]

                @ea.Problem.single
                def err_model_fun(frequencys):
                    return single_err_model(frequencys, chip, reOptimizeNodes, a, varType)

                problem = ea.Problem(
                    name='soea err model',
                    M=1,  # 初始化M（目标维数）
                    maxormins=[1],  # 初始化maxormins（目标最小最大化标记列表，1：最小化该目标；-1：最大化该目标）
                    Dim=len(reOptimizeNodes),  # 决策变量维数
                    varTypes=[1] * len(reOptimizeNodes),  # 决策变量的类型列表，0：实数；1：整数
                    lb=lb,  # 决策变量下界
                    ub=ub,  # 决策变量上界
                    evalVars=err_model_fun
                )

                algorithm = ea.soea_DE_best_1_bin_templet(
                    problem,
                    ea.Population(Encoding='RI', NIND=100),
                    MAXGEN=200,
                    logTras=1,
                    # trappedValue=1e-10,
                    # maxTrappedCount=20
                )
                algorithm.mutOper.F = 1
                algorithm.recOper.XOVR = 1

                # algorithm.run()

                freq_bset = None
                res = ea.optimize(
                    algorithm,
                    prophet=freq_bset,
                    # prophet=np.array(self.experiment_options.FIR0),
                    verbose=True, drawing=0, outputMsg=False,
                    drawLog=False, saveFlag=True, dirName='results\\'
                )
                result_list.append(res)
                if res['ObjV'] < 5e-3:
                    break
            fun_list = [res['ObjV'] for res in result_list]
            freq_list_bset = result_list[fun_list.index(min(fun_list))]['Vars'][0]
            print(f'qubit num: {len(reOptimizeNodes)}')
            for qubit in reOptimizeNodes:
                chip.nodes[qubit]['frequency'] = chip.nodes[qubit]['allow freq'][freq_list_bset[reOptimizeNodes.index(qubit)]]

        newreOptimizeNodes, conflictXyDict, conflictResPairs = checkcoli(chip, a, varType)
        hisChip.append(deepcopy(chip))
        hisReOptimizeNodes.append(set(newreOptimizeNodes))
        on = [len(h) for h in hisReOptimizeNodes]

        if len(hisReOptimizeNodes) > 5 or min(on) == 0:
            on = [len(h) for h in hisReOptimizeNodes]
            chip = hisChip[on.index(min(on))]
            print('jump', on, on.index(min(on)), 'is the chip with smallest conflict qubits.')
            jumpToEmpty = True
        else:
            print('no jump')
            jumpToEmpty = False

        avgErrEpoch.append(sum([chip.nodes[qubit]['all err'] for qubit in chip.nodes if chip.nodes[qubit].get('all err', False)]) / 
                           len([chip.nodes[qubit]['all err'] for qubit in chip.nodes if chip.nodes[qubit].get('all err', False)]))
        print('avg err estimate', avgErrEpoch)
        if len([chip.nodes[qubit]['all err'] for qubit in chip.nodes if chip.nodes[qubit].get('all err', False)]) == len(chip.nodes):
            bestFreq = [chip.nodes[qubit]['frequency'] for qubit in chip.nodes]
            bestIsolateErr = [chip.nodes[qubit]['isolate err'] for qubit in chip.nodes]
            bestXyErr = [chip.nodes[qubit]['xy err'] for qubit in chip.nodes]
            bestResidualErr = [chip.nodes[qubit]['residual err'] for qubit in chip.nodes]
            # bestDistBoundErr = [chip.nodes[qubit]['distort bound err'] for qubit in chip.nodes]
            bestAllErr = [chip.nodes[qubit]['all err'] for qubit in chip.nodes]
            conflictXyDictFinal = conflictXyDict
            conflictResPairFinal = conflictResPairs
            # distBoundErrFinal = distBoundErr

        pos = gen_pos(chip)
        labelDict = dict([(i, i) for i in chip.nodes])
        errList = [np.log10(chip.nodes[i].get('all err', 1e-5)) for i in chip.nodes]
        errLow = min(errList)
        errHigh = max(errList)
        plt.figure(figsize=(8, 8))
        nx.draw_networkx_labels(chip, pos, labelDict, font_size=14, font_color="black")
        nx.draw_networkx_edges(chip, pos, edgelist=chip.edges, edge_cmap='coolwarm')
        nx.draw_networkx_nodes(chip, pos, nodelist=chip.nodes, node_color=errList, cmap='coolwarm')
        plt.axis('off')
        plt.colorbar(matplotlib.cm.ScalarMappable(norm=matplotlib.colors.Normalize(vmin=errLow, vmax=errHigh), cmap='coolwarm'))
        plt.savefig('results\\' + str(epoch) + 'chip err.pdf', dpi=300)
        plt.close()


        reOptimizeNodeDict = dict()
        for qubit in newreOptimizeNodes:
            if not(nx.has_path(chip, qubit, centerConflictNode)):
                reOptimizeNodeDict[qubit] = 10000
            else:
                reOptimizeNodeDict[qubit] = nx.shortest_path_length(chip, qubit, centerConflictNode)

        emptyNodeDict = dict()
        for qubit in chip.nodes():
            if not(chip.nodes[qubit].get('frequency', False)):
                if not(nx.has_path(chip, qubit, centerConflictNode)):
                    emptyNodeDict[qubit] = 10000
                else:
                    emptyNodeDict[qubit] = nx.shortest_path_length(chip, qubit, centerConflictNode)

        if len(reOptimizeNodeDict) > 0 and not(jumpToEmpty):
            print('reoptimize qubit distance', reOptimizeNodeDict)
            centerConflictNode = random.choices(list(reOptimizeNodeDict.keys()), weights=[1 / max(0.5, distance) for distance in reOptimizeNodeDict.values()], k=1)[0]
        elif len(emptyNodeDict) > 0:
            hisReOptimizeNodes = []
            hisChip = []
            jumpToEmpty = False
            print('empty qubit distance', emptyNodeDict)
            centerConflictNode = list(sorted(emptyNodeDict.items(), key=lambda x : x[1]))[0][0]
        epoch += 1

    print('ave', avgErrEpoch)
    plt.plot(avgErrEpoch, label='err epoch')
    plt.xlabel('epoch')
    plt.legend()
    plt.savefig('results\\' + 'err.pdf', dpi=300)
    plt.close()

    for qubit in chip.nodes:
        chip.nodes[qubit]['frequency'] = bestFreq[list(chip.nodes).index(qubit)]

    pos = gen_pos(chip)
    labelDict = dict([(i, i) for i in chip.nodes])
    errList = np.log10(bestIsolateErr)
    errLow = min(errList)
    errHigh = max(errList)
    plt.figure(figsize=(8, 8))
    nx.draw_networkx_labels(chip, pos, labelDict, font_size=14, font_color="black")
    nx.draw_networkx_edges(chip, pos, edgelist=chip.edges, edge_cmap='coolwarm')
    nx.draw_networkx_nodes(chip, pos, nodelist=chip.nodes, node_color=errList, cmap='coolwarm')
    plt.axis('off')
    plt.colorbar(matplotlib.cm.ScalarMappable(norm=matplotlib.colors.Normalize(vmin=errLow, vmax=errHigh), cmap='coolwarm'))
    plt.savefig('results\\' + 'best' + 'chip isolate err.pdf', dpi=300)
    plt.close()

    pos = gen_pos(chip)
    labelDict = dict([(i, i) for i in chip.nodes])
    errList = np.log10(bestXyErr)
    errLow = min(errList)
    errHigh = max(errList)
    plt.figure(figsize=(8, 8))
    nx.draw_networkx_labels(chip, pos, labelDict, font_size=14, font_color="black")
    nx.draw_networkx_edges(chip, pos, edgelist=chip.edges, edge_cmap='coolwarm')
    nx.draw_networkx_nodes(chip, pos, nodelist=chip.nodes, node_color=errList, cmap='coolwarm')
    plt.axis('off')
    plt.colorbar(matplotlib.cm.ScalarMappable(norm=matplotlib.colors.Normalize(vmin=errLow, vmax=errHigh), cmap='coolwarm'))
    plt.savefig('results\\' + 'best' + 'chip xy err.pdf', dpi=300)
    plt.close()

    pos = gen_pos(chip)
    labelDict = dict([(i, i) for i in chip.nodes])
    errList = np.log10(bestResidualErr)
    errLow = min(errList)
    errHigh = max(errList)
    plt.figure(figsize=(8, 8))
    nx.draw_networkx_labels(chip, pos, labelDict, font_size=14, font_color="black")
    nx.draw_networkx_edges(chip, pos, edgelist=chip.edges, edge_cmap='coolwarm')
    nx.draw_networkx_nodes(chip, pos, nodelist=chip.nodes, node_color=errList, cmap='coolwarm')
    plt.axis('off')
    plt.colorbar(matplotlib.cm.ScalarMappable(norm=matplotlib.colors.Normalize(vmin=errLow, vmax=errHigh), cmap='coolwarm'))
    plt.savefig('results\\' + 'best' + 'chip residual err.pdf', dpi=300)
    plt.close()

    # pos = gen_pos(chip)
    # labelDict = dict([(i, i) for i in chip.nodes])
    # errList = np.log10(bestDistBoundErr)
    # errLow = min(errList)
    # errHigh = max(errList)
    # plt.figure(figsize=(8, 8))
    # nx.draw_networkx_labels(chip, pos, labelDict, font_size=14, font_color="black")
    # nx.draw_networkx_edges(chip, pos, edgelist=chip.edges, edge_cmap='coolwarm')
    # nx.draw_networkx_nodes(chip, pos, nodelist=chip.nodes, node_color=errList, cmap='coolwarm')
    # plt.axis('off')
    # plt.colorbar(matplotlib.cm.ScalarMappable(norm=matplotlib.colors.Normalize(vmin=errLow, vmax=errHigh), cmap='coolwarm'))
    # plt.savefig('results\\' + 'best' + 'chip distort err.pdf', dpi=300)
    # plt.close()

    pos = gen_pos(chip)
    labelDict = dict([(i, i) for i in chip.nodes])
    errList = np.log10(bestAllErr)
    errLow = min(errList)
    errHigh = max(errList)
    plt.figure(figsize=(8, 8))
    nx.draw_networkx_labels(chip, pos, labelDict, font_size=14, font_color="black")
    nx.draw_networkx_edges(chip, pos, edgelist=chip.edges, edge_cmap='coolwarm')
    nx.draw_networkx_nodes(chip, pos, nodelist=chip.nodes, node_color=errList, cmap='coolwarm')
    plt.axis('off')
    plt.colorbar(matplotlib.cm.ScalarMappable(norm=matplotlib.colors.Normalize(vmin=errLow, vmax=errHigh), cmap='coolwarm'))
    plt.savefig('results\\' + 'best' + 'chip all err.pdf', dpi=300)
    plt.close()

    pos = gen_pos(chip)
    freqList = [int(round(chip.nodes[qubit]['frequency'], 3)) for qubit in chip.nodes]
    qlow = min(freqList)
    qhigh = max(freqList)
    freqDict = dict([(i, int(round(chip.nodes[i]['frequency'], 3))) for i in chip.nodes])
    plt.figure(figsize=(8, 8))
    nx.draw_networkx_labels(chip, pos, freqDict, font_size=14, font_color="black")
    nx.draw_networkx_edges(chip, pos, edgelist=chip.edges, edge_cmap='coolwarm')
    nx.draw_networkx_nodes(chip, pos, nodelist=chip.nodes, node_color=freqList, cmap='coolwarm')
    plt.axis('off')
    plt.colorbar(matplotlib.cm.ScalarMappable(norm=matplotlib.colors.Normalize(vmin=qlow, vmax=qhigh), cmap='coolwarm'))
    plt.savefig('results\\' + 'chip freq.pdf', dpi=300)
    plt.close()

    errList = bestXyErr
    labelList = list(chip.nodes)
    # plt.scatter([str(i) for i in labelList], errList, color='blue', alpha=0.5, s=100)
    plt.scatter([range(len(labelList))], errList, color='blue', alpha=0.5, s=100)
    plt.axhline(y=1e-2, color='red', linestyle='--')
    plt.semilogy()
    plt.savefig('results\\' + 'xy err scatter.pdf', dpi=300)
    plt.close()

    errList = bestResidualErr
    labelList = list(chip.nodes)
    # plt.scatter([str(i) for i in labelList], errList, color='blue', alpha=0.5, s=100)
    plt.scatter([range(len(labelList))], errList, color='blue', alpha=0.5, s=100)
    plt.axhline(y=1e-2, color='red', linestyle='--')
    plt.semilogy()
    plt.savefig('results\\' + 'residual err scatter.pdf', dpi=300)
    plt.close()

    errList = bestAllErr
    labelList = list(chip.nodes)
    # plt.scatter([str(i) for i in labelList], errList, color='blue', alpha=0.5, s=100)
    plt.scatter([range(len(labelList))], errList, color='blue', alpha=0.5, s=100)
    plt.axhline(y=1e-2, color='red', linestyle='--')
    plt.semilogy()
    plt.savefig('results\\' + 'all err scatter.pdf', dpi=300)
    plt.close()

    errList = bestIsolateErr
    labelList = list(chip.nodes)
    # plt.scatter([str(i) for i in labelList], errList, color='blue', alpha=0.5, s=100)
    plt.scatter([range(len(labelList))], errList, color='blue', alpha=0.5, s=100)
    plt.axhline(y=1e-2, color='red', linestyle='--')
    plt.semilogy()
    plt.savefig('results\\' + 'isolate err scatter.pdf', dpi=300)
    plt.close()

    with open('results\\chip err.txt', 'w') as fp:
        for qubit in chip.nodes:
            fp.write(str(qubit) + ' frequency: ' + str(round(bestFreq[list(chip.nodes).index(qubit)])) +
                     ', isolate error: ' + str(round(bestIsolateErr[list(chip.nodes).index(qubit)], 7)) +
                     ', xy error: ' + str(round(bestXyErr[list(chip.nodes).index(qubit)], 7)) +
                    #  ', distort error: ' + str(round(bestDistBoundErr[list(chip.nodes).index(qubit)], 7)) +
                     ', residual error: ' + str(round(bestResidualErr[list(chip.nodes).index(qubit)], 7)) +
                     ', all error: ' + str(round(bestAllErr[list(chip.nodes).index(qubit)], 7)) + 
                     '\n')
    with open('results\\conflict xy dict.txt', 'w') as fp:
        for qubit in conflictXyDictFinal:
            fp.write(str(qubit) + ': ')
            for neighbor in conflictXyDictFinal[qubit]:
                fp.write(str(neighbor) + ' ')
            fp.write('\n')
    with open('results\\conflict residual pair.txt', 'w') as fp:
        for pair in conflictResPairFinal:
            fp.write(str(pair) + '\n')
    # with open('results\\conflict distort pair.txt', 'w') as fp:
    #     for pair in distBoundErrFinal:
    #         fp.write(str(pair) + '\n')


    return chip

