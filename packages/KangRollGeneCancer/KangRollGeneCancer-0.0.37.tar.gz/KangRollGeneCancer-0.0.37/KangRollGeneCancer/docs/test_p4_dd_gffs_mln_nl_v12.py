import numpy as np

import matplotlib.pyplot as plt


def print_colored(text, color_code):
    print(f"\033[{color_code}m{text}\033[0m")
def print_yellow(text):
    print_colored(text, "93")

# 使用简化的函数
# print_yellow(" --- Debug： KangFocus--> ")



# 1. 定义基因损伤和基因功能特征谱的初始参数
v1 = 0.9  # DNA损伤
print ('\n ------V1 :  V1 =',v1)
v2 = np.array([0, 1, 1, 0] + [0]*12 + [v1])  # V2: 基因功能特征谱 (GFFS)

print ('\n ------bar V2 :  V2 =[v2 ，，，， v1]: \n',v2)

# 打印基因功能特征谱
print("Gene Functional Feature Spectrum V2 (v2):")
print(v2)
print("------")

# 2. 初始化权重矩阵 W 用于将 GFFS 映射到调整因子
# W_v3= np.zeros((4, 17))  # W_V3 调整因子
# # W_v3[2, 2] = W_v3[0, 0] = -1
# W_v3[0,16] = v2[0]
# W_v3[2,16] = v2[1]

print('----------------17 维度 W Setting---------')

# 定义基因损伤和基因功能特征谱的初始参数
v1 = 0.9  # DNA损伤
print('\n ------V1 :  V1 =', v1)

# 基因功能特征谱 (GFFS)
v2 = np.array([0, 1, 1, 0] + [0]*12 + [v1]) 
print('\n ------bar V2 :  V2 =[v2 ，，，， v1]: \n', v2)
print('v2[0] = ',v2[0] )
print('v2[1] = ',v2[1] )
print('v2[2] = ',v2[2] )
# 初始化17维的权重矩阵 W，用于映射 GFFS 到调整因子
W_v3 = np.zeros((4, 17))  # 初始化为全零矩阵
# 设置W矩阵的特定元素以纳入调控信息
# 假设V2的前两位分别对应W矩阵的第1行和第3行
W_v3[0, 16] = -1 * v2[0]  # V2的第1位控制W的第1行
W_v3[2, 16] = -1 * v2[1]  # V2的第2位控制W的第3行
# 打印权重矩阵 W
print("Weight Matrix W (W_v3):")
print(W_v3)

print('----------------17 维度 W Setting-- DONE-------')
# 打印权重矩阵 W
print("Weight Matrix W (W_v3):")
print(W_v3)
print("------")
# 3. 定义计算调整因子 Delta 的函数
def V3_compute_delta(W, V2):
    return W @ V2

# 4. 定义调整和谐集合 H3 的函数
def V3_adjust_H3(H3, delta):
    w = 1  # 内部权重
    return H3 + w * delta * H3

# 5. 定义初始和谐集合 H
H3_ini = np.array([0.1, 10, 0.8, 0])
print("-----V1: Initial Harmonic Set H (H3_ini):")
print(H3_ini)
print("------")

# 6. 计算调整因子 Delta
print("-----V3.1: Computed Adjustment Factor Delta (delta_v3):")
print('W_v3 =', W_v3)
print('v2 =', v2)


# print ('w——v3:' W_v3)
# print('V2:'v2)
delta_v3 = V3_compute_delta(W_v3, v2)
print("----V3.1: Computed Adjustment Factor Delta (delta_v3): delta_v3 = W @ V2")
print(delta_v3)
print("------")


# # 使用简化的函数
# print_yellow(" --- Debug： KangFocus--> ")

# 7. 使用计算出的 Delta 调整和谐集合
print("-----V3.2: Before (V3_adjust_H3---Genamonic Transfor):")
print('H3 (H3_ini) =', H3_ini)
print('delta_v3 =', delta_v3)


# 使用简化的函数
print_yellow(" --- Debug： KangFocus--> ")

H3_after_genamonic_tf = V3_adjust_H3(H3_ini, delta_v3)
print("-----V3.2: Harmonic Set H3 adjusted with Delta (V3_adjust_H3----Genamonic Transfor):")
print('- MARK HERE !!!!-- H3_after_genamonic_tf =', H3_after_genamonic_tf)
print("------")

