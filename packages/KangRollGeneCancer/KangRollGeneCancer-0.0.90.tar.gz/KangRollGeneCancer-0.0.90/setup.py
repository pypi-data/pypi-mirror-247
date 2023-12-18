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
    version="0.0.90",
    author="Xiaowen kang",
    description="xiaowenseekjob@gmail.com A brief description of Kang Roll package",
    packages=find_packages(),
    package_data={
        'KangRollGeneCancer': ['kangroll_000/*','kangrool_000/temp/*']  #,'release/pytransform/*'
    },
    install_requires=[
        # 依赖项列表，例如 'numpy>=1.18.5'
    ],
)




# setup(
#     name='YourPackageName',
#     version='1.0.0',
#     packages=find_packages(),
#     package_data={
#         # 确保包含 _pytransform.dylib 和其他必要的文件
#         '': ['*.dylib', '*.so', '*.dll'],  # 对应 macOS, Linux, Windows
#         'YourPackageName': ['path/to/pytransform/*']
#     },
#     # 其他设置...
# )


