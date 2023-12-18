
import sys
sys.path.append('/Users/kang/1.live_wit_GPT4/code_pypi/KangRollGeneCancerWorkspace')

from KangRollGeneCancer.core.config import IS_KANGROLL_PRODUCTION, KANGROLL_PRODUCTION_KEY

# 剩余的代码...


# from KangRollGeneCancer.config import IS_KANGROLL_PRODUCTION, KANGROLL_PRODUCTION_KEY

if IS_KANGROLL_PRODUCTION:
    # 生产环境的逻辑
    print("生产密钥:", KANGROLL_PRODUCTION_KEY)
else:
    # 开发环境的逻辑
    print("开发环境")
