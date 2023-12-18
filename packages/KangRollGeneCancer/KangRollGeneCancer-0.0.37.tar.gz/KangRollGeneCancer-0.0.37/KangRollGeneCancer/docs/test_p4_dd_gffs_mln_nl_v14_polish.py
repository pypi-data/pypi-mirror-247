import numpy as np
import matplotlib.pyplot as plt

def print_colored(text, color_code):
    print(f"\033[{color_code}m{text}\033[0m")

def print_yellow(text):
    print_colored(text, "93")

# 初始化DNA损伤和基因功能特征谱
v1 = 0.9  # DNA损伤
v2 = np.array([0, 1, 1, 0] + [0]*12 + [v1])  # 基因功能特征谱 (GFFS)

# 初始化17维的权重矩阵 W
W_v3 = np.zeros((4, 17))
W_v3[0, 16] = -1 * v2[0]  # 第1位控制W的第1行
W_v3[2, 16] = -1 * v2[1]  # 第2位控制W的第3行

# 计算调整因子 Delta
delta_v3 = W_v3 @ v2

# 初始化和谐集合 H
H3_ini = np.array([0.05, 10, 0.1, 0])

# 调整和谐集合 H3
H3_after_genamonic_tf = H3_ini + delta_v3 * H3_ini

print_yellow("H3_after_genamonic_tf: " + str(H3_after_genamonic_tf))

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
def V3_simulate_MLN(H3, iterations):
    tau1, B1, tau2, B2 = H3
    print_yellow(f"Entering MLN with tau1: {tau1}, B1: {B1}, tau2: {tau2}, B2: {B2}")

    u1_values = layer_one(1, tau1, B1, iterations)
    u2_values = layer_two(u1_values[-1], tau2, B2, iterations)

    print_yellow(f"MLN parameters inside: tau1: {tau1}, B1: {B1}, tau2: {tau2}, B2: {B2}")
    return u1_values + u2_values

# 模拟多层网络动态
MLN_output_V3 = V3_simulate_MLN(H3_after_genamonic_tf, 100)

# 计算新生负荷
NL_final_V4 = MLN_output_V3[-1]
print_yellow("Final Neoplastic Load after 3 Iterations: " + str(NL_final_V4))

# 展示图像
plt.figure(figsize=(10, 5))
plt.plot(MLN_output_V3, label='MLN_output_V3')
plt.title('Time series of the two-layer network (v3)')
plt.xlabel('Month')
plt.ylabel('Value')
plt.legend()
plt.grid(True)
plt.show(block=False)
plt.pause(2)
plt.close()
