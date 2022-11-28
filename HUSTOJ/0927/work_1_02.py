n = input()
a = set(map(int,input().split()))
m = input()
b = set(map(int,input().split()))
l0 = sorted(list(a&b))
l1 = sorted(list(a|b))
l2 = sorted(list(a-b))

print(' '.join(str(x) for x in l0))
print(' '.join(str(x) for x in l1))
print(' '.join(str(x) for x in l2))

