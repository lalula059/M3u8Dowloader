import os
import subprocess
import shutil
import re
from sjz42_url.data_save.data_sort import Data_Sort
cou = 0
config = 'E:\\video'
curdir = 'E:\\video\\脚本写入路径'
def sort(file):
    try:
        data_empty = list()
        print(Data_Sort.data_sort.get(cou))
        for item in Data_Sort.data_sort.get(cou):
            pattern = '(\w+\.ts)'
            patt = re.compile(pattern)
            text = re.findall(patt,item)[0]
            data_empty.append(text)
        return data_empty
    except Exception as e:
        return file

def merge():
    global cou
    global config
    global curdir
    config = 'E:\\video'
    
    curdir = os.path.abspath(config+'\\脚本写入路径')
    def outp(doc):
        global cou
        count = 0
        for j in range(1,len(doc)):
            count +=1
            cou =count
            file = config+'\\'+str(j)
            t_file = os.listdir(file)
            print(t_file)
            after = sort(t_file)
            save_file = curdir+'\\'+str(count)+'.txt'
            with open(save_file,'w') as f:
                for i in after:
                    f.write(f"file '{config}\\{str(j)}\\{i}'\n")
    outp(os.listdir(config))
    mer()
    delete()
def mer():
    global cou
    for i in range(1,cou+1):
        comman1 = f'ffmpeg -f concat -safe 0 -i E:\\video\\脚本写入路径\\{i}.txt -c copy E:\\video\\脚本写入路径\\output{i}.mp4'
        subprocess.run(comman1, shell=True)
def delete():
    for i in range(1,cou+1):
        os.remove(curdir+f'\\{i}.txt'.format(i=i))
        shutil.rmtree(config+f'\\{i}')
