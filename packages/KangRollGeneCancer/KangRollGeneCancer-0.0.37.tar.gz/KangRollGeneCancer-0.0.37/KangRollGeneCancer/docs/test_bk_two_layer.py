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

# 测试函数
u1 = 10
tau1 = H3[0]
B1 = H3[1]
tau2 = H3[2]
B2 = H3[3]  # 假设B2的值，因为它没有被定义
iterations = 10  # 定义迭代次数

# 第一层迭代
u1_values = layer_one(u1, tau1, B1, iterations)

print('-----V3_simulate_MLN----------:  \n  tau2  = ', tau2)

# 第二层迭代，使用第一层的最终结果作为起始值
u2_final = layer_two(u1_values[-1], tau2, B2, iterations)

# 打印结果
print(f"tau1: {tau1}, B1: {B1}, tau2: {tau2}, B2: {B2}")
print("u1 values over iterations: ", u1_values)
print("u2 values over iterations: ", u2_final)
