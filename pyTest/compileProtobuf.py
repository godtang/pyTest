# -*- coding: utf-8 -*-

import os

proto = 'D:/CODE/IM_project/im-comm-proto/src/main/resources/protoc.exe'
rootDir = 'D:/CODE/IM_project/im-comm-proto/src/main/resources/message'
outDir = 'D:/CODE/IM_project/im-comm-proto/src/main/resources/python'
for root, dirs, files in os.walk(rootDir):

    # root 表示当前正在访问的文件夹路径
    # dirs 表示该文件夹下的子目录名list
    # files 表示该文件夹下的文件list

    # 遍历文件
    for f in files:
        if '.proto' == f[-6:]:
            fileFullPath = os.path.join(root, f)
            '''fobj = open(fileFullPath,'r+')     #wt：可写入操作方式/at为在原有的文件内容追加写入
            content = fobj.read(1024*1024)
            fobj.seek(0)
            fobj.write('syntax = "proto2";\npackage go_protobuf;\n')    #写函数
            fobj.write(content)
            fobj.close()'''
            commond = str.format('{2} -I{3} --python_out={0} {1}', outDir, fileFullPath, proto, root)
            os.system(commond)

    # 遍历所有的文件夹
    for d in dirs:
        pass
        #print(os.path.join(root, d))


