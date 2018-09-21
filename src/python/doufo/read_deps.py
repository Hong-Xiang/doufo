import os
import sys
from re import match
import re
bad_char = [']', '[', ')', '(', '\'', '\"', '=', ' ', '\n']

MOD_NAME = 'doufo'
FROM_STR = 'from ' + MOD_NAME
FROM_DOT_STR = 'from .'
FROM_MOD_DOT_STR = 'from ' + MOD_NAME + '.'
def GetFileList(path = '.'):
    fileList = []
    dirList = []
    for root, dirs, files in os.walk('.', topdown=True):
        for file in files:
            portion = os.path.splitext(file)
            if 'test' in portion[0] or '__' in portion[0] or portion[0] == 'read_deps':
                continue
            if portion[1] == '.py':
                fileList.append((os.path.join(root, file)).replace(str(os.getcwd), ''))
            else:
                continue
        for dir in dirs:
            if 'test' in dir or '__' in dir:
                continue
            tmp = os.path.join(root, dir)
            if '/.' not in tmp:
                dirList.append(tmp)    
            # print((os.path.join(root, file)).replace(str(os.getcwd), ''))
        
    return fileList, dirList

def FindModuleLocations(path = '.', modList = dict([])):
    files, dirs = GetFileList(path)
    for file in files:
        f = open(file, 'r')
        line = f.readline()
        t = con = cm = 0
        file1 = file.replace('.py', '').replace('.','').replace('/','.')
        file1 = ''.join(word +'.' for word in file1.split('.')[:-1])
        while line and t < 20:
            if line[0] == '\#':
                continue
            if line.strip(' ')[:3] == '\"\"\"':
                if cm == 1:
                    cm = 0
                else:
                    cm = 1
            if cm == 1:
                continue
            line = line.strip()
            if '__all__' in line:
                line_new = ''.join(c for c in line if c not in bad_char).replace('__all__', '')
                keywords = line_new.split(',')
                for key in keywords:
                    if ' ' not in key:
                        modList[MOD_NAME + file1 + key] = [file]
                con = 1
                break
            t = t + 1
            line = f.readline()

        while con == 1:
            if line[:2] == '  ':
                line_new = ''.join(c for c in line if c not in bad_char)
                keywords = line_new.split(',')
                for key in keywords:
                    if ' ' not in key:
                        modList[MOD_NAME + file1 + key] = [file]
                line = f.readline()
            else:
                con = 0
                
    for file in files:
        tfile = file.replace('/', '.').replace('..','.').replace('.py','')
        modList[MOD_NAME + tfile] = []
        for key in modList:
            if '.' + tfile.replace('.','/') + '.py' in modList[key]:
                modList[MOD_NAME + tfile].extend(modList[key])
                
    for dir in dirs:
        tdir = MOD_NAME + dir.replace('/', '.').replace('..','.')
        modList[tdir] = []
        for key in modList:
            if tdir in key and tdir != key:
                modList[tdir].extend(modList[key])
    return modList


def FindImportList(modList, path = '.', importList = dict([])):
    files, _ = GetFileList(path)
    for file in files:
        importList[file] = []
        f = open(file, 'r')
        lines = f.readlines()
        cm = 0
        modprefix = file.split('/')
        modprefix = MOD_NAME + ''.join('.' + word for word in modprefix[1:-1])
        for line in lines:

            if line.strip(' ')[0] == '#':
                continue
            if line.strip(' ')[:3] == '\"\"\"':
                if cm == 1:
                    cm = 0
                else:
                    cm = 1
            if cm == 1:
                continue

            if FROM_STR in line:
                if '*' in line:
                    submod = line.split(' ')[1]
                    for ele in modList[submod]:
                        if ele not in importList[file]:
                            importList[file].append(ele)
                else:
                    submods = re.split(',|\s', line)
                    while '' in submods:
                        submods.remove('')
                    for ele in submods[3:]:
                        for ele in modList[submods[1] + '.' + ele]:
                            if ele not in importList[file]:
                                importList[file].append(ele)

            if FROM_DOT_STR in line:
                tline = line.split(' ')
                tfile = modprefix + tline[1]
                if tfile in modList:
                    for ele in modList[tfile]:
                        if ele not in importList[file]:
                            importList[file].append(ele)                
                else:
                    if tfile[0] not in importList[file]:
                        importList[file].extend(tfile)
#     for key in importList:
#         importList[key] = set(importList[key])
    return importList



def print(importList: dict, filename: str):
    fo = open(filename, "w+")

    fo.writelines("strict digraph \"dependencies\" {\n")
    fo.writelines("ratio = fill;node [style = filled];graph [rankdir = \"LR\",")
    fo.writelines("overlap = \"scale\", size = \"8,10\", ratio = \"fill\", fontsize = \"16\", fontname = \"Helvetica\",")
    fo.writelines("clusterrank = \"local\"];")
    fo.writelines("node [fontsize=7,shape=ellipse];")

    for key in importList:
        sentence = "\"" + str(key) + "\"   [style = filled];\n"
        fo.writelines(sentence)
        for ele in importList[key]:
            # ele = ele.replace('.', '', 2)
            sentence = "\"" + str(key) + "\" -> \"" + str(ele) + "\"\n"
            fo.writelines(sentence)
    fo.writelines("}\n")

    fo.close()

if __name__ == '__main__':
    fileList = GetFileList()
    modList = FindModuleLocations()
    importList = FindImportList(modList, '.', {})
    print(importList, './dep.dot')
