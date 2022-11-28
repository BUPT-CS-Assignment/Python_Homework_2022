def get_half(num):
    return int(num / 2 if num % 2 == 0 else (num + 1) / 2)

def get_input():
    n = int(input())
    nums = list(map(int,input().split()))
    nums.sort()
    return n, nums

if __name__ == '__main__':
    sum = 0
    n, stu_list = get_input()
    for i in range(0,get_half(n)):
        sum = sum + get_half(stu_list[i])
    print(sum)

