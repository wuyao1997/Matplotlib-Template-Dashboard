@echo off
chcp 65001
@echo off
echo 开始执行构建脚本...

echo 执行 ipynb2py.py
python ipynb2py.py

echo 执行 py2image.py
python py2image.py

echo 执行 dir2html.py
python dir2html.py

echo 执行 resource_embedding.py
python resource_embedding.py

echo 构建完成。
