import numpy as np

def update_network(u, tau, B):
    """更新网络状态"""
    return u + tau * (B - u)



