n = list(map(int,input().split()))[0]
page = []
sum = 0
for i in list(map(int,input().split())):
    if page.count(i) == 0:
        page.insert(0,i)
        sum += 1
    else:
        pos = page.index(i)
        if pos != 0:
            del page[pos]
            page.insert(0,i)
    if len(page) > n:
        page.pop()


print(sum)
page.sort()
print(' '.join(str(x) for x in page))