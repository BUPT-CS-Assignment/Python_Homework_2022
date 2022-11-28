def get_input():
    a,b = input().split()
    return list(str(int(a))),list(str(int(b)))

if __name__ == '__main__':
    a,b = get_input()
    if len(a) < len(b):
        for i in range(0,len(a)):
            b.insert(2*i,a[i])
        print("".join(b))
    else:
        for i in range(0,len(b)):
            a.insert(2*i+1,b[i])
        print("".join(a))
    