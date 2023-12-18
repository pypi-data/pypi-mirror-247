
import numpy as np

from KangRollGeneCancer.core.config import IS_KANGROLL_PRODUCTION, KANGROLL_PRODUCTION_KEY
# 剩余的代码...
# from KangRollGeneCancer.config import IS_KANGROLL_PRODUCTION, KANGROLL_PRODUCTION_KEY
print('------------------------ env ----------------------------------')
if IS_KANGROLL_PRODUCTION:
    # 生产环境的逻辑

    print("产品环境设置-IS_KANGROLL_PRODUCTION:", IS_KANGROLL_PRODUCTION)
    print("生产密钥:", KANGROLL_PRODUCTION_KEY)
else:
    # 开发环境的逻辑
    print("开发环境")
print('------------------------ env end ----------------------------------\n')


# -----------------------for test
print('------------------------ test : ----------------------------------')

from KangRollGeneCancer.core.multi_layer_network import update_network


import numpy as np
import matplotlib.pyplot as plt


# # 初始化参数
# tau_1, B_1 = 0.1, 10
# tau_2, B_2 = 0.1, 2
# u_1, u_2 = 0, 0  # 初始状态

# # 更新网络状态
# for _ in range(30):  # 假设迭代10次
#     u_1 = update_network(u_1, tau_1, B_1)
#     u_2 = update_network(u_2, tau_2, B_2)

# print("变异程度:", u_1, "修复程度:", u_2)


# 初始化参数
tau_1, B_1 = 0.1, 10
tau_2, B_2 = 0.1, 0
u_1, u_2 = 0, 0  # 初始状态

# 用于存储每次迭代后的状态
u_values = []

# 第一轮迭代（u1）
for _ in range(10):  # 假设迭代10次
    u_1 = update_network(u_1, tau_1, B_1)
    u_values.append(u_1)

# 第二轮迭代（u2），以u1的最终状态作为初始状态
u_2 = u_1
for _ in range(10):  # 再迭代10次
    u_2 = update_network(u_2, tau_2, B_2)
    u_values.append(u_2)


print("变异程度:", u_1, "修复程度:", u_2)
print("u value process:", u_values)


# 可视化过程
plt.plot(u_values)
plt.xlabel('Iteration')
plt.ylabel('u value')
plt.title('Network State Over Iterations')
plt.show()

