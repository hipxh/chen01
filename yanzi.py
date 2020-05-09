file=open('公共行政学'+'.txt')
keys=[]
mymap = {}
for line in file.readlines():
    keys.append(line.strip())


for key in keys:
    username=key.split("\t")[0]
    password=key.split("\t")[1]
    mymap[username] = password
# print(mymap)


keys.clear()
file=open('13'+'.txt')
for line in file.readlines():
    keys.append(line.strip())
for key in keys:
    if key in mymap.keys():
        print(mymap[key])
    else:
        print("")
