# webCode
This repository contains a few miscellaneous projects related to making things displayable on the web (e.g., as an HTML snippet). 

## [tex2svg](/tex2svg.sh)
Bash code for converting a LaTex equation to an `svg`. Code from the `amssymb` and `amsmath` packages are allowed. This requires the following bash commands: 
`pdflatex`, `pdfcrop`, and `pdf2svg`. 

The packages can be installed with the following `apt` command (or similar depending on your OS):
```sh
# TeX Live is a popular (La)TeX distribution;
#   should include pdflatex and pdfcrop and needed packages
sudo apt-get install texlive-latex-base 
sudo apt-get install pdf2svg
```

The command syntax is as follows:
```
tex2svg.sh out eq
  out: file for output
  eq:  text of equation (e.g., "\hat{H}\left|\psi\right>=E\left|\psi\right>")
```

## [codeToHTML](/codeToHTML)
This folder contains (Python) code for taking a string containing code and adding HTML markup that can be further formatted. 
For examples of `css` formatting, see the [codeCSS](/codeToHTML/codeCSS) folder.

### Example
Working in `/codeToHTML` folder:
```py
from pyToHTML import pyToHTML # import function that converts python to html

with open('pyToHTML.py', 'r') as read:
    code = read.read() # read-in pyToHTML.py code
    
html = pyToHTML(code, lineNums=True) # generate HTML code with line numbers
print(html)
```
This will print HTML to terminal with the code used to convert python code to HTML.
