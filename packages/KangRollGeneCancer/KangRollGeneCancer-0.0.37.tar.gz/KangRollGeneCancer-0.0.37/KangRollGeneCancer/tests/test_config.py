# test_config.py

import unittest
import sys


import os
sys.path.append(os.path.abspath('..'))
print(sys.path)

# from config import IS_PRODUCTION, PRODUCTION_KEY
# test_config.py
# from KangRollGeneCancer.config import IS_PRODUCTION, PRODUCTION_KEY
# 测试代码...

# 如果在包外：也是可以的，主要添加所搜路径可以搜索到即可。 
from config import IS_PRODUCTION, PRODUCTION_KEY
# from KangRollGeneCancer.config import IS_PRODUCTION, PRODUCTION_KEY
# 如果在包内：  证明可行。 welldone. (config in the KangRollGeneCancer 发布包内)
# from KangRollGeneCancer.config import IS_PRODUCTION, PRODUCTION_KEY



# from config import IS_PRODUCTION, PRODUCTION_KEY
# 接下来是您的测试代码...



class TestConfig(unittest.TestCase):
    def test_is_production(self):
        # 测试 IS_PRODUCTION 标志
        # self.assertFalse(IS_PRODUCTION)  # 假设您当前处于开发环境
        self.assertTrue(IS_PRODUCTION)  # 假设您当前处于产品环境

    def test_production_key(self):
        # 测试生产环境密钥
        self.assertEqual(PRODUCTION_KEY, "KangRoll2023_key")  # 替换为您的实际密钥

if __name__ == '__main__':
    unittest.main()
