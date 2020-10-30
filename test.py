import os

def make_path(path):
    file_list = os.listdir(path)
    path_list = []
    
    for f in file_list:
        path_list.append(os.path.join(path, f))

    return path_list

paths = make_path("C:\\Users\\zmzmd\\Desktop\\test\\Train\\")

for f in paths:
    print(f)