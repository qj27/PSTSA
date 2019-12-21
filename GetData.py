import math

import numpy as np
from sympy import *

np.set_printoptions(precision=3, suppress=True)
# 读取潮流数据[U, theta, P_generated, Q_generated, P_loss, Q_loss]
f = open("PowerFlow.txt", "r", encoding='utf-8')
f_read = f.read()
# print(f_read)
f.close()
f = open("PowerFlow.txt", "r", encoding='utf-8')
l = []
for line in f:
    t = f.read(7)
    del (t)
    num = list(line.split())
    l.append(num)
del (l[0])
chaoliu = []
i = 0
while i < len(l):
    j = 0
    p = []
    while j < len(l[0]):
        if j > 0:
            p.append(float(l[i][j]))
        else:
            p.append(int(l[i][j]))
        j += 1
    chaoliu.append(p)
    i += 1
# print('chaoliu: ', chaoliu)
f.close()

# 读取BUS.con母线数据【编号、基准电压、电压初始幅值猜测p.u.、电压初始相位猜测、区号、地区编号】
file = open("d_036.txt", "r", encoding='utf-8')
B = []
a = file.readlines()[1:37]
for line in a:
    num = list(line.split())
    B.append(num)
BUS_data = []
i = 0
while i < len(B):
    j = 0
    p = []
    while j < len(B[0]):
        p.append(float(B[i][j]))
        j += 1
    BUS_data.append(p)
    i += 1
# print('Bus_data: ', BUS_data)
file.close()

# 读取line.con支路数据【起始线I侧、终点线J侧、额定功率、额定电压、额定频率、线长、无用、电阻p.u.、电抗p.u.、电纳p.u.、无用、无用、电流限幅p.u、有功限幅pu、视在功率限幅pu、连接状态】
file = open("d_036.txt", "r", encoding='utf-8')
C = []
b = file.readlines()[40:82]
for line in b:
    num = list(line.split())
    C.append(num)
line_data = []
i = 0
while i < len(C):
    j = 0
    p = []
    while j < len(C[0]):
        p.append(float(C[i][j]))
        j += 1
    line_data.append(p)
    i += 1
# print(line_data)
file.close()

# 读取Shunt.con分流导纳数据格式[BUS号码、额定功率、额定电压、额定频率、电导率pu、电纳pu、连接状态0/1]
file = open("d_036.txt", "r", encoding='utf-8')
C = []
b = file.readlines()[86:94]
for line in b:
    num = list(line.split())
    C.append(num)
Shunt_data = []
i = 0
while i < len(C):
    j = 0
    p = []
    while j < len(C[0]):
        p.append(float(C[i][j]))
        j += 1
    Shunt_data.append(p)
    i += 1
# print(Shunt_data)
file.close()

# 读取SW.con备用发电机数据【编号、额定功率、额定电压、电压幅值pu、参考角度pu、最大无功功率pu、最小无功功率pu、最大电压pu、最小电压pu、？、？】
file = open("d_036.txt", "r", encoding='utf-8')
C = []
b = file.readlines()[97:98]
for line in b:
    num = list(line.split())
    C.append(num)
SW_data = []
i = 0
while i < len(C):
    j = 0
    p = []
    while j < len(C[0]):
        p.append(float(C[i][j]))
        j += 1
    SW_data.append(p)
    i += 1
# print(SW_data)
file.close()

# 读取PV.con【编号、额定功率、额定电压、有功功率pu、电压幅值pu、最大无功功率pu、最小无功功率pu、最大电压pu、最小电压pu、损失参与系数、连接状态】
file = open("d_036.txt", "r", encoding='utf-8')
C = []
b = file.readlines()[101:108]
for line in b:
    num = list(line.split())
    C.append(num)
PV_data = []
i = 0
while i < len(C):
    j = 0
    p = []
    while j < len(C[0]):
        p.append(float(C[i][j]))
        j += 1
    PV_data.append(p)
    i += 1
# print(PV_data)
file.close()

# 读取Ind.con感应电机数据【编号、额定功率、额定电压、额定频率、moedl order、启动控制、定子电阻pu、定子电抗pu、
# 第一笼转子电阻pu、第一笼转子电抗pu、第二笼转子电阻pu、第二笼转子电抗pu、磁化电抗KWs/kVA、惯性常数pu、a pu、b pu、c pu（Tm=a+b*w+c*w*w为机电时间常数）、开始时间、是否允许刹车、连接状态】】
file = open("d_036.txt", "r", encoding='utf-8')
C = []
b = file.readlines()[119:120]
for line in b:
    num = list(line.split())
    C.append(num)
Ind_data = []
i = 0
while i < len(C):
    j = 0
    p = []
    while j < len(C[0]):
        p.append(float(C[i][j]))
        j += 1
    Ind_data.append(p)
    i += 1
# print(Ind_data)
file.close()

# 读取PQ.con【编号、额定功率、额定电压、有功功率pu、无功功率pu、最大电压pu、最小电压pu、是否允许转移为阻抗、连接状态】
file = open("d_036.txt", "r", encoding='utf-8')
C = []
b = file.readlines()[123:132]
for line in b:
    num = list(line.split())
    C.append(num)
