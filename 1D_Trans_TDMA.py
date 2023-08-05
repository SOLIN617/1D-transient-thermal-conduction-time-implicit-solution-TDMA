from matplotlib import pyplot as plt
import numpy as np

#

Den = 100
Cp = 1000
k = 10
s = 0
L = 3
Tl = 3
Th = 5
dt = 1000
tall = 100000
N = 5
dx = L / N
#
t = np.zeros(int(tall // dt))
T = np.zeros((int(tall // dt), N + 2))
ap1 = np.zeros((int(tall // dt), N + 2))
aw1 = np.zeros((int(tall // dt), N + 2))
ae1 = np.zeros((int(tall // dt), N + 2))
ap0 = np.zeros((int(tall // dt), N + 2))
an = np.zeros(N + 2)
bn = np.zeros(N + 2)
cn = np.zeros(N + 2)
dn = np.zeros(N + 2)
pn = np.zeros(N + 2)
qn = np.zeros(N + 2)

T[:, 0] = Tl
T[0, 1:(N+1)] = Tl
T[:, N + 1] = Th

# 创建实时绘制横纵轴变量
time = []
Temp = []
# 创建绘制实时损失的动态窗口
plt.ion()

# 随时间变化
for i in range(1, int(tall // dt)):
    t[i] = i * dt
    x = 1
    aw1[i, x] = k / (dx / 2)
    ae1[i, x] = k / dx
    ap0[i, x] = Den * Cp * dx / dt
    ap1[i, x] = aw1[i, x] + ae1[i, x] + ap0[i, x]

    an[x] = ap1[i, x]
    bn[x] = -aw1[i, x]
    cn[x] = -ae1[i, x]
    dn[x] = aw1[i, x] * T[i, x - 1] + ap0[i, x] * T[i - 1, x] + s
    pn[x] = -cn[x] / an[x]
    qn[x] = dn[x] / an[x]

    for x in range(2, N):
        aw1[i, x] = k / dx
        ae1[i, x] = k / dx
        ap0[i, x] = Den * Cp * dx / dt
        ap1[i, x] = aw1[i, x] + ae1[i, x] + ap0[i, x]

        an[x] = ap1[i, x]
        bn[x] = -aw1[i, x]
        cn[x] = -ae1[i, x]
        dn[x] = ap0[i, x] * T[i - 1, x] + s
        pn[x] = -cn[x] / (an[x]+bn[x]*pn[x-1])
        qn[x] = (dn[x]-bn[x]*qn[x-1]) / (an[x]+bn[x]*pn[x-1])

    x = N
    aw1[i, x] = k / dx
    ae1[i, x] = k / (dx / 2)
    ap0[i, x] = Den * Cp * dx / dt
    ap1[i, x] = aw1[i, x] + ae1[i, x] + ap0[i, x]

    an[x] = ap1[i, x]
    bn[x] = -aw1[i, x]
    cn[x] = -ae1[i, x]
    dn[x] = ae1[i,x] * T[i, x + 1] + ap0[i, x] * T[i - 1, x] + s
    pn[x] = -cn[x] / (an[x] + bn[x] * pn[x - 1])
    qn[x] = (dn[x] - bn[x] * qn[x - 1]) / (an[x] + bn[x] * pn[x - 1])

    T[i, N] = qn[N]
    for y in range(N - 1, 1, -1):
        T[i, y] = pn[y] * T[i, y + 1] + qn[y]
    T[i, 1] = pn[1] * T[i, 2] + qn[1]

    # 画图
    time.append(i * dt)  # 添加t到x轴的数据中
    Temp.append(T[i, 1:(N+1)])  # 添加T到y轴的数据中
    plt.clf()  # 清除之前画的图
    plt.plot(time, Temp)  # 画出当前x列表和y列表中的值的图形
    plt.pause(0.1)  # 暂停一段时间，不然画的太快会卡住显示不出来
    plt.ioff()  # 关闭画图窗口
plt.show()
print(T[i, 1])
