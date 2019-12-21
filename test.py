from sympy import *
import numpy as np

x = symbols('x')
sinx = 0
'''
for i in range(4):
    sinxunit = (-1) ** (i) * x ** (2 * i + 1) / factorial(2 * i + 1)
    sinx += sinxunit
print(sinx)
print(solve(Eq(x + sinx, 0), x))

a = [1, 1, 1.0]
print(type(a))
print(type(a[0]))
print(type(a[2]))
'''

print(complex(1, 1), arg(1+1j))
print(arg(1+2j))
a = np.zeros((3, 4))
print(len(a))

c = 3
b = np.arange(1, 26).reshape((5,5))

A = ((b[:len(b)-c]).transpose()[:len(b)-c]).transpose().copy()
B = ((b[:len(b)-c]).transpose()[-c:]).transpose().copy()
D = ((b[-c:].transpose())[-c:]).transpose().copy()


print(b)
print(A)
print(B)
print(D)
print(np.linalg.inv(A))

'''
def y_alter(ymatrix, load, generator, fault):
    
    设原系统有（n+N）条母线（节点）, n个发电机端节点, 则本函数生成的 Altered_Y 应该是2n+N 阶方阵
    :param ymatrix: 初始节点导纳矩阵, (n+N) * (n+N) array
    :param load: LoadData, 3*k list, 编号, r, x
    :param generator: 发电机信息矩阵, 8*n list, 机端节点编号, 发电机内节点编号, Xd', M, Pg, Qg, V, theta, 有用的只有generator[0], [1], [2]
    :param fault: 故障信息矩阵, 1*4 list, 起始线端int, 终止线端int, 故障位置int(0-100), 接地阻抗实部 R_Δ, 接地阻抗虚部 X_Δ, 故障线路（双回）的r, x, b
    
    yaltered = ymatrix[:]
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
    # 故障等效的等值阻抗对节点导纳矩阵的影响
    # 检查故障矩阵的前两元素是否为某条支路的两端，否则为数据输入错误
    for i in range(len(LineData)):
        if ((LineData[0][i] - fault[0]) < 0.1) and ((LineData[1][i] - fault[1]) < 0.1):
            if fault[2] == 0:  # 故障发生在线路首端, 不需要增阶, 对首端节点的自导纳进行修正
                yaltered[fault[0] - 1][fault[0] - 1] += 1 / complex(fault[3], fault[4])
            elif fault[2] == 100:  # 故障发生在线路末端, 不需要增阶，对末端节点的自导纳进行修正
                yaltered[fault[1] - 1][fault[1] - 1] += 1 / complex(fault[3], fault[4])
            else:  # 故障发生在线路中间，不新增节点，而是采用星网变换，等效成同时发生在两端的两个短路
                # 先把原来双回线中的一回的影响消除掉
                # 自导纳
                yaltered[fault[0] - 1][fault[0] - 1] += -1 / (2 * complex(LineData[2][i], LineData[3][i]))
                yaltered[fault[1] - 1][fault[1] - 1] += -1 / (2 * complex(LineData[2][i], LineData[3][i]))  # *2是因为认为双回线
                # 互导纳
                yaltered[fault[0] - 1][fault[1] - 1] += 1 / (2 * complex(LineData[2][i], LineData[3][i]))
                yaltered[fault[1] - 1][fault[0] - 1] += 1 / (2 * complex(LineData[2][i], LineData[3][i]))
                # 星网变换中的值的求解
                zone = fault[2] / 100 * 2 * complex(LineData[2][i], LineData[3][i])
                ztwo = (1 - fault[2] / 100) * 2 * complex(LineData[2][i], LineData[3][i])
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


    return yaltered
'''


class Generator(object):
    def __init__(self, number, e, pm, m):
        self.E = e
        self.Pmi = pm
        self.num = number
        self.Mi = m

G = Generator(1,2,3,4)
print(G.E)