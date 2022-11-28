f = open('temp.txt',mode='w')
f.write(input())
f.close()

try:
    f = open('temp.txt',mode = input())
    f.write(input())
except Exception:
    pass
f.close()

f = open('temp.txt',mode='r')
print(f.read())
f.close()