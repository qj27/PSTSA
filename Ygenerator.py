import numpy as np
import GetData



def y_generator(nofbus, bus, branch):
    '''

    :param numberofbus: int, 节点数
    :param bus: 3*n array, 节点号，并联电导，并联电纳
    :param branch: 5*n array, 起始节点，终止节点，串联电阻，串联电抗，并联电纳
    :return: 原始导纳矩阵，没考虑负荷和发电机，没收缩到发电机内节点
    '''
    Y = np.zeros((nofbus, nofbus), dtype=complex)
    for i in range(len(bus[0])):
        # print(bus[0][i])
        # print(bus[1][i])
        # print(bus[2][i])
        Y[bus[0][i] - 1][bus[0][i] - 1] += complex(bus[1][i], bus[2][i])  # shunt元件修正自导纳，对互导纳无影响
    for i in range(len(branch[0])):
        Y[branch[0][i] - 1][branch[0][i] - 1] += 1 / complex(branch[2][i], branch[3][i])  # branch串联元件修正始节点自导纳, r,x
        Y[branch[1][i] - 1][branch[1][i] - 1] += 1 / complex(branch[2][i], branch[3][i])  # branch串联元件修正末节点自导纳, r,x
        Y[branch[0][i] - 1][branch[0][i] - 1] += complex(0, branch[4][i] / 2)  # branch并联元件修正始节点自导纳, b/2
        Y[branch[1][i] - 1][branch[1][i] - 1] += complex(0, branch[4][i] / 2)  # branch并联元件修正末节点自导纳, b/2
        Y[branch[0][i] - 1][branch[1][i] - 1] += -1 / complex(branch[2][i], branch[3][i])  # branch串联元件修正始节点互导纳
        Y[branch[1][i] - 1][branch[0][i] - 1] += -1 / complex(branch[2][i], branch[3][i])  # branch串联元件修正末节点互导纳
        # branch 并联元件对互导纳没有影响
    return Y


def z_deltagenerator(type, y0=0, y2=0):
    '''
    待完善，应该能计算四类短路模式的附加阻抗
    :param type: 短路故障类型, int, 1-单相接地短路, 2-两相接地短路, 3-两相相间短路, 4-三相接地短路
    :param y0: 短路后零序导纳矩阵, (n+N*n+N)list
    :param y2: 短路后负序导纳矩阵, (n+N*n+N)list
    :return: 附加阻抗 Z_Δ, complex
    '''
    if (type-4) < 0.1:
        return 0.0000001 + 0.0000001j


def getfalut():
    i = int(input('输入故障线路起始端母线编号： '))
    j = int(input('输入故障线路终止端母线编号： '))
    k = int(input('输入故障发生位置（0-100, int）: '))
    type000 = int(input('输入故障类型（int, 1-单相接地短路, 2-两相接地短路, 3-两相相间短路, 4-三相接地短路）： '))
    r = z_deltagenerator(type000).real
    x = z_deltagenerator(type000).imag
    return [i, j, k, r, x]


