#coding=utf-8
import os
# A list of useful API

# Make a dir
def mk_dir(path):
    path = path.strip()
    path = path.rstrip("\\")
    is_exist = os.path.exists(path)
    if not is_exist:
        temp_str = path + ' create successfully!'
        print temp_str
        os.makedirs(path)
        return True
    else:
        temp_str = path + ' is already be there!'
        print temp_str
        return False

def get_dir_files(dir,is_contain_dir = False):
    file_list = []
    if os.path.exists(dir):
        dir_file_list = os.listdir(dir);
        for dir_file in dir_file_list:
            if is_contain_dir:    file_list.append(dir + dir_file);
            else:     file_list.append(dir_file);
    return file_list
