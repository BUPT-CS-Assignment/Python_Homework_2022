key_map={}
for i in range(0,int(input())):
    line = str(input()).split(' ')
    key_map[line[1]]=line[0]

while True:
    msg = input()
    if msg == 'dog':
        break
    print(key_map.get(msg,'dog'))
        