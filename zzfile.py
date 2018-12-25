
import os 
from shutil import copyfile

def Test1(rootDir): 
    list_dirs = os.walk(rootDir) 
    for root, dirs, files in list_dirs: 
        # for d in dirs: 
            # print(os.path.join(root, d))      
        for f in files: 
        	if f.find('png') != -1:
        		copyfile(os.path.join(root, f), '/Users/huangtao/Desktop/emoil/more/'+f)
            	# print(os.path.join(root, f))

Test1('/Users/huangtao/Downloads/KeyboardforChat/KeyboardForChat/Assets.xcassets/more')
