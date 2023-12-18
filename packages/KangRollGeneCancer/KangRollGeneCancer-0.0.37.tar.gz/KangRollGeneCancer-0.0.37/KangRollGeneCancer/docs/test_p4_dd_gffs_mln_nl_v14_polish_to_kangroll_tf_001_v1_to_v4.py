import numpy as np
import matplotlib.pyplot as plt

def kangroll_tf_001_v1_to_v4(v1, v2, mln_iterations=100):
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
        u1_values = layer_one(1, tau1, B1, iterations)
        u2_values = layer_two(u1_values[-1], tau2, B2, iterations)
        return u1_values + u2_values

    # 模拟多层网络动态
    MLN_output_V3 = V3_simulate_MLN(H3_after_genamonic_tf, mln_iterations)

    # 计算新生负荷
    NL_final_V4 = MLN_output_V3[-1]

    return MLN_output_V3, NL_final_V4

# 示例调用
v1_example = 0.9
v2_example = np.array([0, 1, 1, 0] + [0]*12 + [v1_example])
MLN_output, NL_final = kangroll_tf_001_v1_to_v4(v1_example, v2_example, mln_iterations=100)

# 可选：显示图像
plt.figure(figsize=(10, 5))
plt.plot(MLN_output, label='MLN_output')
plt.title('Time series of the two-layer network')
plt.xlabel('Month')
plt.ylabel('Value')
plt.legend()
plt.grid(True)
# plt.show()


# 显示图像，但不阻塞后续代码的执行
plt.show(block=False)

# 图像显示2秒后自动关闭
plt.pause(2)
plt.close()