PQ_data = []
i = 0
while i < len(C):
    j = 0
    p = []
    while j < len(C[0]):
        p.append(float(C[i][j]))
        j += 1
    PQ_data.append(p)
    i += 1
# print(PQ_data)
file.close()

# 读取syn.con发电机【接入母线编号、Sn、Vn、fn、发电机模型、漏电抗、ra pu、xd pu、xd' pu、
# xd'' pu、Td0'、Td0''、xq pu、xq' pu、xq'' pu、Tq0'、Tq0''、M（M=2H）、D（阻尼系数）】
file = open("d_036.txt", "r", encoding='utf-8')
C = []
b = file.readlines()[137:145]
for line in b:
    num = list(line.split())
    C.append(num)
syn_data = []
i = 0
while i < len(C):
    j = 0
    p = []
    while j < len(C[0]):
        p.append(float(C[i][j]))
        j += 1
    syn_data.append(p)
    i += 1
# print(syn_data)
file.close()

# 读取Exc.con 励磁装置 [Generator_number, Type, vrmax最大调节电压 pu, vrmin pu,
# Ka放大器增益 pu, Ta, Kf稳定器增益 pu, Tf, Ke励磁回路积分偏差 pu, Te, Tr测量时间常数,
# Ae, Be, u]
file = open("d_036.txt", "r", encoding='utf-8')
C = []
b = file.readlines()[150:157]
for line in b:
    num = list(line.split())
    C.append(num)
Exc_data = []
i = 0
while i < len(C):
    j = 0
    p = []
    while j < len(C[0]):
        p.append(float(C[i][j]))
        j += 1
    Exc_data.append(p)
    i += 1
# print(Exc_data)
file.close()

# 读取Tg.con  涡轮调速器【编号、类型、参考速度p.u、下垂p.u、最大涡轮功率p.u、
# 最小涡轮功率p.u、调速器时间常数s、私服时间常数、瞬态增益时间常数、功率分数时间常数、
# 连接状态】
file = open("d_036.txt", "r", encoding='utf-8')
C = []
b = file.readlines()[160:166]
for line in b:
    num = list(line.split())
    C.append(num)
Tg_data = []
i = 0
while i < len(C):
    j = 0
    p = []
    while j < len(C[0]):
        p.append(float(C[i][j]))
        j += 1
    Tg_data.append(p)
    i += 1
# print(Tg_data)
file.close()

# 读取Tcsc.con  静止串联补偿器【Line number、Model type、操作模式、调度策略、额定功率、
# 额定电压、额定频率、串联补偿百分比、调节器时间常数、最大电抗（发射角）、
# 最小电抗（发射角）、PI控制器的比例增益 pu、PI控制器积分增益 pu、感性电抗 pu、
# 容性电抗 pu、稳定信号的增益 pu、连接状态】
file = open("d_036.txt", "r", encoding='utf-8')
C = []
b = file.readlines()[168:169]
for line in b:
    num = list(line.split())
    C.append(num)
Tcsc_data = []
i = 0
while i < len(C):
    j = 0
    p = []
    while j < len(C[0]):
        p.append(float(C[i][j]))
        j += 1
    Tcsc_data.append(p)
    i += 1
# print(Tcsc_data)
file.close()

# 读取Fault.con故障数据[Bus, Sn, Vn, fn, tf故障时间, tc清除时间, rf pu, xf pu]
file = open("d_036.txt", "r", encoding='utf-8')
C = []
b = file.readlines()[173:174]
for line in b:
    num = list(line.split())
    C.append(num)
Fault_data = []
i = 0
while i < len(C):
    j = 0
    p = []
    while j < len(C[0]):
        p.append(float(C[i][j]))
        j += 1
    Fault_data.append(p)
    i += 1
# print(Fault_data)
file.close()

# 读取Breaker.con断路器数据[Line, Bus, Sn, Vn, fn, 连接状态, t1第一次干预时间,
# t2第二次干预时间, u1进行第一次干预, u2进行第二次干预]
file = open("d_036.txt", "r", encoding='utf-8')
C = []
b = file.readlines()[178:179]
for line in b:
    num = list(line.split())
    C.append(num)
Breaker_data = []
i = 0
while i < len(C):
    j = 0
    p = []
    while j < len(C[0]):
        p.append(float(C[i][j]))
        j += 1
    Breaker_data.append(p)
    i += 1
# print(Breaker_data)
file.close()

# 读取Pss.con电力系统稳定器
file = open("d_036.txt", "r", encoding='utf-8')
C = []
b = file.readlines()[182:186]
for line in b:
    num = list(line.split())
    C.append(num)
Pss_data = []
i = 0
while i < len(C):
    j = 0
    p = []
    while j < len(C[0]):
        p.append(float(C[i][j]))
        j += 1
    Pss_data.append(p)
    i += 1
# print(Pss_data)
file.close()

