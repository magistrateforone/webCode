#!/usr/bin/env bash

# inputs:
#     $1: output svg
#     $2: latex equation
tempdir=$(mktemp -d)
# printf "\\documentclass{article}\\pagestyle{empty}\\\begin{document}\\[%s\\]\\\end{document}" $2 > $tempdir/temp.tex
echo '\documentclass{article}\usepackage{amssymb,amsmath}\pagestyle{empty}\begin{document}\begin{align*}' $2 '\end{align*}\end{document}' > $tempdir/temp.tex
pdflatex -interaction=nonstopmode -output-directory=$tempdir $tempdir/temp.tex 1> /dev/null
pdfcrop $tempdir/temp.pdf $tempdir/temp1.pdf  1> /dev/null
pdf2svg $tempdir/temp1.pdf $1 1> /dev/null
rm -r $tempdir
