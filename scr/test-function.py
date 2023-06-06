import os

with open("test-client.py", 'r') as file:
    k=1
    ls=[]
    s=""
    for line in file:
        if "class" in line:
            project_folder = os.getcwd()
            p = os.path.join(project_folder, line[6:-2])
            os.mkdir(p)
        if "def" in line:
            ls.append(s)
            s=""
        s+=line
    ls.append(s)
    del ls[0]


for k in range(len(ls)):
    with open(f"task{k}.txt", "w") as file_write:
        file_write.write(ls[k])
