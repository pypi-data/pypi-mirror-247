#!/bin/bash
set -e  # 在命令执行失败时退出

filename=$(basename "$1")
filename="${filename%.*}"

xelatex $filename.tex
# pdflatex $filename.tex

# bibtex $filename.aux

xelatex $filename.tex
xelatex $filename.tex
wait

open $filename.pdf



# #!/bin/bash
# set -e  # 在命令执行失败时退出
# xelatex $1.tex
# wait
# open $1.pdf

