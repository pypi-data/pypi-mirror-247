import numpy as np
import pandas as pd

# # 假设的TP53基因功能谱数值
# tp53_ts_values = np.array([
#     [0.8, 0.2, 0,0],  # O: 正常Harmonic Set, 异常Harmonic Set
#     [0.7, 0.3, 0,0],  # M: Harmonic Transform, Kinetic Transform
#     [0.6, 0.4, 0.5],  # V: 结构蛋白, 功能蛋白, RNA
#     [0.9, 0.1, 0.2]   # B: 条件依赖性, 网络互动依赖性, 剂量依赖性
# ])

# # 创建表格
# tp53_ts_df = pd.DataFrame(
#     tp53_ts_values,
#     index=["调控对象 (O)", "调控手段 (M)", "调控载体 (V)", "边界依赖性 (B)"],
#     columns=["组件1", "组件2", "组件3"]
# )

# # 打印整体的数学符号和逻辑
# print("TP53基因功能谱（TS）的数学符号和逻辑:")
# print("TS := { O, M, V, B }")
# print("O: 调控对象, M: 调控手段, V: 调控载体, B: 边界依赖性\n")

# # 打印表格
# print("TP53基因功能谱的数值:")
# print(tp53_ts_df)

# # 简要说明
# print("\n表格说明：")
# print("每行代表基因功能谱的一个组件，每列代表该组件的一个子组件。")
# print("数值表示TP53在不同组件和子组件上的功能或属性的强度。")

import pandas as pd

# 假设的TP53基因功能谱数值
tp53_ts_values = [
    [0.8, 0.2],  # O: 正常Harmonic Set, 异常Harmonic Set
    [0.7, 0.3],  # M: Harmonic Transform, Kinetic Transform
    [0.6, 0.4, 0.5],  # V: 结构蛋白, 功能蛋白, RNA
    [0.9, 0.1, 0.2]   # B: 条件依赖性, 网络互动依赖性, 剂量依赖性
]

# 创建表格
tp53_ts_df = pd.DataFrame(
    tp53_ts_values,
    index=["调控对象 (O)", "调控手段 (M)", "调控载体 (V)", "边界依赖性 (B)"],
    columns=["元素1", "元素2", "元素3"]
)

# 打印整体的数学符号和逻辑
print("TP53基因功能谱（TS）的数学符号和逻辑:")
print("TS := { O, M, V, B }")
print("O: 调控对象, M: 调控手段, V: 调控载体, B: 边界依赖性\n")

# 打印表格
print("TP53基因功能谱的数值:")
print(tp53_ts_df)

# 简要说明
print("\n表格说明：")
print("每行代表基因功能谱的一个组件，每列代表该组件的一个子组件。")
print("数值表示TP53在不同组件和子组件上的功能或属性的强度。")




# 继续之前的程序，增加对每个维度和子集元素的说明

import pandas as pd

# 假设的TP53基因功能谱数值
tp53_ts_values = [
    [0.8, 0.2],  # O: 正常Harmonic Set, 异常Harmonic Set
    [0.7, 0.3],  # M: Harmonic Transform, Kinetic Transform
    [0.6, 0.4, 0.5],  # V: 结构蛋白, 功能蛋白, RNA
    [0.9, 0.1, 0.2]   # B: 条件依赖性, 网络互动依赖性, 剂量依赖性
]

# 创建表格
tp53_ts_df = pd.DataFrame(
    tp53_ts_values,
    index=["调控对象 (O)", "调控手段 (M)", "调控载体 (V)", "边界依赖性 (B)"],
    columns=["元素1", "元素2", "元素3"]
)

# 打印整体的数学符号和逻辑
print("TP53基因功能谱（TS）的数学符号和逻辑:")
print("TS := { O, M, V, B }")
print("O: 调控对象, M: 调控手段, V: 调控载体, B: 边界依赖性\n")

# 打印表格
print("TP53基因功能谱的数值:")
print(tp53_ts_df)

# 简要说明
print("\n表格说明：")
print("每行代表基因功能谱的一个组件，每列代表该组件的一个子组件。")
print("数值表示TP53在不同组件和子组件上的功能或属性的强度。")

# 增加四个维度下的子集元素名称和涵义
print("\n四个维度及其子集元素的名称和涵义：")
print("调控对象 (O):")
print("    正常Harmonic Set (Har_norm): TP53在正常细胞状态下的功能特征。")
print("    异常Harmonic Set (Har_abn): TP53在异常细胞状态下的功能特征。")
print("\n调控手段 (M):")
print("    Harmonic Transform (HarT): TP53通过和谐转换调控细胞过程。")
print("    Kinetic Transform (KT): TP53通过动力学转换调控细胞过程。")
print("\n调控载体 (V):")
print("    结构蛋白 (SP): TP53通过影响细胞结构蛋白来实施调控。")
print("    功能蛋白 (FP): TP53通过影响细胞功能蛋白来实施调控。")
print("    RNA相关调控载体 (RNA): TP53通过RNA相关途径来实施调控。")
print("\n边界依赖性 (B):")
print("    条件依赖性 (CD): TP53的调控效果依赖于特定条件。")
print("    网络互动依赖性 (NID): TP53的调控效果依赖于细胞网络的互动。")
print("    剂量依赖性 (DD): TP53的调控效果依赖于特定剂量。")


#-----------------------------------------------------------------
