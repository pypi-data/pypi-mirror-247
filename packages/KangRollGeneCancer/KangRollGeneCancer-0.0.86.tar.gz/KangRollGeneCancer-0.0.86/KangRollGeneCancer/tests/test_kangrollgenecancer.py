import sys
print(sys.path)



import unittest
from KangRollGeneCancer import analyze_gene
from KangRollGeneCancer import analyze_gene


class TestKangRollGeneCancer(unittest.TestCase):

    def test_analyze_gene(self):
        # 假设的测试案例
        gene_sequence = "ATCG"
        expected_result = "某种预期结果"  # 这应该是你期望的结果

        # 调用函数
        result = analyze_gene(gene_sequence)

        # 断言检查结果是否正确
        self.assertEqual(result, expected_result)

if __name__ == '__main__':
    unittest.main()
