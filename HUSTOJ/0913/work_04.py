def get_input():
    n = int(input())
    scores = list(map(int,input().split()))
    scores.sort()
    return n,scores

if __name__ == '__main__':
    n,scores = get_input()
    sum = count = 0
    for i in range(0,n):
        sum += scores[i]
        if scores[i] >= 60:
            count += 1
    print('average = {:.1f}'.format(sum/n))
    print('count = {}'.format(count))
