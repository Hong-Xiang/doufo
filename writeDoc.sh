# use pdoc to automatically generate documents of this modules after installation
# install pdoc first
# $ pip install pdoc
pdoc --html --html-dir doc/documentations --overwrite doufo 
# generate tree 
tree -P "*.py" src -o doc/tree.txt