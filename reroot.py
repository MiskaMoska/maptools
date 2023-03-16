import os
os.chdir('.')

print("Now you are trying to replace the project root directory")
print("This opreation may be harmful, please be careful!!!")
if os.path.exists('now_root'):
    with open('now_root', 'r') as f:
        old_root = f.read()
else:
    old_root = input("Please input the current project root directory: ")
new_root = input("Please input the new project root directory: ")
new_root = "'"+new_root+"'"
file_list = [
    'maptools/ctg.py',
    'maptools/inferator.py',
    'maptools/map_plotter.py',
    'maptools/noc_mapper.py',
    'maptools/onnx_converter.py',
    'maptools/operator_graph.py',
    'maptools/xbar_mapper.py',
]

def replace(old_str, new_str):
    for file in file_list:
        assert os.path.exists(file), f"No such file: {file}"
        with open(file, "r") as f:  
            data = f.read() 
            str_replace = data.replace(old_str, new_str)
            with open(file, "w") as f:
                f.write(str_replace)
        print(f"replaced one file: {file}")

replace(old_root, new_root)
with open('now_root', 'w') as f:
    f.write(new_root)