def yalteredgenerator(ymatrix, load, generator, fault, type, linedata):
    '''
    设原系统有（n+N）条母线（节点）, n个发电机端节点, 则本函数生成的 Altered_Y 应该是2n+N 阶方阵
    :param ymatrix: 初始节点导纳矩阵, (n+N) * (n+N) array
    :param load: LoadData, 3*k list, 编号, r, x
    :param generator: 发电机信息矩阵, 8*n list, 机端节点编号, 发电机内节点编号, Xd', M, Pg, Qg, V, theta, 有用的只有generator[0], [1], [2]
    :param fault: 故障信息矩阵, 1*5 list, 起始线端int, 终止线端int, 故障位置int(0-100), 接地阻抗实部 R_Δ, 接地阻抗虚部 X_Δ
    :param type: 需要的是短路时段的节点导纳矩阵还是切除故障后的节点导纳矩阵, int, 0-短路时段, 1-故障切除
    :param linedata: 线路信息矩阵, 参数可以从 GetData 中获得
    '''
    yaltered = ymatrix[:].copy()
    temp = np.zeros((len(generator[0]), len(yaltered)))  # 发电机内节点使节点导纳矩阵增阶
    yaltered = np.row_stack((yaltered, temp))
    temp = np.zeros((len(yaltered), len(generator[0])))
    yaltered = np.column_stack((yaltered, temp))  # 增阶完成
    # 负荷等值阻抗对对应节点自导纳的修正，对互导纳没有影响
    for i in range(len(load[0])):
        yaltered[load[0][i] - 1][load[0][i] - 1] += 1 / complex(load[1][i], load[2][i])
    # 发电机直轴暂态电抗对节点导纳矩阵元素的修正
    for i in range(len(generator[0])):
        yd = 1 / (generator[2][i] * 1j)
        yaltered[generator[0][i] - 1][generator[0][i] - 1] += yd  # xd'对发电机机端节点自导纳的修正
        yaltered[generator[1][i] - 1][generator[1][i] - 1] += yd  # xd'对发电机内节点自导纳的修正
        yaltered[generator[0][i] - 1][generator[1][i] - 1] += -yd  # xd' 对机端和内节点间互导纳的修正
        yaltered[generator[1][i] - 1][generator[0][i] - 1] += -yd
    if type == 0:
        # 故障等效的等值阻抗对节点导纳矩阵的影响
        # 检查故障矩阵的前两元素是否为某条支路的两端，否则为数据输入错误
        lineexistance = False
        for i in range(len(linedata)):
            if ((linedata[0][i] - fault[0]) < 0.1) and ((linedata[1][i] - fault[1]) < 0.1):
                if fault[2] == 0:  # 故障发生在线路首端, 不需要增阶, 对首端节点的自导纳进行修正
                    yaltered[fault[0] - 1][fault[0] - 1] += 1 / complex(fault[3], fault[4])
                elif fault[2] == 100:  # 故障发生在线路末端, 不需要增阶，对末端节点的自导纳进行修正
                    yaltered[fault[1] - 1][fault[1] - 1] += 1 / complex(fault[3], fault[4])
                else:  # 故障发生在线路中间，不新增节点，而是采用星网变换，等效成同时发生在两端的两个短路
                    # 先把原来双回线中的一回的影响消除掉
                    # 自导纳
                    yaltered[fault[0] - 1][fault[0] - 1] += -1 / (2 * complex(linedata[2][i], linedata[3][i]))
                    yaltered[fault[1] - 1][fault[1] - 1] += -1 / (
                            2 * complex(linedata[2][i], linedata[3][i]))  # *2是因为认为双回线
                    # 互导纳
                    yaltered[fault[0] - 1][fault[1] - 1] += 1 / (2 * complex(linedata[2][i], linedata[3][i]))
                    yaltered[fault[1] - 1][fault[0] - 1] += 1 / (2 * complex(linedata[2][i], linedata[3][i]))
                    # 星网变换中的值的求解
                    zone = fault[2] / 100 * 2 * complex(linedata[2][i], linedata[3][i])
                    ztwo = (1 - fault[2] / 100) * 2 * complex(linedata[2][i], linedata[3][i])
                    zthree = complex(fault[3], fault[4])
                    sigmazz = zone * ztwo + zone * zthree + ztwo * zthree
                    zone_two = sigmazz / zthree
                    zone_three = sigmazz / ztwo
                    ztwo_three = sigmazz / zone
                    # 对节点导纳矩阵元素进行修正
                    yaltered[fault[0] - 1][fault[0] - 1] += 1 / zone_two + 1 / zone_three
                    yaltered[fault[1] - 1][fault[1] - 1] += 1 / zone_two + 1 / ztwo_three
                    yaltered[fault[0] - 1][fault[1] - 1] += -1 / zone_two
                    yaltered[fault[1] - 1][fault[0] - 1] += -1 / zone_two
                lineexistance = True
        if not lineexistance:
            print('This Line Donot Exist! ')
            return None
        else:
            return yaltered
    elif type == 1:
        # 故障切除对（已经完成了增阶和计入负荷、发电机影响的节点导纳矩阵中元素）的影响
        # 检查故障矩阵的前两元素是否为某条支路的两端，否则为数据输入错误
        lineexistance = False
        for i in range(len(linedata)):
            if ((linedata[0][i] - fault[0]) < 0.1) and ((linedata[1][i] - fault[1]) < 0.1):
                # 把原来双回线中的一回的影响消除掉,就可以了
                # 自导纳
                yaltered[fault[0] - 1][fault[0] - 1] += -1 / (2 * complex(linedata[2][i], linedata[3][i]))
                yaltered[fault[1] - 1][fault[1] - 1] += -1 / (2 * complex(linedata[2][i], linedata[3][i]))  # *2是因为认为双回线
                # 互导纳
                yaltered[fault[0] - 1][fault[1] - 1] += 1 / (2 * complex(linedata[2][i], linedata[3][i]))
                yaltered[fault[1] - 1][fault[0] - 1] += 1 / (2 * complex(linedata[2][i], linedata[3][i]))
                lineexistance = True
        if not lineexistance:
            print('This Line Donot Exist! ')
            return None
        else:
            return yaltered
    else:
        print('Error: type = 0 or 1. ( given: ', type, ')')
        return None


def yorderreducedgenerator(yalteredmatrix, numberofenode):
    '''
    收缩到发电机内节点
    :param yalteredmatrix: (n+N)*(n+N)array
    :param numberofenode: int, 需要保留的E节点个数, 和之前的函数配合, 需要保留的节点即为倒数 numberofenode 个 节点
    :return: n*n array, 收缩到发电机内节点(E节点)的节点导纳矩阵
    '''
    # 分块矩阵yall = [[ynn, yne], [yen, yee]]
    yall = yalteredmatrix[:].copy()
    ynn = (yall[: len(yalteredmatrix) - numberofenode].transpose())[
          :len(yalteredmatrix) - numberofenode].transpose().copy()
    yne = (yall[: len(yalteredmatrix) - numberofenode].transpose())[-numberofenode:].transpose().copy()
    yen = (yall[-numberofenode:].transpose())[: len(yalteredmatrix) - numberofenode].transpose().copy()
    yee = (yall[-numberofenode:].transpose())[-numberofenode:].transpose().copy()
    yorderreduced = yee - np.dot(np.dot(yen, np.linalg.inv(ynn)), yne)
    return yorderreduced


if __name__ == '__main__':

    NumberOfBus = GetData.getnumberofbus()
    BusData = GetData.getshuntdata()
    LineData = GetData.getlinedata()
    GeneratorData = GetData.getgeneratordata()
    LoadData = GetData.getloaddata()
    Ym = y_generator(NumberOfBus, BusData, LineData)
    Ymlist = Ym.tolist().copy()
    print(Ym)
    for row in Ymlist:
        print(row)
    print('-----------------------------------------------------------------------------------------------------------')
    YalterdSC = yalteredgenerator(Ym, LoadData, GeneratorData, [16, 19, 80, 0.000001, 0.000001], 0, LineData)
    YalterdFC = yalteredgenerator(Ym, LoadData, GeneratorData, [16, 19, 80, 0.000001, 0.000001], 1, LineData)
    print(YalterdSC)
    print(yorderreducedgenerator(YalterdSC, len(GeneratorData[0])))
    print('end')
