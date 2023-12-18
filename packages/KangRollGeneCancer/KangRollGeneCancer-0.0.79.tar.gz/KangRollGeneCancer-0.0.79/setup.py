# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

# setup(
#     name="KangRollGeneCancer",
#     version="0.0.70",
#     author="Xiaowen kang",
#     description="xiaowenseekjob@gmail.com A brief description of Kang Roll package",
#     packages=find_packages(),
#     install_requires=[
#         # 依赖项列表，例如 'numpy>=1.18.5'
#     ],
# )


from setuptools import setup, find_packages

setup(
    name="KangRollGeneCancer",
    version="0.0.79",
    author="Xiaowen kang",
    description="xiaowenseekjob@gmail.com A brief description of Kang Roll package",
    packages=find_packages(),
    package_data={
        'KangRollGeneCancer': ['release/*']
    },
    install_requires=[
        # 依赖项列表，例如 'numpy>=1.18.5'
    ],
)