# 原始数据处理成方便后面模块使用的格式
# -----------------------------------分割线------------------------------------------
linenumber = np.zeros((2, len(line_data)), dtype=int)
linerxb = np.zeros((3, len(line_data)))
for columnindex in range(len(line_data)):
    linenumber[0][columnindex] = int(line_data[columnindex][0])
    linenumber[1][columnindex] = int(line_data[columnindex][1])
    linerxb[0][columnindex] = line_data[columnindex][7]
    linerxb[1][columnindex] = line_data[columnindex][8]
    linerxb[2][columnindex] = line_data[columnindex][9]
LineData = linenumber.tolist() + linerxb.tolist()

shuntnumber = np.zeros(len(Shunt_data), dtype=int)
shuntgb = np.zeros((2, len(Shunt_data)), dtype=float)
for columnindex in range(len(Shunt_data)):
    shuntnumber[columnindex] = int(Shunt_data[columnindex][0])
    shuntgb[0][columnindex] = Shunt_data[columnindex][4]
    shuntgb[1][columnindex] = Shunt_data[columnindex][5]
ShuntData = [shuntnumber.tolist()] + shuntgb.tolist()

# 发电机机端节点和内节点的信息矩阵
generatornumber = np.zeros((2, len(syn_data)), dtype=int)
generatordata = np.zeros((6, len(syn_data)))
for columnindex in range(len(syn_data)):
    generatornumber[0][columnindex] = int(syn_data[columnindex][0])
    generatornumber[1][columnindex] = int(syn_data[columnindex][0]) + 36
    generatordata[0][columnindex] = syn_data[columnindex][8]  # Xd'
    generatordata[1][columnindex] = syn_data[columnindex][17]  # M = 2H = TJ
    # 要获得发电机连接的节点（母线）编号, 把机端功率和发电机对应起来
    for row in chaoliu:
        for columnindex in range(len(generatornumber[0])):
            if row[0] == generatornumber[0][columnindex]:
                generatordata[2][columnindex] = row[3]  # Pg
                generatordata[3][columnindex] = row[4]  # Qg
                generatordata[4][columnindex] = row[1]  # V
                generatordata[5][columnindex] = math.radians(row[2])  # theta 转成弧度，原来是角度
                break
    # 生成发电机内节点的信息矩阵【编号, Pm, E, delta】
enumber = generatornumber.copy()
edata = np.zeros((3, len(syn_data)))
for columnindex in range(len(syn_data)):
    Current = ((generatordata[2][columnindex] + 1j * generatordata[3][columnindex]) / (
            generatordata[4][columnindex] * math.cos(generatordata[5][columnindex]) + 1j * generatordata[4][
        columnindex] * math.sin(
        generatordata[5][columnindex]))).conjugate()
    E = generatordata[4][columnindex] * math.cos(generatordata[5][columnindex]) + 1j * generatordata[4][
        columnindex] * math.sin(
        generatordata[5][columnindex]) + 1j * generatordata[0][columnindex] * Current
    # E 是复数, Current = (Pg + jQg / Vg(complex)).conjugate
    edata[0][columnindex] = abs(E)  # E 的幅值
    edata[1][columnindex] = arg(E)  # E 的相角delta, 弧度制
    Pm = (E * (Current.conjugate())).real
    edata[2][columnindex] = Pm
EData = enumber.tolist() + edata.tolist()
GeneratorData = generatornumber.tolist() + generatordata.tolist()

# 负荷信息计算, 所有负荷都采用恒阻抗模型
loadnumber = np.zeros(len(PQ_data), dtype=int)
loaddata = np.zeros((2, len(PQ_data)))
for columnindex in range(len(PQ_data)):
    loadnumber[columnindex] = PQ_data[columnindex][0]
    for i in range(len(chaoliu)):
        if loadnumber[columnindex] == chaoliu[i][0]:
            V = chaoliu[i][1] * math.cos(np.radians(chaoliu[i][2])) + 1j * chaoliu[i][1] * math.sin(
                np.radians(chaoliu[i][2]))
            Current = ((chaoliu[i][5] + 1j * chaoliu[i][6]) / V).conjugate()
            Z = V / Current
            # print('current', columnindex, '  ', Current)
            break
    loaddata[0][columnindex] = Z.real
    loaddata[1][columnindex] = Z.imag
LoadData = [loadnumber.tolist()] + loaddata.tolist()

def getlinedata():
    return LineData


def getnumberofbus():
    numberofbus = 0
    for item in BUS_data:
        numberofbus += 1
    return numberofbus


def getshuntdata():
    return ShuntData


def getedata():
    return EData


def getgeneratordata():
    return GeneratorData

def getloaddata():
    return LoadData


if __name__ == '__main__':
    print(linenumber)
    print(linerxb)
    print('Shunt_data: ', Shunt_data)
    print(shuntnumber)
    print(shuntgb)
    print('chaoliu: ', chaoliu)
    print('EData:', EData)
    print('LoadData: ', LoadData)
    print('ShuntData: ', ShuntData)
    print('LineData: ', LineData)
    print('GeneratorData: ', GeneratorData)