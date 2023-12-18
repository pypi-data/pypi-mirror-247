#!/bin/bash



# 自动更新 setup.py 中的版本号。
# 清理旧的构建文件。
# 构建新的发行版并上传到 PyPI。
# 卸载旧版本并安装新版本。



# echo "更新版本号..."
# python3 update_version.py



#!/bin/bash

echo "更新版本号..."
new_version=$(python3 ./kangsmarttools/update_version.py)
update_status=$?

if [ $update_status -ne 0 ]; then
    echo "版本更新失败，脚本终止。"
    exit 1
fi

echo "将更改提交到 Git..."
git add -A
git commit -m "update pypi- $new_version publish -> match with pypi"
git push

# 其余的脚本步骤...



# 其余步骤...
# echo "清理旧的构建文件..."
# # rm -rf build dist
# rm build/* dist/*

echo "清理旧的构建文件..."
[ -d "KangRollGeneCancer.egg-info" ] && rm -rf KangRollGeneCancer.egg-info
[ -d "build" ] && rm -rf build/*
[ -d "dist" ] && rm -rf dist/*


echo "开始构建新版本..."
python setup.py sdist bdist_wheel

echo "上传到 PyPI..."
twine upload dist/*

echo "卸载旧版本..."
pip uninstall -y KangRollGeneCancer

echo "暂停1秒..."
sleep 1

echo "安装新版本..."
pip install KangRollGeneCancer

echo "卸载旧版本..."
pip uninstall -y KangRollGeneCancer

echo "暂停1秒..."
sleep 1

echo "安装新版本..."
pip install KangRollGeneCancer


echo "发布过程完成."

