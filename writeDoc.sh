# use pdoc to automatically generate documents of this modules after installation
# install pdoc first
# $ pip install pdoc
pdoc --html --html-dir docs/documentations --overwrite doufo 
# generate tree 
tree -P "*.py" src -o docs/tree.txt