H3_v3 = H3_after_genamonic_tf  # H3_v3 用于 v3.

print('---------Prepare for H3_v3 -------:\n')
print('-- H3_v3 =', H3_v3)



# 8. 定义两层网络的第一层和第二层的迭代函数
# def layer_one(u1, tau1, B1, n_iterations):
#     for _ in range(n_iterations):
#         u1 = u1 + tau1 * (B1 - u1)
#     return u1

# def layer_two(u2, tau2, B2, n_iterations):
#     for _ in range(n_iterations):
#         u2 = u2 + tau2 * (B2 - u2)
#     return u2

# 修改后的第一层网络的迭代函数
def layer_one(u1, tau1, B1, n_iterations):
    u1_values = []  # 用于存储每次迭代的结果
    for _ in range(n_iterations):
        u1 = u1 + tau1 * (B1 - u1)
        u1_values.append(u1)  # 将每次迭代的结果添加到列表中
    return u1_values

# 修改后的第二层网络的迭代函数
def layer_two(u2, tau2, B2, n_iterations):
    u2_values = []  # 用于存储每次迭代的结果
    for _ in range(n_iterations):
        u2 = u2 + tau2 * (B2 - u2)
        u2_values.append(u2)  # 将每次迭代的结果添加到列表中
    return u2_values

# 9. 定义计算新生负荷 (Neoplastic Load) 的函数
def V4_calculate_NL(MLN_output):
    return MLN_output[-1]

# 10. 打印详细信息的函数
def print_details_V5(iteration, H_input, delta, H_adjusted, MLN_output=None, NL=None):
    print(f"迭代 {iteration}:")
    print(f"输入 Harmonic Set H: {H_input}, Delta: {delta}, 调整后 Harmonic Set H: {H_adjusted}")
    if MLN_output is not None and NL is not None:
        print(f"MLN输出: {MLN_output}, Neoplastic Load: {NL}")
    print("------")

# 11. 集成双层网络模拟到主循环中
def V3_simulate_MLN(H3, iterations=10):
    u1 = 1
    tau1 = H3[0]
    B1 = H3[1]
    tau2 = H3[2]
    B2 = H3[3]

    # u1_final = layer_one(u1, tau1, B1, iterations)
    # u2_final = layer_two(u1_final, tau2, B2, iterations)



    # 第一层迭代
    u1_values = layer_one(u1, tau1, B1, iterations)

    print('-----V3_simulate_MLN----------:  \n  tau2  = ', tau2)

    # 第二层迭代，使用第一层的最终结果作为起始值
    u2_values = layer_two(u1_values[-1], tau2, B2, iterations)

    # u_mln = u_mln.append(u2_values)


    u_mln = list(u1_values)  # 创建u1_values的副本，以避免修改原始列表
    u_mln.extend(u2_values)


    # 打印结果
    print(f"tau1: {tau1}, B1: {B1}, tau2: {tau2}, B2: {B2}")
    print("u1 values over iterations: ", u1_values)
    print("u2 values over iterations: ", u2_values )


    # 打印参数
    print(f"tau1: {tau1}, B1: {B1}, tau2: {tau2}, B2: {B2}")


    return u_mln   #np.array([u1_values, u2_values])

# 12. 模拟多层网络动态
for iteration in range(1):
    print_details_V5(iteration + 1, H3_v3, delta_v3, H3_v3)
    MLN_output_V3 = V3_simulate_MLN(H3_v3)

    print('-----------------------do V4 - NL ---------------------\n')
    NL_final_V4 = V4_calculate_NL(MLN_output_V3)
    print_details_V5(iteration + 1, H3_v3, delta_v3, H3_v3, MLN_output_V3, NL_final_V4)

print("Final Neoplastic Load after 3 Iterations:", NL_final_V4)






# Plot the time series for v3
plt.figure(figsize=(10, 5))
plt.plot(MLN_output_V3, label='MLN_output_V3')
plt.plot(NL_final_V4, label='NL_final_V4')
# plt.plot(u_values, label='u values')
plt.title('Time series of the two-layer network (v3)')
plt.xlabel('month')
plt.ylabel('Value')
plt.legend()
plt.grid(True)
# plt.show()


# 显示图像，但不阻塞后续代码的执行
plt.show(block=False)

# 图像显示2秒后自动关闭
plt.pause(0.5)
plt.close()

