## 查看帮助命令
python3 setup.py --help-commands

## 构建 发布
python setup.py sdist build 

## 上传到 远程 pypitest 库 --verbose：显示详细信息
twine upload dist/* -r pypitest --verbose