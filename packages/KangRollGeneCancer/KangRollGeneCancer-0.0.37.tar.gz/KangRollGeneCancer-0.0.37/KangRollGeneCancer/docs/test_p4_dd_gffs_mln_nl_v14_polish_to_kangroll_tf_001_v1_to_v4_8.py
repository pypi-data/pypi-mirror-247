import numpy as np
import matplotlib.pyplot as plt
import random

# 定义函数
def kangroll_tf_001_v1_to_v4(v1, v2, u_ini, H3_ini, lay1_iterations, lay2_iterations, mln_iterations=100, debug_mode=False, test_random=True):
    

    if test_random:
        # 随机调整 tau1 值和第一层迭代次数
        H3_ini[0] = random.uniform(0.001, 0.005)
        lay1_iterations = random.randint(100, 500)


    # 初始化17维的权重矩阵 W
    W_v3 = np.zeros((4, 17))
    W_v3[0, 16] = -1 * v2[0]  # 第1位控制W的第1行
    W_v3[2, 16] = -1 * v2[1]  # 第2位控制W的第3行

    # 计算调整因子 Delta
    delta_v3 = W_v3 @ v2

    # 调整和谐集合 H3
    H3_after_genamonic_tf = H3_ini + delta_v3 * H3_ini


    if debug_mode:
        print("Debug Information:")
        print("V1:", v1)
        print("V2:", v2)
        print("W:", W_v3)
        print("Delta:", delta_v3)
        print("H3:", H3_after_genamonic_tf)

    # 定义两层网络的迭代函数
    def layer_one(u1, tau1, B1, iterations):
        u1_values = []
        for _ in range(iterations):
            u1 = u1 + tau1 * (B1 - u1)
            u1_values.append(u1)
        return u1_values

    def layer_two(u2, tau2, B2, iterations):
        u2_values = []
        for _ in range(iterations):
            u2 = u2 + tau2 * (B2 - u2)
            u2_values.append(u2)
        return u2_values

    # 集成双层网络模拟到主循环
    def V3_simulate_MLN(H3, u_ini):
        tau1, B1, tau2, B2 = H3
        u1_values = layer_one(u_ini, tau1, B1, lay1_iterations)
        u2_values = layer_two(u1_values[-1], tau2, B2, lay2_iterations)
        return u1_values + u2_values

    # 模拟多层网络动态
    MLN_output_V3 = V3_simulate_MLN(H3_after_genamonic_tf, u_ini)

    # 计算新生负荷
    NL_final_V4 = MLN_output_V3[-1]

    if debug_mode:
        print("V3:", MLN_output_V3)
        print("NL final V4:", NL_final_V4)

    return MLN_output_V3, NL_final_V4

# 设置相同的随机数生成种子
random.seed(42)

# 图像设置为一列三行
# fig, axs = plt.subplots(3, 1, figsize=(10, 15))
# 图像设置为一列三行，但尺寸更小
fig, axs = plt.subplots(3, 1, figsize=(6, 8))  # 尺寸调整为8x12

# 损伤值的列表
v1_values = [0.1, 0.3, 0.5]

# 颜色列表，用于区分不同的损伤值
colors = ['blue', 'green', 'red']

# 对每个损伤值进行模拟
for index, v1_test in enumerate(v1_values):
    v2_test = np.array([0, 1, 1, 0] + [0]*12 + [v1_test])   # TP 53的基因功能特征谱
    u_ini_test = 0   # 双层网络的初始值
    H3_ini_test = np.array([0.001, 1, 0.005, 0]) # 和谐集合H的初始值
    lay1_iterations_test = random.randint(100, 500) # 第一层迭代次数
    lay2_iterations_test = 500 # 第二层迭代次数

    # 总的MLN_output存储变量
    total_MLN_output = []

    # 进行三十次循环迭代
    for i in range(30):
        # 调用函数
        MLN_output, NL_final = kangroll_tf_001_v1_to_v4(v1_test, v2_test, u_ini_test, H3_ini_test, lay1_iterations_test, lay2_iterations_test, mln_iterations=100, debug_mode=False, test_random=True)

        # 更新u_ini_test为MLN_output的最后一个值
        u_ini_test = MLN_output[-1]

        # 将MLN_output加入总的MLN_output
        total_MLN_output.extend(MLN_output)

    # 绘制每个损伤值的图像
    axs[index].plot(total_MLN_output, label=f'TP53 Damage: {v1_test}', color=colors[index])
    axs[index].set_title(f'TP53 Damage: {v1_test}')
    axs[index].set_xlabel('Hours')
    axs[index].set_ylabel('Value')
    axs[index].legend()
    axs[index].grid(True)



# ...（其余代码不变）...

# # 显示整个图像
# plt.tight_layout()
# plt.show()




# 显示整个图像
plt.tight_layout()
# plt.show()


# 显示图像，但不阻塞后续代码的执行
plt.show(block=False)

# 图像显示5秒后自动关闭
plt.pause(100)
plt.close()
