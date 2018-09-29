import os
import sys
from re import match
bad_char = [']', '[', ')', '(', '\'', '\"','=',' ', '\n']

def GetFileList(path = '.', fileList = []):
    for dirpath, dirnames, filenames in os.walk(path):
        for name in filenames:
            # print(os.path.join(dirpath, name))
            if name[:2] == '__':
                continue
            if 'test' in os.path.join(dirpath, name):
                continue
            if name[-2:] == 'py':
                fileList.append(os.path.join(dirpath, name))
    return fileList

def FindModuleLocations(path = '.', modList = dict([])):
    for dirpath, dirnames, filenames in os.walk(path):
        for name in filenames:
            # print(os.path.join(dirpath, name))
            if name[:2] == '__':
                continue
            if 'test' in os.path.join(dirpath, name):
                continue
            if name[-2:] != 'py':
                continue
            filename = os.path.join(dirpath, name)
            f = open(filename, 'r')
            line = f.readline()
            t = 0
            ctn = 0
            while line and t < 20:
                line = line.strip()
                if '__all__' in line:
                    line_new = ''.join(c for c in line if c not in bad_char).replace('__all__', '')
#                     line = f.readline()
#                     while line[:4] == '    ':
#                         line_new = line_new.join(c for c in line if c not in bad_char).replace('__all__', '')
#                         line = f.readline()
#                     print(line_new)
                    keywords = line_new.split(',')
#                     print(keywords)
                    
                    for key in keywords:
#                         print(key)

                        modList[key] = os.path.join(dirpath, name).replace('./src/python/doufo/','')
                    break
                t = t + 1
                line = f.readline()
    return modList

def FindImportList(modList, path = '.', importList = dict([])):
    for dirpath, dirnames, filenames in os.walk(path):
        for name in filenames:
            # print(os.path.join(dirpath, name))
            if name[:2] == '__':
                continue
            if 'test' in os.path.join(dirpath, name):
                continue
            if name[-2:] != 'py':
                continue
            if name[-12:] == 'read_deps.py':
                continue
            if name[:5] == 'setup':
                continue
            filename = os.path.join(dirpath, name)
            filename_alias = filename.replace('./src/python/doufo/','')
            importList[filename_alias] = []
            f = open(filename, 'r')
            lines = f.readlines()

            for line in lines:
                if line[0] == '#':
                    continue
                if 'from doufo import' in line:
                    line = line.replace('from doufo import','')
                    tline = ''.join(c for c in line if c not in bad_char)
                    keys = tline.split(',')
                    for key in keys:
                        if modList[key] not in importList[filename_alias]:
                            importList[filename_alias].append(modList[key])

                if f'from .' in line:
                    tline = line.split(' ')
                    file = os.path.join(dirpath,tline[1]).replace('./src/python/doufo/','')
                    
                    importList[filename_alias].append(file.replace('.', '') + '.py')
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
    # for x in modList:
    #     print(x + ', ' + modList[x])
    importList = FindImportList(modList, '.', {})
    print(importList, './dep.dot')

    # # print(modList)
    # fo = open('deps.dot', 'w+')
    # for file in fileList:
    #     fo.writelines("\"" + file + "\"  [style=filled];\r")
    #     fi = open(file, "r")
    #     for _ in range(20):
    #         text = fi.readline()
    #         if text[:6] != "from .":
    #             continue
    #         sentence = ''
    #         for t in text.split(' '):
    #             if t[0] != '.' and t != 'from' and t != 'import':
    #                 t = t.replace(',','').strip()
    # #                 print(t)
    #                 # try:
    #                 sentence = "\"" + file + "\" -> \"" + modList[t] + "\""
    #                 # except:
    #                     # print(file + '   ' +  t)
    #             # print(sentence)
    #                 fo.writelines(sentence + '\r')

    # print(fileList)
        # for dir, file in zip(dirnames, filenames):
        #     print(os.path.join(dir, file))
        # fileList = ['./' + dir + file for dir, file in zip(dirnames, filenames)]
    # print(fileList)
    # fileList = []
    # fileList = GetFileList(fileList, dirnames, filenames)
    # fi = open('deps.dot', 'a+')
    # print(fileList)
    # for file in fileList:
    #     fi.writelines(file+ "  [style=filled];")
    #     fo = open(file, "r")
    #     for _ in range(20):
    #         text = fo.readline()
    #         if text[:6] != "from .":
    #             continue
    #         sentence = ''
    #         for t in text.split(' '):
    #             if t == 'from' or t == 'import':
    #                 continue
    #             if t[0] == '.':
    #                 t1 = t
    #             sentence = "\"" + file + "\" -> \"" + t1 + "\""
    #         print(sentence)
    #         fi.writelines(sentence)



