import math

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

# fault = Ygenerator.getfalut()  # 这一行用以指定故障, 实例见下一行
fault = [16, 19, 80, 0.000001, 0.000001]  # [int, int, int, float, float]即[线路起始节点，终止节点，故障位置（发生在线路百分之多少处），附加阻抗实部，附加阻抗虚部]

# Ym 为正常的Y矩阵, 没有考虑发电机影响, 没有考虑负荷, 没有考虑故障, array
# Yalter 为‘变化’后的Y矩阵,考虑了发电机、负荷、故障, SC对应Short Circuit即短路, FC对应Falut Cleared 即故障切除
# YOrderReduced 为‘降阶’后的Y矩阵, 收缩到了发电机内节点, 采用算例数据时应为8阶, SC和FC的含义见上一行 ↑
Ym = Ygenerator.y_generator(NumberOfBus, BusData, LineData)
YOrderReducedNormal = Ygenerator.yorderreducedgenerator(Ym, len(GeneratorData[0]))
YalterdSC = Ygenerator.yalteredgenerator(Ym, LoadData, GeneratorData, fault, 0, LineData)
YOrderReducedSC = Ygenerator.yorderreducedgenerator(YalterdSC, len(GeneratorData[0]))
YalterdFC = Ygenerator.yalteredgenerator(Ym, LoadData, GeneratorData, fault, 1, LineData)
YOrderReducedFC = Ygenerator.yorderreducedgenerator(YalterdFC, len(GeneratorData[0]))

# print(EData)
# print(YOrderReducedSC)
# print(GeneratorData)
Pein = []
Pei = []
for i in range(len(GeneratorData[0])):
    Pein.append(i + 1)
    Pei.append(pe_calculator(YOrderReducedSC, EData, i + 1))
    print('Pe', i + 1, '=  ', pe_calculator(YOrderReducedSC, EData, i + 1))
Pei = [Pein] + [Pei]  # 第一行是发电机机端节点编号, 第二行是短路状态下的发电机电磁功率
print(Pei)

G = []
for i in range(len(GeneratorData[0])):
    G.append(Generator(GeneratorData[0][i], EData[2][i], EData[4][i], GeneratorData[3][i]))
# G 是一个list, 其元素为 Class Generator 的对象, 这里还没有排序
# print('Gtemp', G)

for i in range(len(GeneratorData[0]) - 1):  # 作排序
    for j in range(len(GeneratorData[0]) - i - 1):
        if G[j].num > G[j + 1].num:
            G[j], G[j + 1] = G[j + 1], G[j]  # 排序完成
# print('G: ', G)

PaccdivdM = []
for i in range(len(GeneratorData[0])):
    for j in range(len(GeneratorData[0])):
        if Pei[0][i] == G[j].num:
            pacci = G[j].Pmi - Pei[1][i]
            PaccdivdM.append(pacci / G[j].Mi)
            break
PaccdivdM = [Pein] + [PaccdivdM]  # 加角速度矩阵, 第一行是编号, 第二行是加角速度
print(PaccdivdM)
