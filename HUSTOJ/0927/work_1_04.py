n = int(input())
nums = list(map(int,input().split()))
for i in range(1,n):
    for j in range(0,i):
        if nums[i] < nums[j]:
            nums.insert(j,nums[i])
            del nums[i+1]
    print(' '.join(str(x) for x in nums))
