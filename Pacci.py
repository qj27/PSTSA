import math
import numpy as np

import GetData
import Ygenerator


class Generator:
    def __init__(self, number, e, pm, m):
        self.E = e
        self.Pmi = pm
        self.num = number
        self.Mi = m  # E 是对应发电机的电动势, Pmi是发电机对应的机械功率, num是发电机对应节点导纳矩阵的编号, Mi是对应发电机的惯性时间常数


def pe_calculator(yormatrix, enodedata, number):
    '''
    :param yormatrix: 收缩到发电机内节点的节点导纳矩阵, 可以是短路状态下的，也可以是切除故障状态下的. n*n array, 与发动机编号对应
    :param enodedata: 发电机内节点信息矩阵 [[Ni(E节点编号), Pm, E, delta]*n]
    :param number: 所求功率的节点在 yormatrix 中对应的 行号+1 (也是列号+1)
    return
    '''
    pe = 0.0
    # yormatrix 中 行号（列号）与发电机节点编号是对应的，但 enodedata 中不是，所以要进行匹配
    # 方法是认定列号-寻找发电机机端节点编号-对应的E, 这个方法应该更简单, 避免了一次搜索
    for i in range(len(EData[0])):
        if EData[0][i] == number:
            for j in range(len(yormatrix)):
                if number == j:
                    pe += enodedata[3][i] ** 2 * yormatrix[number - 1][j].real
                else:
                    pe += enodedata[3][i] * enodedata[3][j] * yormatrix[number - 1][j].imag * math.sin(
                        enodedata[4][i] - enodedata[4][j])
                    pe += enodedata[3][i] * enodedata[3][j] * yormatrix[number - 1][j].real * math.cos(
                        enodedata[4][i] - enodedata[4][j])
    return pe


NumberOfBus = GetData.getnumberofbus()
BusData = GetData.getshuntdata()
LineData = GetData.getlinedata()
GeneratorData = GetData.getgeneratordata()
LoadData = GetData.getloaddata()
EData = GetData.getedata()  # [Ni(E节点编号), Pm, E, delta]


# fault = Ygenerator.getfalut()
fault = [16, 19, 80, 0.000001, 0.000001]
Ym = Ygenerator.y_generator(NumberOfBus, BusData, LineData)
YalterdSC = Ygenerator.yalteredgenerator(Ym, LoadData, GeneratorData, fault, 0, LineData)
YOrderReducedSC = Ygenerator.yorderreducedgenerator(YalterdSC, len(GeneratorData[0]))

print(EData)
print(YOrderReducedSC)
print(GeneratorData)
Pein = []
Pei = []
for i in range(len(GeneratorData[0])):
    Pein.append(i+1)
    Pei.append(pe_calculator(YOrderReducedSC, EData, i+1))
    print('Pe', i+1, '=  ', pe_calculator(YOrderReducedSC, EData, i+1))
Pei = [Pein] + [Pei]  # 第一行是发电机机端节点编号, 第二行是短路状态下的发电机电磁功率
print(Pei)

G = []
for i in range(len(GeneratorData[0])):
    G.append(Generator(GeneratorData[0][i], EData[2][i], EData[4][i], GeneratorData[3][i]))

#def __init__(self, number, e, pm, m):
