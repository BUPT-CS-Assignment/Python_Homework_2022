def is_prime(n):
    if n == 1: return False
    if n == 2: return True
    for i in range(2,int(n/2)+1):
        if n % i == 0:
            return False
    return True

if __name__ == "__main__":
    N = int(input())
    arrlist = []
    for i in range(1,N+1):
        if is_prime(i):
            arrlist.append(i)
    for i in range(0,len(arrlist)-1):
        print(arrlist[i],end=' ')
    print(arrlist[-1])